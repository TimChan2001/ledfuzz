# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import os

def read_file_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"Error: File '{file_path}' does not exist.")
        exit(1)
    
target_path = input("Enter the target path: ").strip()
program_name = read_file_content(target_path+'/name').strip()
bug_report = read_file_content(target_path+'/bug-report')
source_code = read_file_content(target_path+'/source-code')

print(program_name)
print(bug_report)
print(source_code)

client = OpenAI(api_key="add your api key", base_url="https://api.deepseek.com")

output_file = open(f'{target_path}/output.log','w')

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
This program has a vulnerability. I will provide you with a vulnerability report and some source code. Please attempt to analyze the 'triggering condition' of this vulnerability. Note that I will not provide all the source code at once. If you find the provided code insufficient for analysis, you can request additional code from me, for example, by asking, 'I would like to see the code for the xxx function.' Please note the following requirements:
1. try to use a conditional statement associated with the program to describe the triggering condition instead of natural languages. For example, a good triggering condition can be "a > b", "doapr_outch(sbuffer, buffer, &currlen, maxlen, ch) == 0", or "ptr == NULL"
2. When analyzing the vulnerability, please consider the program's purpose, the function's purpose, input file formats, and code comments.

bug report:

{bug_report}

source code:

{source_code}
"""})

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=False
)

print(response.choices[0].message.content)
output_file.write(response.choices[0].message.content)
output_file.close()



