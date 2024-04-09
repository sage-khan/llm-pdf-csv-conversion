import subprocess
import pandas as pd
from io import StringIO
import os
import sys
import re
from config import command

text_file_path = sys.argv[1]
template_path = sys.argv[2]
output_path = sys.argv[3]

def extract_content_within_backticks(input_string):
    start_index = input_string.find("```")
    end_index = input_string.rfind("```")
    if start_index != -1 and end_index != -1:
        return input_string[start_index + 3:end_index].strip()
    else:
        return None

def convert_to_csv(input_string):
    content = extract_content_within_backticks(input_string)
    if content:
        data = StringIO(content)
        df = pd.read_csv(data)
        return df
    else:
        return None

process = subprocess.Popen(command.format(text_file_path=text_file_path,template_path=template_path), stdout=subprocess.PIPE, shell=True)

output, _ = process.communicate()

output = output.decode("utf-8")

print(output)

output = output.replace('csv','')
match = re.search(r'```(.*?)```', output, re.DOTALL)
if match:
    csv_data = match.group(1)

    with open(output_path,'w') as file:
      file.write(csv_data)
      file.close()
    print("CSV generated successfully")
else:
   with open(output_path,'w') as file:
      file.write(output)
      file.close()
      print("CSV generated successfully")

