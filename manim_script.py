from manim import *
class video(Scene):
    def construct(self):
        equation = MathTex("a^2 + b^2 = c^2").scale(2)
        self.play(Write(equation))
        right_triangle = Polygon(
            [0,0,0],[3,0,0],[3,2,0]
        ).set_fill(BLUE, opacity=0.5)
        self.play(Create(right_triangle))
        a = MathTex("a").next_to(right_triangle,DOWN)
        b = MathTex("b").next_to(right_triangle,LEFT)
        c = MathTex("c").next_to(right_triangle,RIGHT)
        self.play(Write(a),Write(b),Write(c))

