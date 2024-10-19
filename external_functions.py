from manim import *

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
    if "from manim import *" in code:
        code = code.replace("from manim import *", "")
    print(code) #temporary
    # exec(code)
    
# johnny: finished installing latex, location of installation: macintosh 
class test(Scene):
    def construct(self):
        #create 2 base newton law equations
        t01 = MathTex(r'F_g = \frac{Gmm}{r^2}')
        self.play(Write(t01))
        self.wait(1)