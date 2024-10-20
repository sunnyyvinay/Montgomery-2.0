from manim import *
class video(Scene):
    def construct(self):
        equation1 = MathTex("a^2 + b^2 = c^2").scale(2)
        equation2 = MathTex("2^2 + 4^2 = c^2").scale(2).next_to(equation1, DOWN)
        equation3 = MathTex("4 + 16 = c^2").scale(2).next_to(equation2, DOWN)
        equation4 = MathTex("20 = c^2").scale(2).next_to(equation3, DOWN)
        equation5 = MathTex("c = \\sqrt{20}").scale(2).next_to(equation4, DOWN)
        self.play(Write(equation1))
        self.play(Write(equation2))
        self.play(Write(equation3))
        self.play(Write(equation4))
        self.play(Write(equation5))

