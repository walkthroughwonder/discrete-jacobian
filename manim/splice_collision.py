#!/usr/bin/env python3
"""
Manim Community script for the Discrete Jacobian splice collision diagram.
For the presentation to Pablo Arrighi, Marin Costes, Luidnel Maignan.

Usage (Manim Community Edition):
    manim -pql manim/splice_collision.py SpliceCollision
    manim -pqh manim/splice_collision.py SpliceCollision   # higher quality

Requires: manim, and optionally networkx if you want more complex graphs.
"""

from manim import *

class SpliceCollision(Scene):
    def construct(self):
        # Title
        title = Text("The Splice Collision", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        subtitle = Text("Locally invertible, globally not injective", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.add(subtitle)

        # ========== S1 ==========
        s1_group = VGroup()
        s1_label = Text("S₁  (loop ⊔ out-star)", font_size=22, color=BLUE)
        s1_label.move_to(LEFT * 4.2 + UP * 1.8)

        # Nodes for S1: 0 (loop), 1 (center), 2, 3
        n0 = Dot(LEFT*5.2 + UP*0.5, color=YELLOW, radius=0.15)
        n1 = Dot(LEFT*4.0 + UP*0.5, color=WHITE, radius=0.15)
        n2 = Dot(LEFT*3.0 + UP*1.2, color=WHITE, radius=0.12)
        n3 = Dot(LEFT*3.0 + DOWN*0.2, color=WHITE, radius=0.12)

        # Labels
        l0 = Text("0", font_size=16).next_to(n0, DOWN, buff=0.08)
        l1 = Text("1", font_size=16).next_to(n1, DOWN, buff=0.08)
        l2 = Text("2", font_size=14).next_to(n2, RIGHT, buff=0.05)
        l3 = Text("3", font_size=14).next_to(n3, RIGHT, buff=0.05)

        # Edges: loop at 0, 1→2, 1→3
        loop = ArcBetweenPoints(n0.get_center() + UP*0.25, n0.get_center() + DOWN*0.25, 
                                 angle=2.8, color=YELLOW, stroke_width=3)
        e12 = Arrow(n1.get_center(), n2.get_center(), buff=0.15, color=BLUE, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        e13 = Arrow(n1.get_center(), n3.get_center(), buff=0.15, color=BLUE, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)

        s1_group = VGroup(n0, n1, n2, n3, l0, l1, l2, l3, loop, e12, e13, s1_label)
        self.add(s1_group)

        # ========== S2 ==========
        s2_label = Text("S₂  (loop ⊔ in-star)", font_size=22, color=GREEN)
        s2_label.move_to(LEFT * 4.2 + DOWN * 1.5)

        m0 = Dot(LEFT*5.2 + DOWN*2.5, color=YELLOW, radius=0.15)
        m1 = Dot(LEFT*4.0 + DOWN*2.5, color=WHITE, radius=0.15)
        m2 = Dot(LEFT*3.0 + DOWN*1.8, color=WHITE, radius=0.12)
        m3 = Dot(LEFT*3.0 + DOWN*3.2, color=WHITE, radius=0.12)

        ml0 = Text("0", font_size=16).next_to(m0, DOWN, buff=0.08)
        ml1 = Text("1", font_size=16).next_to(m1, DOWN, buff=0.08)
        ml2 = Text("2", font_size=14).next_to(m2, RIGHT, buff=0.05)
        ml3 = Text("3", font_size=14).next_to(m3, RIGHT, buff=0.05)

        loop2 = ArcBetweenPoints(m0.get_center() + UP*0.25, m0.get_center() + DOWN*0.25,
                                  angle=2.8, color=YELLOW, stroke_width=3)
        e12_2 = Arrow(m1.get_center(), m2.get_center(), buff=0.15, color=GREEN, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        e32 = Arrow(m3.get_center(), m2.get_center(), buff=0.15, color=GREEN, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)

        s2_group = VGroup(m0, m1, m2, m3, ml0, ml1, ml2, ml3, loop2, e12_2, e32, s2_label)
        self.add(s2_group)

        # ========== Common result ==========
        result_label = Text("Common successor (directed 4-path)", font_size=22, color=RED)
        result_label.move_to(RIGHT * 3.0 + UP * 2.0)

        # Path nodes: simplified 0-1-2-3
        p0 = Dot(RIGHT*1.5 + UP*0.3, color=YELLOW, radius=0.15)
        p1 = Dot(RIGHT*2.8 + UP*0.3, color=WHITE, radius=0.15)
        p2 = Dot(RIGHT*4.1 + UP*0.3, color=WHITE, radius=0.15)
        p3 = Dot(RIGHT*5.4 + UP*0.3, color=WHITE, radius=0.15)

        pl0 = Text("0", font_size=16).next_to(p0, DOWN, buff=0.08)
        pl1 = Text("1", font_size=16).next_to(p1, DOWN, buff=0.08)
        pl2 = Text("2", font_size=16).next_to(p2, DOWN, buff=0.08)
        pl3 = Text("3", font_size=16).next_to(p3, DOWN, buff=0.08)

        pe01 = Arrow(p0.get_center(), p1.get_center(), buff=0.15, color=RED, stroke_width=3)
        pe12 = Arrow(p1.get_center(), p2.get_center(), buff=0.15, color=RED, stroke_width=3)
        pe23 = Arrow(p2.get_center(), p3.get_center(), buff=0.15, color=RED, stroke_width=3)

        result_group = VGroup(p0, p1, p2, p3, pl0, pl1, pl2, pl3, pe01, pe12, pe23, result_label)
        self.add(result_group)

        # Arrows from S1 and S2 to result
        arrow1 = Arrow(LEFT*2.5 + UP*0.5, RIGHT*0.8 + UP*0.5, color=BLUE, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(LEFT*2.5 + DOWN*2.5, RIGHT*0.8 + DOWN*0.2, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.1)

        self.add(arrow1, arrow2)

        # Note about monodromy
        note = Text("The final path forgets which vertex held the loop\n→ discrete monodromy", 
                    font_size=18, color=ORANGE, line_spacing=1.1)
        note.move_to(RIGHT * 3.2 + DOWN * 2.2)
        self.add(note)

        # Rule reminder
        rule = Text("Rule: {(a,a),(b,c)} → {(a,b),(c,a)}", font_size=16, color=GRAY)
        rule.to_edge(DOWN, buff=0.25)
        self.add(rule)

        self.wait(2)


class SpliceRuleOnly(Scene):
    """Simpler scene showing just the rule."""
    def construct(self):
        title = Text("Splice Rule", font_size=36)
        title.to_edge(UP)
        self.add(title)

        left = Text("{(a,a), (b,c)}", font_size=28)
        arrow = Text("→", font_size=36)
        right = Text("{(a,b), (c,a)}", font_size=28)

        formula = VGroup(left, arrow, right).arrange(RIGHT, buff=0.5)
        formula.move_to(ORIGIN)
        self.add(formula)

        desc = Text('"splice a loop into an edge"', font_size=22, color=GRAY)
        desc.next_to(formula, DOWN, buff=0.4)
        self.add(desc)

        self.wait(1)
