from gemini_call import call_gemini
from external_functions import speak_to_user, animate_with_manim

while True:
    user_input = input("Enter Prompt: ")
    call_gemini(user_input)