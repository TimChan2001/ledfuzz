#include <stdio.h>
#include <stdlib.h>
#include "distance.h"  // 引入 distance 计算

int funcA() { return rand() % 100; }
int funcB() { return rand() % 100; }

int main() {
    setup_shm();  // 连接 AFL 共享内存

    int a = funcA();
    int b = funcB();

    distance_instrument(a - b);  // 只调用 distance(a - b)

    printf("a = %d, b = %d, distance = %d\n", a, b, a - b);
    
    return 0;
}
