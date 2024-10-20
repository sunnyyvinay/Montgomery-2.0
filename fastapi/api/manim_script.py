from manim import *
class video(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
        )
        graph = axes.plot(lambda x: x, color=RED)
        eq = MathTex("y=x").scale(2).next_to(axes,UP)
        self.play(Create(axes),Create(graph),Write(eq))

