#!/usr/bin/env python3
"""
Full animated version of the Discrete Jacobian splice collision.
Shows both S₁ and S₂, highlights the matches, performs the rewrites,
and demonstrates they produce isomorphic directed 4-paths (discrete monodromy).

Recommended for the presentation:
    manim -pqh manim/splice_full_collision.py FullCollision

(Use -pql for a fast preview.)
"""

from manim import *

class FullCollision(Scene):
    def construct(self):
        # ===== Title =====
        title = Text("The Splice Collision", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        rule = Text("Rule: {(a,a), (b,c)}  →  {(a,b), (c,a)}", font_size=20, color=GRAY)
        rule.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(rule))
        self.wait(0.6)

        # ===== Helper to create a small graph =====
        def make_graph(center, nodes_pos, edges, labels, color=WHITE, loop_color=YELLOW):
            dots = {}
            texts = {}
            edge_mobs = VGroup()
            for name, pos in nodes_pos.items():
                d = Dot(center + pos, radius=0.14, color=YELLOW if name == "0" else color)
                t = Text(name, font_size=16).next_to(d, DOWN, buff=0.08)
                dots[name] = d
                texts[name] = t
            for (u, v) in edges:
                if u == v:  # loop
                    arc = ArcBetweenPoints(
                        dots[u].get_center() + UP*0.22,
                        dots[u].get_center() + DOWN*0.22,
                        angle=2.5, color=loop_color, stroke_width=3.5
                    )
                    edge_mobs.add(arc)
                else:
                    arr = Arrow(
                        dots[u].get_center(), dots[v].get_center(),
                        buff=0.16, stroke_width=2.8, color=color,
                        max_tip_length_to_length_ratio=0.18
                    )
                    edge_mobs.add(arr)
            return VGroup(*dots.values(), *texts.values(), edge_mobs), dots

        # ===== S1 =====
        s1_label = Text("S₁  (loop ⊔ out-star)", font_size=22, color=BLUE)
        s1_label.move_to(LEFT * 4.8 + UP * 2.0)

        s1_nodes = {
            "0": LEFT*1.1 + UP*0.0,
            "1": ORIGIN,
            "2": RIGHT*1.0 + UP*0.9,
            "3": RIGHT*1.0 + DOWN*0.9,
        }
        s1_edges = [("0", "0"), ("1", "2"), ("1", "3")]
        s1_group, s1_dots = make_graph(LEFT*4.5 + UP*0.3, s1_nodes, s1_edges, None, color=BLUE)

        self.play(FadeIn(s1_label), FadeIn(s1_group))
        self.wait(0.7)

        # ===== S2 =====
        s2_label = Text("S₂  (loop ⊔ in-star)", font_size=22, color=GREEN)
        s2_label.move_to(LEFT * 4.8 + DOWN * 1.3)

        s2_nodes = {
            "0": LEFT*1.1 + UP*0.0,
            "1": ORIGIN,
            "2": RIGHT*1.0 + UP*0.0,
            "3": RIGHT*0.3 + DOWN*1.0,
        }
        s2_edges = [("0", "0"), ("1", "2"), ("3", "2")]
        s2_group, s2_dots = make_graph(LEFT*4.5 + DOWN*2.4, s2_nodes, s2_edges, None, color=GREEN)

        self.play(FadeIn(s2_label), FadeIn(s2_group))
        self.wait(0.9)

        # ===== Highlight matches =====
        highlight1 = SurroundingRectangle(s1_group, color=ORANGE, buff=0.12)
        highlight2 = SurroundingRectangle(s2_group, color=ORANGE, buff=0.12)
        self.play(Create(highlight1), Create(highlight2))
        self.wait(0.6)
        self.play(FadeOut(highlight1), FadeOut(highlight2))

        # ===== Result path =====
        result_label = Text("Common successor\n(directed 4-path)", font_size=22, color=RED, line_spacing=1.1)
        result_label.move_to(RIGHT * 3.3 + UP * 2.1)

        path_nodes = {
            "A": LEFT*1.8,
            "B": LEFT*0.6,
            "C": RIGHT*0.6,
            "D": RIGHT*1.8,
        }
        path_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        path_group, path_dots = make_graph(RIGHT*3.2 + UP*0.2, path_nodes, path_edges, None, color=RED)

        # ===== Animate both transforming =====
        self.play(
            s1_group.animate.scale(0.7).move_to(LEFT*4.5 + UP*1.5),
            s2_group.animate.scale(0.7).move_to(LEFT*4.5 + DOWN*1.8),
            run_time=1.0
        )

        # Arrows indicating rewrite
        arr1 = Arrow(LEFT*2.8 + UP*1.5, RIGHT*0.8 + UP*0.6, color=BLUE, stroke_width=3)
        arr2 = Arrow(LEFT*2.8 + DOWN*1.8, RIGHT*0.8 + DOWN*0.4, color=GREEN, stroke_width=3)

        self.play(GrowArrow(arr1), GrowArrow(arr2))
        self.play(FadeIn(result_label), FadeIn(path_group))
        self.wait(0.8)

        # Monodromy message
        mono = Text("Both non-isomorphic states map to the same path\nThe identity of the loop vertex is forgotten\n→ Discrete Monodromy", 
                    font_size=20, color=ORANGE, line_spacing=1.15)
        mono.move_to(DOWN * 2.6)
        self.play(Write(mono))
        self.wait(1.5)

        # Final takeaway
        takeaway = Text("Locally invertible  ≠  Globally injective", font_size=26, weight=BOLD)
        takeaway.to_edge(DOWN, buff=0.25)
        self.play(FadeOut(mono), Write(takeaway))
        self.wait(2.5)

        # Optional: fade everything to leave a clean end frame
        self.play(*[FadeOut(m) for m in self.mobjects])
        end = Text("Sharpness witness for context-preservation", font_size=28)
        self.play(Write(end))
        self.wait(2)
