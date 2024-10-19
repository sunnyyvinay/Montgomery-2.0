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

gemini_thread = None
retries = 0

generation_config = {
    "temperature": 1.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 3000,
    "response_mime_type": "text/plain",
}

main_model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash-002",
    generation_config = generation_config,
    system_instruction = """
        You are the world's best teacher, with proficiency especially in a variety of mathematics, physics, and computer science, including but not limited to AI/ML.
        You believe very strongly in the power of visual learning, and so you have trained yourself extensively in manim animations.
        
        You will assist the user by helping animate their thought process to assist with visual learning.
        What this means is that while the user is explaining their thought process, you will use python code for manim animation to draw out whatever they say.
        
        For example, if the user says "let's start with Einstein's equation," you will animate the equation.
        If the user says "let's move this variable to the other side" you will reanimate the equation accordingly.
        The user will not necessarily say these words verbatim, but the general idea is that you will animate every single step.
        
        The user will not always be addressing you directly. You are an assistant, so even if the user appears to be addressing an audience, animate as if it is speaking to you.
        For example, if the user says "let's do __", interpret it as a command
        """
)

mainChat = main_model.start_chat(history=[], enable_automatic_function_calling=False)

def call_gemini(user_prompt: str):
    """After thread is created, call Gemini, get a response, and begin executing commands
    
    Args:
        recorder: the recorder object must be created in the main process, so it is passed in to this function as an argument and used
    """
    global gemini_thread, retries

    # if function has been recursively called 3 times (in 3 attempts to retry a prompt), break out of loop
    if retries == 3:
        retries = 0
        print('An unexpected error occurred on Google\'s side.	Wait a bit and retry your request. If the issue persists after retrying, please report it using the Send feedback button in Google AI Studio.')        
        return

    model_prompt = f"""
        The last thing that the user said is:
        {user_prompt}
        
        Analyze what the user said, and identify whether it is related to the previous string of thought from the user. 
        You have three options for functions to call: nextCommand, speak_to_user, and animate_with_manim.
            the function nextCommand should be used when the user's statement is not related and nothing should be animated or said. This will be a very common case
            the function speak_to_user should be used when you are not sure what to do because the user's train of thought is too vague. You may ask for clarification. Be casual
            the function animate_with_manim should be used when the user's statement is related to the previous string of thought from the user. You will use python code for manim animation to draw out whatever they say.
            
        Rules when responding:
        - do not use any additional formatting like backticks, <tool_code>, or unnecessary wrappers.
        - do not use any additional formatting for language specifications like ```python...
        - When generating manim code, Assume all code will automatically be executed in python, do NOT include "```python..." in your parameter for the function
        - When generating manim code, Assume all necessary manim libraries are already imported properly. Do NOT import the manim library in your parameter for the function     
        - Only return the name of the function and its arguments as plain text, wrapped with <> brackets.
        
        You will output your response in the form:
        <function to call>
        arguments
        
        For example:
        <speak_to_user>
        Hello, I am your personal assistant. I am here to help you with your math and physics problems.
        
        Ommit any farewells, greetings, and backticks and unnecessary information.
        """
        
    try:
        response = mainChat.send_message(model_prompt)
        print(response.text)
        
        # pseudo function calling
        functionName = response.text.split('>')[0][1:]
        if functionName == 'speak_to_user':
            speak_to_user(response.text.split('>')[1].strip())
        elif functionName == 'animate_with_manim':
            animate_with_manim(response.text.split('>')[1])
        
        
        
    except ResourceExhausted as resource_error:
        print(f'You have exceeded the API call rate. Please wait a minute before trying again... \nError message from Google:\n{resource_error}')
        # tts_speak('You have exceeded the API call rate. Please wait a minute before trying agian...')
    except InternalServerError as internal_error:
        retries += 1
        print(f'An expected error occured on Google\'s side. Retrying after 1 second cooldown... Attempt {retries}/3')
        print(f'Error message from Google:\n{internal_error}')
    except Exception as e:
        print(f'Unknown error encountered. \nError message from Google:\n{e}')
    print('fin')

call_gemini("Let's start with the pythagorean theorem equation")

