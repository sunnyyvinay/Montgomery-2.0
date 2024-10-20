from manim import *
class video(Scene):
    def construct(self):
        limit_definition = MathTex(r"\lim_{x \to c} f(x) = L \iff \forall \epsilon 