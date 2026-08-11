#!/usr/bin/env python3
"""
Animated Manim scene for the Discrete Jacobian splice collision.
Shows the rewrite happening and both S1 and S2 mapping to the same path.

Usage:
    manim -pql manim/splice_animated.py SpliceAnimated
    manim -pqh manim/splice_animated.py SpliceAnimated   # higher quality for presentation
"""

from manim import *

class SpliceAnimated(Scene):
    def construct(self):
        # Title
        title = Text("Splice Collision – Animated", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))
        self.wait(0.5)

        # Rule display
        rule_text = Text("Rule:  {(a,a), (b,c)}  →  {(a,b), (c,a)}", font_size=22)
        rule_text.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(rule_text))
        self.wait(0.8)

        # ========== Build S1 ==========
        s1_label = Text("S₁  (loop ⊔ out-star)", font_size=24, color=BLUE)
        s1_label.move_to(LEFT * 4.5 + UP * 1.6)

        # Nodes
        n0 = Dot(LEFT*5.5 + UP*0.4, color=YELLOW, radius=0.18)
        n1 = Dot(LEFT*4.0 + UP*0.4, color=WHITE, radius=0.18)
        n2 = Dot(LEFT*2.7 + UP*1.3, color=WHITE, radius=0.15)
        n3 = Dot(LEFT*2.7 + DOWN*0.5, color=WHITE, radius=0.15)

        l0 = Text("0", font_size=18).next_to(n0, DOWN, buff=0.1)
        l1 = Text("1", font_size=18).next_to(n1, DOWN, buff=0.1)
        l2 = Text("2", font_size=16).next_to(n2, UR, buff=0.05)
        l3 = Text("3", font_size=16).next_to(n3, DR, buff=0.05)

        # Edges
        loop = ArcBetweenPoints(
            n0.get_center() + UP*0.3, n0.get_center() + DOWN*0.3,
            angle=2.6, color=YELLOW, stroke_width=4
        )
        e12 = Arrow(n1.get_center(), n2.get_center(), buff=0.18, color=BLUE, stroke_width=3)
        e13 = Arrow(n1.get_center(), n3.get_center(), buff=0.18, color=BLUE, stroke_width=3)

        s1_nodes = VGroup(n0, n1, n2, n3, l0, l1, l2, l3)
        s1_edges = VGroup(loop, e12, e13)
        s1 = VGroup(s1_label, s1_nodes, s1_edges)

        self.play(FadeIn(s1_label), FadeIn(s1_nodes))
        self.play(Create(loop), Create(e12), Create(e13))
        self.wait(1.0)

        # Highlight the match that will be spliced (loop + one edge)
        match_box = SurroundingRectangle(VGroup(n0, n1, n2, loop, e12), color=ORANGE, buff=0.15)
        match_label = Text("Match: loop + edge", font_size=16, color=ORANGE)
        match_label.next_to(match_box, UP, buff=0.1)
        self.play(Create(match_box), FadeIn(match_label))
        self.wait(0.8)

        # ========== Animate the rewrite ==========
        # We will morph the selected edge + loop into the spliced form
        # For clarity, fade out the old and bring in the result path

        # Create the resulting path (for S1 splicing the 1→2 edge)
        # Result example: path involving the loop vertex
        p0 = Dot(RIGHT*1.0 + UP*0.4, color=YELLOW, radius=0.18)
        p1 = Dot(RIGHT*2.5 + UP*0.4, color=WHITE, radius=0.18)
        p2 = Dot(RIGHT*4.0 + UP*0.4, color=WHITE, radius=0.18)
        p3 = Dot(RIGHT*5.5 + UP*0.4, color=WHITE, radius=0.18)

        pl0 = Text("0", font_size=18).next_to(p0, DOWN, buff=0.1)
        pl1 = Text("1", font_size=18).next_to(p1, DOWN, buff=0.1)
        pl2 = Text("2", font_size=18).next_to(p2, DOWN, buff=0.1)
        pl3 = Text("3", font_size=18).next_to(p3, DOWN, buff=0.1)

        pe01 = Arrow(p0.get_center(), p1.get_center(), buff=0.18, color=RED, stroke_width=4)
        pe12 = Arrow(p1.get_center(), p2.get_center(), buff=0.18, color=RED, stroke_width=4)
        pe23 = Arrow(p2.get_center(), p3.get_center(), buff=0.18, color=RED, stroke_width=4)

        result_label = Text("Common directed 4-path", font_size=22, color=RED)
        result_label.move_to(RIGHT * 3.2 + UP * 1.8)

        result = VGroup(p0, p1, p2, p3, pl0, pl1, pl2, pl3, pe01, pe12, pe23, result_label)

        # Animate transition
        self.play(
            FadeOut(match_box), FadeOut(match_label),
            FadeOut(s1_edges),
            run_time=0.8
        )

        # Move nodes toward the path positions (simplified morph)
        self.play(
            n0.animate.move_to(p0.get_center()),
            n1.animate.move_to(p1.get_center()),
            n2.animate.move_to(p2.get_center()),
            n3.animate.move_to(p3.get_center()),
            l0.animate.next_to(p0, DOWN, buff=0.1),
            l1.animate.next_to(p1, DOWN, buff=0.1),
            l2.animate.next_to(p2, DOWN, buff=0.1),
            l3.animate.next_to(p3, DOWN, buff=0.1),
            run_time=1.2
        )

        self.play(Create(pe01), Create(pe12), Create(pe23), FadeIn(result_label))
        self.wait(0.5)

        # Now bring in S2 briefly to show it also maps to the same thing
        s2_note = Text("S₂ (loop ⊔ in-star) also rewrites\nto an isomorphic path", font_size=20, color=GREEN)
        s2_note.move_to(DOWN * 2.2)
        self.play(FadeIn(s2_note))
        self.wait(1.2)

        # Monodromy message
        mono = Text("The final path forgets which vertex carried the loop\n→ Discrete Monodromy", 
                    font_size=22, color=ORANGE, line_spacing=1.2)
        mono.move_to(DOWN * 2.2)
        self.play(Transform(s2_note, mono))
        self.wait(2.0)

        # Final emphasis
        final = Text("Locally invertible  ≠  Globally injective", font_size=26, weight=BOLD)
        final.to_edge(DOWN, buff=0.3)
        self.play(Write(final))
        self.wait(2.5)


class SpliceSideBySide(Scene):
    """Static side-by-side for slides if animation is not needed."""
    def construct(self):
        title = Text("Splice Collision", font_size=36, weight=BOLD)
        title.to_edge(UP)
        self.add(title)

        # (You can expand this with the earlier static version)
        note = Text("See SpliceAnimated for the full rewrite animation", font_size=24)
        note.move_to(ORIGIN)
        self.add(note)
        self.wait(1)
