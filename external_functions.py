from manim import *
import tempfile
import subprocess

config.media_width = "100%"
config.verbosity = "WARNING"

def speak_to_user(text_to_speech):
    """
    Speak to user (verbal feedback), using text to speech via an API
    
    Args:
        text_to_speech: the text in the form of a string that will be spoken verbally to user
        
    Returns:
        0 on successful call
    """
    print('function speak_to_user called')
    print(text_to_speech) #temporary
    return 0

def animate_with_manim(code):
    """
    Generate manim code
    
    Args:
        code: manim code passed as a string
        
    Returns:
        0 on successful call
    """
    print('function animate_with_manim called')
    if "from manim import *" not in code:
        manimImport = "from manim import *"
        code = manimImport + code
    print(code) #temporary
    
# johnny: finished installing latex, location of installation: macintosh 
from manim import *

# class video(Scene):
#     def construct(self):
#         #create 2 base newton law equations
#         t01 = MathTex(r'F_g = \frac{Gmm}{r^2}')
#         self.play(Write(t01))
#         self.wait(1)




# Create a temporary file
with tempfile.NamedTemporaryFile(suffix=".py") as tmp:
    code = r"""
from manim import *

class video(Scene):
    def construct(self):
        #create 2 base newton law equations
        t01 = MathTex(r'F_g = \frac{Gmm}{r^2}')
        self.play(Write(t01))
        self.wait(1)
            
    """
    # Write the code to run the generated class to the temporary file
    tmp.write(code.encode())
    tmp.flush()

    # Run the temporary file as a manim animation
    try:
        #subprocess.run(["conda", "activate", "calhacks"])
        subprocess.run(["manim", tmp.name, "video", "-pqh"])
    except subprocess.CalledProcessError as e:
        print(f"Error running Manim: {e}")