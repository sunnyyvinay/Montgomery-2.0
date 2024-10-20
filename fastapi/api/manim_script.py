from manim import *
class video(Scene):
    def construct(self):
        line1 = Text("Hey, I'm Montgomery!").scale(1.2)
        self.play(Write(line1))
        self.play(line1.animate.shift(UP))
        line2 = Text("Start by asking me anything!").scale(0.5).next_to(line1, DOWN)
        self.play(Write(line2))
    