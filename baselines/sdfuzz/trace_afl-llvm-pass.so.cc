#define AFL_LLVM_PASS

#include "../config.h"
#include "../debug.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/Support/Debug.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

using namespace llvm;

namespace {

class AFLCoverage : public ModulePass {
public:
  static char ID;
  AFLCoverage() : ModulePass(ID) {}

  bool runOnModule(Module &M) override;
};

} // namespace

char AFLCoverage::ID = 0;

bool AFLCoverage::runOnModule(Module &M) {
  LLVMContext &C = M.getContext();
  IntegerType *Int8Ty = IntegerType::getInt8Ty(C);
  IntegerType *Int32Ty = IntegerType::getInt32Ty(C);

  char be_quiet = 0;
  if (isatty(2) && !getenv("AFL_QUIET")) {
    SAYF(cCYA "afl-llvm-pass " cBRI VERSION cRST " by <lszekeres@google.com>\n");
  } else
    be_quiet = 1;

  char *inst_ratio_str = getenv("AFL_INST_RATIO");
  unsigned int inst_ratio = 100;
  if (inst_ratio_str) {
    if (sscanf(inst_ratio_str, "%u", &inst_ratio) != 1 || !inst_ratio || inst_ratio > 100)
      FATAL("Bad value of AFL_INST_RATIO (must be between 1 and 100)");
  }

  GlobalVariable *AFLMapPtr = new GlobalVariable(
      M, PointerType::get(Int8Ty, 0), false, GlobalValue::ExternalLinkage, 0, "__afl_area_ptr");

  GlobalVariable *AFLPrevLoc = new GlobalVariable(
      M, Int32Ty, false, GlobalValue::ExternalLinkage, 0, "__afl_prev_loc",
      0, GlobalVariable::GeneralDynamicTLSModel, 0, false);

  int inst_blocks = 0;

  // Declare printf
  FunctionType *printfType = FunctionType::get(
      IntegerType::getInt32Ty(C), PointerType::get(Type::getInt8Ty(C), 0), true);
  FunctionCallee printfFunc = M.getOrInsertFunction("printf", printfType);

  for (auto &F : M) {
    if (F.isDeclaration()) continue;

    // Insert AFL edge coverage
    for (auto &BB : F) {
      BasicBlock::iterator IP = BB.getFirstInsertionPt();
      IRBuilder<> IRB(&(*IP));

      if (AFL_R(100) >= inst_ratio) continue;

      unsigned int cur_loc = AFL_R(MAP_SIZE);
      ConstantInt *CurLoc = ConstantInt::get(Int32Ty, cur_loc);

      LoadInst *PrevLoc = IRB.CreateLoad(AFLPrevLoc);
      PrevLoc->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *PrevLocCasted = IRB.CreateZExt(PrevLoc, Int32Ty);

      LoadInst *MapPtr = IRB.CreateLoad(AFLMapPtr);
      MapPtr->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *MapPtrIdx = IRB.CreateGEP(MapPtr, IRB.CreateXor(PrevLocCasted, CurLoc));

      LoadInst *Counter = IRB.CreateLoad(MapPtrIdx);
      Counter->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *Incr = IRB.CreateAdd(Counter, ConstantInt::get(Int8Ty, 1));
      IRB.CreateStore(Incr, MapPtrIdx)->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

      IRB.CreateStore(ConstantInt::get(Int32Ty, cur_loc >> 1), AFLPrevLoc)
          ->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

      inst_blocks++;
    }

    // Entering function
    Instruction *insertBefore = nullptr;
    for (Instruction &I : F.getEntryBlock()) {
      if (!isa<AllocaInst>(&I)) {
        insertBefore = &I;
        break;
      }
    }
    if (!insertBefore) insertBefore = F.getEntryBlock().getTerminator();

    IRBuilder<> entryBuilder(insertBefore);
    std::string entryMsg = "[CALL] Entering function: " + F.getName().str() + "\n";
    Value *entryStr = entryBuilder.CreateGlobalStringPtr(entryMsg);
    entryBuilder.CreateCall(printfFunc, {entryStr});
  }

  // Call site logging
  for (auto &F : M) {
    for (auto &BB : F) {
      for (auto &I : BB) {
        if (auto *call = dyn_cast<CallBase>(&I)) {
          Function *called = call->getCalledFunction();
          if (called && !called->isDeclaration()) {
            std::string filename = "<unknown>";
            unsigned line = 0;
            if (DILocation *Loc = I.getDebugLoc()) {
              line = Loc->getLine();
              filename = Loc->getFilename().str();
              if (filename.empty()) {
                if (DILocation *inlined = Loc->getInlinedAt()) {
                  line = inlined->getLine();
                  filename = inlined->getFilename().str();
                }
              }
            }

            IRBuilder<> builder(&I);
            std::string msg = "[TRACE] Function " + called->getName().str() +
                              " called from " + filename + ":" + std::to_string(line) + "\n";
            Value *str = builder.CreateGlobalStringPtr(msg);
            builder.CreateCall(printfFunc, {str});
          }
        }
      }
    }
  }

  // Leaving function
  for (auto &F : M) {
    if (F.isDeclaration()) continue;

    for (auto &BB : F) {
      for (auto &I : BB) {
        if (isa<ReturnInst>(&I)) {
          IRBuilder<> builder(&I);
          std::string msg = "[RETURN] Leaving function: " + F.getName().str() + "\n";
          Value *str = builder.CreateGlobalStringPtr(msg);
          builder.CreateCall(printfFunc, {str});
        }
      }
    }
  }

  if (!be_quiet) {
    if (!inst_blocks) WARNF("No instrumentation targets found.");
    else OKF("Instrumented %u locations (%s mode, ratio %u%%).",
             inst_blocks, getenv("AFL_HARDEN") ? "hardened" :
             ((getenv("AFL_USE_ASAN") || getenv("AFL_USE_MSAN")) ?
              "ASAN/MSAN" : "non-hardened"), inst_ratio);
  }

  return true;
}

// Register pass
static void registerAFLPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {
  PM.add(new AFLCoverage());
}

static RegisterStandardPasses RegisterAFLPass(
    PassManagerBuilder::EP_OptimizerLast, registerAFLPass);

static RegisterStandardPasses RegisterAFLPass0(
    PassManagerBuilder::EP_EnabledOnOptLevel0, registerAFLPass);
