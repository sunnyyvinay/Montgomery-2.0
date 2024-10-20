from manim import *
class video(Scene):
    def construct(self):
        equation1 = MathTex("a^2 + b^2 = c^2").scale(2).shift(UP)
        equation2 = MathTex("2^2 + 3^2 = c^2").scale(2).shift(DOWN)
        equation3 = MathTex("4 + 9 = c^2").scale(2).shift(DOWN*2)
        equation4 = MathTex("13 = c^2").scale(2).shift(DOWN*3)
        equation5 = MathTex("c = \\sqrt{13}").scale(2).shift(DOWN*4)
        self.play(Write(equation1))
        self.play(Write(equation2))
        self.play(Write(equation3))
        self.play(Write(equation4))
        self.play(Write(equation5))

