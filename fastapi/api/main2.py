from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_call import call_gemini
from external_functions import speak_to_user, animate_with_manim

app = FastAPI()

# Pydantic model to define the structure of the expected input
class UserInput(BaseModel):
    user_input: str  # The string input from the user

# Adding CORS middleware to allow communication between frontend (React) and backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/")
def health_check():
    return "health check complete"

# Route to handle user input and process it using call_gemini
@app.post("/submit")
async def process_user_input(user_input: UserInput):
    # Call the Gemini function with the user input
    result = call_gemini(user_input.user_input)

    # Optionally call other functions like speak_to_user or animate_with_manim if needed
    # speak_to_user(result)
    # animate_with_manim(result)

    # Return a response (you can return anything, including the result from Gemini)
    return {"message": "Processed input", "result": result}
