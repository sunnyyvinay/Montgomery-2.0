print("executing file")

# in order to execute code live, pass the code in as a string to a variable and use the python exec() function to run it

code = """
print('test 1')
"""

code2 = """
print('test 2')
"""

exec(code + code2)

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import (ResourceExhausted, FailedPrecondition, 
                                        InvalidArgument, ServiceUnavailable, 
                                        InternalServerError)

from external_functions import speak_to_user, animate_with_manim
# Load API keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import subprocess

result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
#print(result.stdout)