from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess


app = FastAPI()

class UserInput(BaseModel):
    userInput: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return 'health check complete'

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "message": f"Received query: {q}"}

from fastapi import FastAPI, File, UploadFile, Response
import os
import subprocess

app = FastAPI()

@app.post("/submit")
async def process_manim_code(user_input: str):
    # Here you'd pass the user input to the Gemini AI model
    # Then, Gemini returns the Manim code, which you'd run

    # For demonstration, let's assume the Manim code is processed
    # Save the Manim animation to a video file
    manim_code = f"""
    from manim import *
    
    class video(Scene):
        def construct(self):
            equation = MathTex("{user_input}")
            self.play(Write(equation))
            self.wait(2)
    """
    
    # Write the code to a .py file
    with open("generated_manim.py", "w") as f:
        f.write(manim_code)
    
    # Run the manim code using subprocess
    subprocess.run(["manim", "-pql", "generated_manim.py", "video"])

    # Assume the video is saved as "video.mp4" in the current directory
    video_path = "media/videos/video.mp4"

    if os.path.exists(video_path):
        # Return the video binary data
        with open(video_path, "rb") as video_file:
            return Response(content=video_file.read(), media_type="video/mp4")
    else:
        return {"error": "Video generation failed"}
    
app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000"],  # Update with your frontend URL
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
