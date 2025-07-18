# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import os
import sys

def read_file_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"Error: File '{file_path}' does not exist.")
        exit(1)

args =  sys.argv
if len(args) != 2:
    print("Usage:", args[0], " dir_path\n")
    sys.exit()

# target_path = input("Enter the target path: ").strip()
target_path = args[1]
program_name = read_file_content(target_path+'/name').strip()
bug_report = read_file_content(target_path+'/bug-report')
source_code = read_file_content(target_path+'/source-code')

example_1 = read_file_content('/root/ledfuzz/example_1')
example_2 = read_file_content('/root/ledfuzz/example_2')

print(program_name)
print(bug_report)
print(source_code)

client = OpenAI(api_key="", base_url="https://api.deepseek.com")

output_file = open(f'{target_path}/tc.log','w')

messages=[{"role": "system", "content": "You are an expert in software security"},{"role": "user", "content": f"What do you know about program '{program_name}', like its purpose and input format?"},]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stream=False
)

reply_content = response.choices[0].message.content

output_file.write('About the Program:\n')
output_file.write(response.choices[0].message.content)
output_file.write('\n\n\nTriggering Condition Analysis:\n')

messages.append(response.choices[0].message)
messages.append({"role": "user", "content": f"""
This program has a vulnerability. Analyze the triggering conditions of the vulnerability step by step, using the information and instructions I provide.

Information:
    {bug_report}

    Relevant Source Code:
    {source_code}

Instructions:
    1. Based on the information above, output the triggering conditions of the vulnerability by following these step-by-step guidelines:
        (1) Identify and output each conditional statement along with its code location.
        (2) If multiple conditional statements across different locations are required, assign an execution order to each group.
        (3) For any complex conditional statements, decompose them into atomic conditional statements, and assign a conjunct identifier to each one for later reconstruction.
        (4) Finally, output all triggering conditions in the form of tuples: <cond, loc, seq, conj>

    2. Please refer to these detailed example I have provided:
    {example_1}
    {example_2}

    3. Except for common standard/library functions, avoid assuming function definitions.
    If more source code is needed for your analysis, append the note:
    "Need the content of function(s): xxx, xxx" at the end of your output, and I will provide it.

"""})

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=False
)

print(response.choices[0].message.content)
output_file.write(response.choices[0].message.content)
output_file.close()



