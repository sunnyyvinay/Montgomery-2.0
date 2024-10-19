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
    
    
class intro(Scene):
    def construct(self):
        #create 2 base newton law equations
        t01 = MathTex(r'F =')
        t02 = MathTex(r'ma')
        t0 = VGroup(t01, t02).arrange(RIGHT)
        t0t = Text("Newton's First Law", font_size=30)
        t0.move_to(UP*2.5+LEFT*3)
        t0t.next_to(t0, UP*2.3)
        t11 = MathTex(r'F_g') 
        t12 = MathTex(r'= \frac{Gmm}{r^2}') 
        t1 = VGroup(t11, t12).arrange(RIGHT)
        t1t = Text("Newton's Law of Gravitation", font_size=30)
        t1.move_to(UP*2.5+RIGHT*3)
        t1t.next_to(t1, UP)