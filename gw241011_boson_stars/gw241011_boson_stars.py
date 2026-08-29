from manim import *
import numpy as np
import json
import os
import pandas as pd
import scipy.stats

BH_PRIMARY_COLOR = "#ff8c42"
BH_SECONDARY_COLOR = "#ff6b6b"
REMNANT_COLOR = "#e84c3d"
GW_COLOR = "#4a90e2"
HIGHLIGHT_COLOR = "#ffff99"
TEXT_COLOR = "#e0e0e0"
EXOTIC_COLOR = "#e84c3d"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "from_paper_figures")
COUPLING_COLORS = ["#4a90e2", "#e8a23d", "#3ca97a", "#d4622e", "#c77dbb", "#b08968"]


def spin_indicator(center, obj_radius, color, axis_length_factor=1.6,
                    equator_scale=1.6, equator_squash=0.3):
    """A perfectly vertical spin axis through the poles, plus the equatorial plane — the plane
    perpendicular to the spin axis, not the axis itself — drawn as a flattened ellipse in
    perspective, with an arrow marker that orbits it, always tangent to its direction of travel.

    Returns a VGroup(axis, equator, marker); animate spin with `start_spin(group)`, which
    returns a ValueTracker — do `tracker.animate.set_value(n_loops)` to orbit the marker
    n_loops times (its speed is what reads as "how fast this object spins").
    """
    half_len = obj_radius * axis_length_factor
    axis = Line(center + DOWN * half_len, center + UP * half_len, color=color, stroke_width=3)

    ring_a = obj_radius * equator_scale
    ring_b = ring_a * equator_squash
    equator = Ellipse(width=2 * ring_a, height=2 * ring_b, color=color, stroke_width=2.5)
    equator.move_to(center)

    marker = ArrowTriangleFilledTip(color=color, length=0.18)
    pos0 = equator.point_from_proportion(0)
    pos1 = equator.point_from_proportion(0.001)
    direction0 = pos1 - pos0
    angle0 = np.arctan2(direction0[1], direction0[0])
    marker.move_to(pos0)
    marker.rotate(angle0)

    group = VGroup(axis, equator, marker)
    group.equator = equator
    group.marker = marker
    group.marker_angle = angle0
    return group


def start_spin(indicator):
    """Attaches an orbiting-marker updater to `indicator` (from spin_indicator) and returns a
    ValueTracker. The marker rotates to stay tangent to its direction of travel. Animate with
    `tracker.animate.set_value(n_loops)`; call `indicator.marker.clear_updaters()` once that
    animation finishes.
    """
    tracker = ValueTracker(0)
    marker, equator = indicator.marker, indicator.equator
    state = {"angle": indicator.marker_angle}

    def update_marker(m):
        alpha = tracker.get_value() % 1
        pos = equator.point_from_proportion(alpha)
        pos2 = equator.point_from_proportion((alpha + 0.001) % 1)
        new_angle = np.arctan2(*(pos2 - pos)[1::-1])
        m.move_to(pos)
        m.rotate(new_angle - state["angle"])
        state["angle"] = new_angle

    marker.add_updater(update_marker)
    return tracker


class GW241011Overview(Scene):
    """Scene 1: Introduce GW241011 - very unequal masses, rapidly spinning primary"""

    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"GW241011", font_size=80, color=WHITE)
        title.to_edge(UP, buff=0.5)

        subtitle = Tex(r"A black hole merger detected 11 October 2024",
                        font_size=32, color=TEXT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(title), FadeIn(subtitle), run_time=1)
        self.wait(1.25)

        primary_start = LEFT * 3.3 + UP * 0.3
        secondary_start = RIGHT * 3.3 + DOWN * 0.3
        primary_radius = 0.55
        secondary_radius = 0.30

        primary = Circle(radius=primary_radius, color=BH_PRIMARY_COLOR, fill_opacity=0.95, stroke_width=0)
        primary.move_to(primary_start)
        secondary = Circle(radius=secondary_radius, color=BH_SECONDARY_COLOR, fill_opacity=0.9, stroke_width=0)
        secondary.move_to(secondary_start)

        primary_label = Tex(r"$\approx 20\,M_\odot$", font_size=26, color=WHITE)
        primary_label.next_to(primary, DOWN, buff=0.45)
        secondary_label = Tex(r"$\approx 6\,M_\odot$", font_size=22, color=WHITE)
        secondary_label.next_to(secondary, DOWN, buff=0.4)

        self.play(FadeIn(primary), FadeIn(secondary), run_time=1)
        self.play(Write(primary_label), Write(secondary_label), run_time=1)
        self.wait(0.375)

        mass_ratio_text = Tex(r"Very unequal masses: mass ratio $q \approx 0.30$",
                               font_size=30, color=HIGHLIGHT_COLOR)
        mass_ratio_text.to_edge(DOWN, buff=1.3)
        self.play(Write(mass_ratio_text), run_time=1.25)
        self.wait(1.25)

        # Spin indicators: spin axis + rotation symbol, fast on the primary, near-static on the secondary
        primary_spin = spin_indicator(primary.get_center(), primary_radius, BH_PRIMARY_COLOR)
        secondary_spin = spin_indicator(secondary.get_center(), secondary_radius, BH_SECONDARY_COLOR)

        self.play(Create(primary_spin), Create(secondary_spin), run_time=1)

        spin_label = Tex(r"The primary spins really fast, with $\chi_1 \approx 0.78$",
                          font_size=28, color=HIGHLIGHT_COLOR)
        spin_label.next_to(mass_ratio_text, DOWN, buff=0.3)
        self.play(Write(spin_label), run_time=1.25)

        primary_tracker = start_spin(primary_spin)
        secondary_tracker = start_spin(secondary_spin)
        self.play(
            primary_tracker.animate.set_value(6),
            secondary_tracker.animate.set_value(0.6),
            run_time=3.75,
            rate_func=linear,
        )
        primary_spin.marker.clear_updaters()
        secondary_spin.marker.clear_updaters()
        self.wait(0.375)

        self.play(
            FadeOut(mass_ratio_text), FadeOut(spin_label),
            FadeOut(primary_label), FadeOut(secondary_label),
            run_time=0.75,
        )

        # Inspiral: circle + spin ring move together, rigidly, toward the merger point
        primary_group = VGroup(primary, primary_spin)
        secondary_group = VGroup(secondary, secondary_spin)

        self.play(
            primary_group.animate.move_to(LEFT * 0.35),
            secondary_group.animate.move_to(RIGHT * 0.35),
            run_time=3.125,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.25)

        self.remove(primary, secondary, primary_spin, secondary_spin)

        remnant = Circle(radius=0.62, color=REMNANT_COLOR, fill_opacity=0.95, stroke_width=0)
        remnant.move_to(ORIGIN)
        self.add(remnant)

        for i in range(4):
            wave = Circle(radius=0.7 + i * 0.35, color=GW_COLOR, fill_opacity=0.15, stroke_width=2)
            wave.move_to(ORIGIN)
            self.play(Create(wave), run_time=0.3125)
            self.remove(wave)

        self.wait(0.625)

        closing = VGroup(
            Tex(r"The perfect combination for testing whether the primary", font_size=30, color=WHITE),
            Tex(r"really was a black hole.", font_size=30, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.2)
        closing.to_edge(DOWN, buff=0.6)
        self.play(Write(closing), run_time=1.875)
        self.wait(2.5)


class SpinInducedQuadrupole(Scene):
    """Scene 2: What kappa is, why a mismatched signal would reveal it, and the measured constraint"""

    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"Is the primary really a black hole?", font_size=64, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=1)
        self.wait(0.625)

        # --- Part 1: what a spin-induced quadrupole moment is ---
        explain1 = Tex(r"Spinning objects bulge at the equator.", font_size=32, color=TEXT_COLOR)
        explain1.next_to(title, DOWN, buff=0.5)
        self.play(Write(explain1), run_time=1.25)

        demo_center = LEFT * 3.3 + DOWN * 0.5
        demo_circle = Circle(radius=0.9, color=WHITE, fill_opacity=0.25, stroke_color=WHITE, stroke_width=3)
        demo_circle.move_to(demo_center)
        demo_spin = spin_indicator(demo_center, 0.9, HIGHLIGHT_COLOR)

        self.play(FadeIn(demo_circle), Create(demo_spin), run_time=1)
        demo_tracker = start_spin(demo_spin)
        self.play(
            demo_tracker.animate.set_value(3),
            demo_circle.animate.stretch(1.35, dim=0).stretch(0.7, dim=1),
            run_time=3.125,
            rate_func=linear,
        )
        demo_spin.marker.clear_updaters()
        self.wait(0.375)

        kappa_intro = VGroup(
            Tex(r"This bulge is the \textbf{spin-induced quadrupole moment},", font_size=28, color=TEXT_COLOR),
            Tex(r"captured by one number: $\kappa$", font_size=28, color=TEXT_COLOR),
            Tex(r"For a black hole, general relativity fixes $\kappa = 1$ exactly.", font_size=28,
                color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.2)
        kappa_intro.move_to(RIGHT * 2.7)
        self.play(Write(kappa_intro), run_time=1.875)
        self.wait(1.875)

        self.play(
            FadeOut(demo_circle), FadeOut(demo_spin), FadeOut(kappa_intro), FadeOut(explain1),
            run_time=0.75,
        )

        # --- Part 2: a mismatched kappa leaves a fingerprint on the waveform ---
        explain2 = Tex(r"A different $\kappa$ changes the shape of the gravitational-wave signal.",
                        font_size=30, color=TEXT_COLOR)
        explain2.next_to(title, DOWN, buff=0.5)
        self.play(Write(explain2), run_time=1.25)

        axes = Axes(
            x_range=[0, 10, 100],
            y_range=[-1.8, 1.8, 100],
            x_length=9.5,
            y_length=3.2,
            axis_config={"include_ticks": False, "color": GREY},
            tips=False,
        )
        axes.move_to(DOWN * 0.6)

        T = 10.0

        def amp(t):
            return 0.22 + 0.85 * (t / T) ** 2

        def phase_gr(t):
            return 2.5 * t + 0.4 * t ** 2

        def dephase(t, K=3.0, p=5):
            return K * (t / T) ** p

        def h_gr(t):
            return amp(t) * np.sin(phase_gr(t))

        def h_exotic(t):
            return amp(t) * np.sin(phase_gr(t) + dephase(t))

        curve_gr = axes.plot(h_gr, x_range=[0, T, 0.01], color=GW_COLOR, stroke_width=3)
        curve_exotic = axes.plot(h_exotic, x_range=[0, T, 0.01], color=EXOTIC_COLOR, stroke_width=3)

        legend_gr = Tex(r"$\kappa = 1$ (matches the data)", font_size=24, color=GW_COLOR)
        legend_exotic = Tex(r"hypothetical $\kappa \gg 1$ (does not)", font_size=24, color=EXOTIC_COLOR)
        legend = VGroup(legend_gr, legend_exotic).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.next_to(axes, UP, buff=0.15).align_to(axes, LEFT)

        caption = Tex(r"(illustrative waveforms)", font_size=20, color=GREY)
        caption.next_to(axes, DOWN, buff=0.15)

        self.play(Create(axes), run_time=0.75)
        self.play(Create(curve_gr), run_time=1.875)
        self.play(Write(legend_gr), run_time=0.75)
        self.wait(0.375)
        self.play(Create(curve_exotic), run_time=1.875)
        self.play(Write(legend_exotic), FadeIn(caption), run_time=0.75)

        mismatch_arrow = Arrow(
            start=axes.c2p(8.7, 1.65), end=axes.c2p(8.8, 1.05), color=WHITE, stroke_width=3, buff=0.05,
        )
        mismatch_label = Tex(r"out of sync near merger", font_size=22, color=WHITE)
        mismatch_label.next_to(mismatch_arrow, UP, buff=0.1)
        self.play(GrowArrow(mismatch_arrow), Write(mismatch_label), run_time=1.25)
        self.wait(1.875)

        self.play(
            *[FadeOut(m) for m in
              [explain2, axes, curve_gr, curve_exotic, legend, caption, mismatch_arrow, mismatch_label]],
            run_time=0.75,
        )

        # --- Part 3: the actual measurement ---
        explain3 = Tex(r"The LIGO-Virgo-KAGRA Collaboration measured $\kappa$.", font_size=34, color=WHITE)
        explain3.next_to(title, DOWN, buff=0.5)
        self.play(Write(explain3), run_time=1)
        self.wait(0.625)

        dist_axes = Axes(
            x_range=[-1.0, 3.5, 0.5],
            y_range=[0, 2.2, 10],
            x_length=8.5,
            y_length=2.8,
            axis_config={"include_ticks": False, "color": GREY},
            tips=False,
        )
        dist_axes.move_to(DOWN * 0.5)

        df = pd.read_hdf(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "production_small_samples.h5"), key="samples")
        kappa_samples = 1.0 + df["dQuadMon1"].dropna()
        kde = scipy.stats.gaussian_kde(kappa_samples)

        def kappa_pdf(k):
            return float(kde(k).item())

        dist_curve = dist_axes.plot(kappa_pdf, x_range=[-1.0, 3.5, 0.05], color=HIGHLIGHT_COLOR, stroke_width=3)
        dist_area = dist_axes.get_area(dist_curve, x_range=(-1.0, 3.5), color=HIGHLIGHT_COLOR, opacity=0.25)

        bh_line = DashedLine(dist_axes.c2p(1.0, 0), dist_axes.c2p(1.0, 2.0), color=WHITE, stroke_width=2)
        bh_label = Tex(r"black hole ($\kappa_1=1$)", font_size=22, color=WHITE)
        bh_label.next_to(dist_axes.c2p(1.0, 2.0), UP, buff=0.1)

        self.play(Create(dist_axes), run_time=0.75)
        self.play(Create(dist_curve), FadeIn(dist_area), run_time=1.5)
        self.play(Create(bh_line), Write(bh_label), run_time=0.75)

        consistent_text = VGroup(
            Tex(r"Consistent with a black hole:", font_size=28, color=WHITE),
            Tex(r"$\kappa_1 = 1.0^{+0.86}_{-0.87}$", font_size=28, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.2)
        consistent_text.next_to(dist_axes, DOWN, buff=0.35)
        self.play(Write(consistent_text), run_time=1.5)
        self.wait(1.875)

        final_note = Tex(r"Precise enough to rule out many proposed alternatives — like boson stars.",
                          font_size=26, color=TEXT_COLOR)
        final_note.next_to(consistent_text, DOWN, buff=0.35)
        self.play(Write(final_note), run_time=1.5)
        self.wait(2.5)


class RepulsiveBosonStarsExcluded(Scene):
    """Scene 3: kappa-chi exclusion for repulsive boson stars, then the mass/coupling plane"""

    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"What if it wasn't a black hole?", font_size=60, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=1)

        intro = VGroup(
            Tex(r"One proposal: \textbf{boson stars} — hypothetical objects made of an", font_size=28,
                color=TEXT_COLOR),
            Tex(r"exotic particle field, held together by gravity alone, no black hole required.",
                font_size=28, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.15)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(Write(intro), run_time=1.875)
        self.wait(1.875)
        self.play(FadeOut(intro), run_time=0.625)

        with open(os.path.join(DATA_DIR, "repulsive_curves.json")) as f:
            rep_data = json.load(f)

        axes = Axes(
            x_range=[0.4, 1.05, 0.1],
            y_range=[-0.2, 1.85, 1],
            x_length=9.5,
            y_length=4.3,
            y_axis_config={"scaling": LogBase(10)},
            axis_config={"include_ticks": False, "color": GREY},
            tips=False,
        )
        axes.move_to(DOWN * 0.3 + LEFT * 0.5)

        x_label = Tex(r"spin $\chi_1$", font_size=26, color=TEXT_COLOR)
        x_label.next_to(axes, DOWN, buff=0.5)
        y_label = Tex(r"$\kappa_1$", font_size=26, color=TEXT_COLOR)
        y_label.next_to(axes, LEFT, buff=0.25)

        explain2 = Tex(r"Repulsive boson stars: how much they'd bulge, for a range of self-interaction strengths",
                        font_size=26, color=TEXT_COLOR)
        explain2.next_to(title, DOWN, buff=0.45)

        self.play(Create(axes), Write(x_label), Write(y_label), Write(explain2), run_time=1.25)

        coupling_items = sorted(rep_data["curves"].items(), key=lambda kv: int(kv[0]))
        curves_group = VGroup()
        legend = VGroup()
        for (lam, pts), color in zip(coupling_items, COUPLING_COLORS):
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            graph = axes.plot_line_graph(xs, ys, line_color=color, add_vertex_dots=False, stroke_width=3)
            curves_group.add(graph)
            legend.add(Tex(rf"$\lambda/\mu^2={lam}$", font_size=20, color=color))

        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(axes, RIGHT, buff=0.3)

        self.play(*[Create(g) for g in curves_group], run_time=3.125)
        self.play(Write(legend), run_time=1.25)
        self.wait(1.25)

        blob_pts = [(p[0], max(p[1], 10**-0.2)) for p in rep_data["blob"]]
        blob_screen = [axes.c2p(x, y) for x, y in blob_pts]
        blob = Polygon(*blob_screen, color=HIGHLIGHT_COLOR, fill_color=HIGHLIGHT_COLOR,
                        fill_opacity=0.35, stroke_width=2)

        blob_label = Tex(r"measured $\kappa_1,\chi_1$", font_size=22, color=HIGHLIGHT_COLOR)
        blob_label.move_to(axes.c2p(0.62, 1.9))

        self.play(FadeIn(blob), Write(blob_label), run_time=1.25)
        self.wait(1.875)

        conclusion = Tex(r"No coupling gets close — repulsive boson stars are excluded entirely.",
                          font_size=28, color=WHITE)
        conclusion.next_to(x_label, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.25)
        self.wait(2.5)


class SolitonicStarsAllowed(Scene):
    """Scene 4: solitonic/axionic boson stars survive; general compactness threshold"""

    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"But some boson stars survive", font_size=60, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=1)

        intro = Tex(r"It depends on how \textbf{compact} they can get.", font_size=30, color=TEXT_COLOR)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(Write(intro), run_time=1.25)
        self.wait(1.25)
        self.play(FadeOut(intro), run_time=0.625)

        with open(os.path.join(DATA_DIR, "solitonic_axionic_efs_curves.json")) as f:
            data = json.load(f)
        sol = data["solitonic"]

        axes = Axes(
            x_range=[0.4, 1.1, 0.1],
            y_range=[-0.25, 1.3, 1],
            x_length=9.5,
            y_length=3.8,
            y_axis_config={"scaling": LogBase(10)},
            axis_config={"include_ticks": False, "color": GREY},
            tips=False,
        )
        axes.move_to(DOWN * 0.15 + LEFT * 0.5)

        x_label = Tex(r"spin $\chi_1$", font_size=26, color=TEXT_COLOR)
        x_label.next_to(axes, DOWN, buff=0.5)
        y_label = Tex(r"$\kappa_1$", font_size=26, color=TEXT_COLOR)
        y_label.next_to(axes, LEFT, buff=0.25)

        explain = Tex(r"Solitonic boson stars, for a range of self-interaction strengths $\sigma$",
                      font_size=26, color=TEXT_COLOR)
        explain.next_to(title, DOWN, buff=0.45)

        self.play(Create(axes), Write(x_label), Write(y_label), Write(explain), run_time=1.25)

        coupling_items = sorted(sol["curves"].items(), key=lambda kv: float(kv[0]))[:4]
        curves_group = VGroup()
        legend = VGroup()
        for (sigma, pts), color in zip(coupling_items, COUPLING_COLORS):
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            graph = axes.plot_line_graph(xs, ys, line_color=color, add_vertex_dots=False, stroke_width=3)
            curves_group.add(graph)
            legend.add(Tex(rf"$\sigma={sigma}$", font_size=20, color=color))

        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(axes, RIGHT, buff=0.3)

        self.play(*[Create(g) for g in curves_group], run_time=3.125)
        self.play(Write(legend), run_time=1.25)
        self.wait(1.25)

        blob_pts = [(p[0], max(p[1], 10**-0.25)) for p in sol["blob"]]
        blob_screen = [axes.c2p(x, y) for x, y in blob_pts]
        blob = Polygon(*blob_screen, color=HIGHLIGHT_COLOR, fill_color=HIGHLIGHT_COLOR,
                        fill_opacity=0.35, stroke_width=2)
        blob_label = Tex(r"measured $\kappa_1,\chi_1$", font_size=22, color=HIGHLIGHT_COLOR)
        blob_label.next_to(blob, UP, buff=0.15)

        self.play(FadeIn(blob), Write(blob_label), run_time=1.25)
        self.wait(1.25)

        highlight_note = Tex(r"weaker coupling ($\sigma \lesssim 0.1$): passes right through the measured region",
                              font_size=24, color=HIGHLIGHT_COLOR)
        highlight_note.next_to(x_label, DOWN, buff=0.3)
        self.play(Write(highlight_note), run_time=1.25)
        self.wait(1.875)

        also_note = Tex(r"(axionic boson stars show the same pattern, for weak enough coupling)",
                         font_size=20, color=GREY)
        also_note.next_to(highlight_note, DOWN, buff=0.15)
        self.play(FadeIn(also_note), run_time=0.75)
        self.wait(2.5)


class ClosingSummary(Scene):
    """Scene 5: final one-to-two sentence summary tying the whole story together"""

    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"GW241011", font_size=60, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=1)

        remnant = Circle(radius=0.5, color=REMNANT_COLOR, fill_opacity=0.95, stroke_width=0)
        remnant.move_to(UP * 1.5)
        self.play(FadeIn(remnant), run_time=1)
        self.wait(0.375)

        summary = VGroup(
            Tex(r"GW241011 rules out a large set of spinning", font_size=32, color=WHITE),
            Tex(r"exotic compact objects as explanations", font_size=32, color=WHITE),
            Tex(r"for its primary object.", font_size=32, color=WHITE),
            Tex(r"Models of exotic objects with high compactness", font_size=32, color=HIGHLIGHT_COLOR),
            Tex(r"$\gtrsim 0.24$ are still consistent with data.", font_size=32, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.25)
        summary.next_to(remnant, DOWN, buff=0.6)

        self.play(Write(summary), run_time=3.125)
        self.wait(3.75)
