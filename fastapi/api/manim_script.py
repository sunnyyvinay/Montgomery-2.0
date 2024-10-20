from manim import *
class video(Scene):
    def construct(self):
        equation = MathTex("a^2 + b^2 = c^2").scale(2)
        self.add(equation.to_edge(UP))

