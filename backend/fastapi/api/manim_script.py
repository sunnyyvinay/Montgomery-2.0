from manim import *
class video(Scene):
    def construct(self):
        matrix = Matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]).scale(2)
        self.play(Write(matrix))

