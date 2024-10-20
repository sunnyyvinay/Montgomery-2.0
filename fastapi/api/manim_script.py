from manim import *
class video(Scene):
    def construct(self):
        line1 = MathTex("y = x^2").shift(UP * 2)
        self.play(Write(line1))

