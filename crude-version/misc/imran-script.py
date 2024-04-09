import subprocess

command = '''ollama run mistral "Act like an expert in data formatting and structuring. Please read all contents of $(cat a1.txt) and structure it into csv style table so that it can be saved in csv table and can be reconciled anytime. Also please take care of random spaces between data and make it efficiently to ensure data integrity."'''

process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

output, _ = process.communicate()

output = output.decode("utf-8")

print("Output:", output)
