from manim import *
class video(Scene):
    def construct(self):
        integral = MathTex(r"\int", "(x^2 + 2)", "dx").scale(2)
        self.play(Write(integral))

