import subprocess

def build(task):

    if task == "run calculator":
        subprocess.call(["python3", "calculator.py"])
        return "finished"

    if task == "calculator":
        code = """
print("Calculator")
a = int(input("A: "))
b = int(input("B: "))
print("Result:", a+b)
"""
        open("calculator.py","w").write(code)
        return "Created calculator.py"

    if task == "hello":
        open("hello.py","w").write("print('Hello from AutoCoder')")
        return "Created hello.py"

    if task == "run hello":
        subprocess.call(["python3","hello.py"])
        return "finished"

    if task == "website":
        code = '''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "AutoCoder website working"

app.run(host="0.0.0.0", port=5000)
'''
        open("site.py","w").write(code)
        return "Created site.py"

    if task == "run website":
        subprocess.call(["python3","site.py"])
        return "finished"

    if task == "list":
        subprocess.call(["ls"])
        return ""

    return "Unknown task"

while True:
    task = input("AutoCoder> ")
    print(build(task))
