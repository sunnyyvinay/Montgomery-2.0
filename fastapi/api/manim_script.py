from manim import *
class video(Scene):
    def construct(self):
        equation1 = MathTex("y = e^{x}").scale(2).to_edge(UP)
        equation2 = MathTex("y + 2 = e^{x} + 2").next_to(equation1, DOWN)
        self.play(Write(equation1))
        self.play(Write(equation2))

