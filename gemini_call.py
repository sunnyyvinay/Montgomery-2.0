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
print(os.getenv("GEMINI_API_KEY"))

gemini_thread = None
retries = 0

generation_config = {
    "temperature": 1.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 3000,
    "response_mime_type": "text/plain",
}

# delete all text temporarily excluded
availableFunctions = [
    speak_to_user, # TTS to speak ot user
    animate_with_manim
]

main_model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    #tools = availableFunctions,
    generation_config = generation_config,
    system_instruction = """
        You are the world's best teacher, with proficiency especially in a variety of mathematics, physics, and computer science, including but not limited to AI/ML.
        You believe very strongly in the power of visual learning, and so you have trained yourself extensively in manim animations.
        
        You will assist the user by helping animate their thought process to assist with visual learning.
        What this means is that while the user is explaining their thought process, you will use python code for manim animation to draw out whatever they say.
        
        For example, if the user says "let's start with Einstein's equation," you will animate the equation.
        If the user says "let's move this variable to the other side" you will reanimate the equation accordingly.
        The user will not necessarily say these words verbatim, but the general idea is that you will animate every single step.
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
        {user_prompt}
        """
    
    try:
        response = mainChat.send_message(model_prompt)
        function_calls = 0
        for part in response.parts:
            if fn := part.function_call:
                if callable(globals().get(fn.name)):
                    try:
                        func = globals()[fn.name]
                        print(f'Function Called: {fn.name}')
                        kwargs = fn.args
                        func(**kwargs)
                        function_calls += 1
                        retries = 0
                    except Exception as e:
                        print('Unexpected error encountered attempting to open function... Trying again...')
                        print(f'Error Message:\n{e}')
                        call_gemini(user_prompt) 

        if function_calls == 0:
            retries += 1
            call_gemini(user_prompt) #if model only generates text instead of calling function, retry

    except ResourceExhausted as resource_error:
        print(f'You have exceeded the API call rate. Please wait a minute before trying again... \nError message from Google:\n{resource_error}')
        # tts_speak('You have exceeded the API call rate. Please wait a minute before trying agian...')
    except InternalServerError as internal_error:
        retries += 1
        print(f'An expected error occured on Google\'s side. Retrying after 1 second cooldown... Attempt {retries}/3')
        print(f'Error message from Google:\n{internal_error}')
    except Exception as e:
        print(f'Unknown error encountered. \nError message from Google:\n{e}')

    gemini_thread = None

try:
    call_gemini("say hi")
except InvalidArgument as keyError:
    print(f'Your API key is invalid. Please recheck your key. \nError message from Google:\n{keyError}')
except FailedPrecondition as locationError:
    print(f'Gemini API free tier is not available in your country. Please enable billing on your project in Google AI Studio. \nError message from Google:\n{locationError}')
except ServiceUnavailable as serviceError:
    print(f'The Gemini API service may be temporarily overloaded or down. Please try again later. \nError message from Google:\n{serviceError}')
except Exception as unknownError:
    print(f'An unknown error occured while attempting to connect to the API.\nError Message:\n{unknownError}')
