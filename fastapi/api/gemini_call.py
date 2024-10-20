import os
from dotenv import load_dotenv
import time
import google.generativeai as genai
from google.api_core.exceptions import (ResourceExhausted, FailedPrecondition, 
                                        InvalidArgument, ServiceUnavailable, 
                                        InternalServerError)

from external_functions import speak_to_user, animate_with_manim
# Load API keys
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
        
        You are also a minimalist. Animate the least amount as possible while still communicating the user's point. Try to go step by step, only animating one line at a time.
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
        
        # Instructions
        Analyze what the user said, and identify whether it is related to the previous string of thought from the user. 
        You have three options for functions to call: nextCommand, speak_to_user, and animate_with_manim.
            the function nextCommand should be used when the user's statement is not related and nothing should be animated or said. This will be a very common case
            the function speak_to_user should be used when you are not sure what to do because the user's train of thought is too vague. You may ask for clarification. Be casual
            the function animate_with_manim should be used when the user's statement is related to the previous string of thought from the user. You will use python code for manim animation to draw out whatever they say.
            
        # Rules when responding:
        - Be minimalist. Generate only the minimum amount of code necessary to reflect what the user is trying to communicate. Do not skip steps. Only work out multiple steps if asked to.
        - all steps should be displayed sequentially downward. That means the earliest step should the top most step.
        - do not use any additional formatting like backticks, <tool_code>, or unnecessary wrappers.
        - When generating manim code, Assume all code will automatically be executed in python, do NOT include "```python..." in your parameter for the function
        - Only return the name of the function and its arguments as plain text, wrapped with <> brackets.
        
        # ABSOLUTE Rules when generating code:
        YOU MUST FOLLOW THESE RULES NO MATTER WHAT
        - do not use any additional formatting like backticks, <tool_code>, or unnecessary wrappers.
        - List steps sequentially, from top to bottom.
        - do not use any additional formatting for language specifications like ```python...", assume that the environment you are coding in is already in python
        - When generating manim code, Assume all necessary manim libraries are already imported properly. Do NOT import the manim library in your parameter for the function    
        - The class name with the manim code must ALWAYS be "video", so you should ALWAYS be writing code in "class video(Scene)" 
        - Since you are writing code in the form of a string, when there is a backslash you must use double backslashes so that it does not get mistaken as an escape character.
        - do not include any waiting in your code. No time.sleep! Remember, you are minimalist.
        
        # Important Thought Process to Follow:
        - only output the minimum amount of code needed to communicate the user's idea
        - at every step, silently ask yourself what the position of the location of the current object is
        - at every step, silently ask yourself whether or not there is any overlap of objects. We absolutely do NOT want any overlap. move things up or down as needed.
        - make sure that there is no repetitive information. Review your code once it is all generated
        - If possible do not split up a single equation into multiple separate objects to animate
        - Consider how many lines are being displayed. Remember that **the manim animation output window is limited**. What this means is that if you have more than 3 lines being displayed you must shift the lines up vertically to make room to ensure all lines can be read.
        - Do not overcomplicate the code. Beware of overlap. Mentally analyze the positioning of each line object and ensure that:
            1. There is no overlap between lines
            2. All lines are visible (if there are lots of lines, shift them upward!)
            3. People like it when the text is centered on the screen! Make vertical/horizontal shifts accordingly.
            4. All steps should be formed sequentially and downwards. what this means that visually step 2 should appear BELOW step 1, and step 3 should appear BELOW step 2, and so on.
            
        # Important Background Information Regarding Manim Animations
        Use the following information to help guide your choices of positioning
        - animations typically can contain at most 1 graph (if any)
        - when text/equations are scaled 1x, about 10 lines can be displayed at once. Consider this when assigning locations to equations
        - when text/equations are scaled 2x, about 6 lines can be displayed at one. Consider this when assigning locations to equations
            

        You will output your response in the form:
        <function to call>
        arguments
        
        For example:
        <speak_to_user>
        Hello, I am your personal assistant. I am here to help you with your math and physics problems.
        
        Ommit any farewells, greetings, and backticks and unnecessary information.
        """
        
    try:
        startTime = time.time()
        response = mainChat.send_message(model_prompt)
        endTime = time.time()
        
        print(f'Gemini took {round((startTime - endTime), 2)} seconds to respond')
        # print(response.text)
        
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

#call_gemini("Let's start with the pythagorean theorem")
#call_gemini("Let's start with Einstein's equation of energy in terms of mass")


