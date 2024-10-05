from e2b_code_interpreter import CodeInterpreter
from dotenv import load_dotenv
import os


load_dotenv()


with CodeInterpreter(api_key=os.getenv("E2B_API_KEY")) as code_interpreter:
    code_interpreter.notebook.exec_cell("x = 1")
    execution = code_interpreter.notebook.exec_cell("x+=1; x")
    print(execution.text)  # outputs 2
