from manim import *
class video(Scene):
    def construct(self):
        equation1 = MathTex("a^2 + b^2 = c^2").scale(2).to_edge(UP)
        equation2 = MathTex("1^2 + 3^2 = c^2").next_to(equation1, DOWN).shift(0.5*DOWN)
        equation3 = MathTex("1 + 9 = c^2").next_to(equation2, DOWN).shift(0.5*DOWN)
        equation4 = MathTex("c^2 = 10").next_to(equation3, DOWN).shift(0.5*DOWN)
        equation5 = MathTex("c = \sqrt{10}").next_to(equation4, DOWN).shift(0.5*DOWN)
        self.play(Write(equation1))
        self.play(Write(equation2))
        self.play(Write(equation3))
        self.play(Write(equation4))
        self.play(Write(equation5))

