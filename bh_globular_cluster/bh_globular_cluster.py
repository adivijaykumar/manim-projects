from manim import *
import numpy as np

class MassSegregation(Scene):
    """Scene 1: Mass segregation in globular cluster"""
    def construct(self):
        self.camera.background_color = "#000000"

        # Title with better styling
        title = Tex(r"Mass Segregation", font_size=80, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Create cluster with many particles
        np.random.seed(42)
        cluster_radius = 5
        n_light = 300  # 2x increase in light objects
        n_heavy = 50

        all_particles = []
        light_particles = []
        heavy_particles = []

        # Generate the SAME distribution of positions for both populations
        # Heavy particles: sample from same distribution as light, but fewer of them
        heavy_positions = []
        for i in range(n_heavy):
            r = np.random.uniform(0.5, cluster_radius)
            theta = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            heavy_positions.append((x, y))

        # Light particles: same distribution
        light_positions = []
        for i in range(n_light):
            r = np.random.uniform(0.5, cluster_radius)
            theta = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            light_positions.append((x, y))

        # Create heavy particles (initially at same distribution as light)
        for x, y in heavy_positions:
            circle = Circle(radius=0.14, color="#ff6b6b", fill_opacity=0.85)
            circle.move_to([x, y, 0])
            heavy_particles.append((circle, (x, y)))
            all_particles.append(circle)
            self.add(circle)

        # Create light particles (initially at same distribution)
        for x, y in light_positions:
            circle = Circle(radius=0.06, color="#4a90e2", fill_opacity=0.5)
            circle.move_to([x, y, 0])
            light_particles.append((circle, (x, y)))
            all_particles.append(circle)
            self.add(circle)

        self.wait(1)

        # # Explanation text
        # explanation = Tex(r"Mass segregation through dynamical interactions",
        #                   font_size=36, color="#e0e0e0")
        # explanation.next_to(title, DOWN, buff=0.5)
        # self.add(explanation)

        self.wait(1)

        # Animate transition to intermediate segregation stage
        # time_label = Tex(r"Intermediate time", font_size=32, color="#ffff99")
        # time_label.to_edge(DOWN, buff=0.5)
        # self.add(time_label)

        animations = []

        # Heavy particles move to intermediate positions (inward)
        for circle, (x, y) in heavy_particles:
            target_x = x * 0.35  # Intermediate position towards center
            target_y = y * 0.35
            animations.append(circle.animate.move_to([target_x, target_y, 0]))

        # Light particles move outward within same cluster bounds (r=0.5 to 5.0)
        for circle, (x, y) in light_particles:
            magnitude = np.sqrt(x**2 + y**2)
            if magnitude > 0.1:
                direction_x = x / magnitude
                direction_y = y / magnitude
            else:
                theta = np.random.uniform(0, 2*np.pi)
                direction_x = np.cos(theta)
                direction_y = np.sin(theta)

            # Move outward while keeping maximum at cluster boundary (5.0)
            # Scale to new radius: r_initial maps to larger radius but capped at 5.0
            # r=0.5 → 0.9, r=2.5 → 3.2, r=5.0 → 5.0
            new_radius = 0.4 + magnitude * 0.92  # Linear mapping keeping max at 5.0
            target_x = direction_x * new_radius
            target_y = direction_y * new_radius
            animations.append(circle.animate.move_to([target_x, target_y, 0]))

        # Animate the transition process (this is the key!)
        self.play(*animations, run_time=5)
        self.wait(1)

        # Add final annotations
        # self.remove(time_label)
        center_text = Tex(r"Dense core of\\heavy objects", font_size=32, color="#ff6b6b")
        center_text.move_to([0, -3.5, 0])
        self.add(center_text)

        edge_text = Tex(r"Low mass objects\\escaped to edges", font_size=32, color="#4a90e2")
        edge_text.move_to([4, 3.5, 0])
        self.add(edge_text)

        self.wait(2)


class EqualMassRatioMergers(Scene):
    """Scene 2: Zoom into dense core and show 1:1 black hole merger"""
    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"$\mathrm{1G}+\mathrm{1G}$ Black Hole Mergers", font_size=80, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        explanation = Tex(r"Mass ratio = 1. Remnant has a unique spin value of $\approx 0.7$",
                          font_size=32, color="#e0e0e0")
        explanation.next_to(title, DOWN, buff=0.4)
        self.add(explanation)

        self.wait(1)

        # Show dense core of black holes - SMALL initially (for zoom effect)
        np.random.seed(42)
        core_bhs = []

        # Create ~20 black holes in dense core (initially small for zoom)
        for i in range(50):
            r = np.random.uniform(0.1, 0.8)
            theta = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            bh = Circle(radius=0.08, color="#ff6b6b", fill_opacity=0.8)  # Small initially
            bh.move_to([x, y, 0])
            core_bhs.append(bh)
            self.add(bh)

        zoom_label = Tex(r"Zooming into dense core...", font_size=28, color="#ffff99")
        zoom_label.move_to([0, -3, 0])
        self.add(zoom_label)

        self.wait(1)

        # ZOOM IN ANIMATION - Scale AND move objects outward to fill screen
        zoom_animations = []
        for bh in core_bhs:
            current_pos = bh.get_center()
            # Move objects outward from center AND scale them up
            new_x = current_pos[0] * 2.75  # Scale position outward
            new_y = current_pos[1] * 2.75

            zoom_animations.append(bh.animate.scale(2.75))  # Scale size
            zoom_animations.append(bh.animate.move_to([new_x, new_y, 0]))  # Move outward

        self.play(*zoom_animations, run_time=2)

        self.remove(zoom_label)
        self.wait(1)

        # Highlight and merge two specific BHs
        self.remove(zoom_label)

        bh_1_idx = 3
        bh_2_idx = 14
        bh_1 = core_bhs[bh_1_idx]
        bh_2 = core_bhs[bh_2_idx]

        # Add highlighting to selected BHs
        highlight1 = Circle(radius=0.28, color="#ffff00", fill_opacity=0, stroke_color="#ffff00", stroke_width=3)
        highlight1.move_to(bh_1.get_center())
        highlight2 = Circle(radius=0.28, color="#ffff00", fill_opacity=0, stroke_color="#ffff00", stroke_width=3)
        highlight2.move_to(bh_2.get_center())

        self.add(highlight1, highlight2)

        # annotation = Tex(r"1G+1G Merger: $M + M$ (mass ratio = 1)", font_size=32, color="#ffff00")
        # annotation.to_edge(DOWN, buff=0.5)
        # self.add(annotation)

        self.wait(1.5)

        # Animate the two selected BHs toward center for merger
        merger_point = [0, 0, 0]

        self.play(
            bh_1.animate.move_to(merger_point),
            bh_2.animate.move_to(merger_point),
            highlight1.animate.move_to(merger_point),
            highlight2.animate.move_to(merger_point),
            run_time=2
        )

        self.wait(0.5)

        # Remove the merging BHs and highlights
        self.remove(bh_1, bh_2, highlight1, highlight2)

        # Create merged result (2M black hole with spin)
        result_bh = Circle(radius=0.28, color="#ff8c42", fill_opacity=0.9)
        result_bh.move_to(merger_point)

        self.add(result_bh)

        # Gravitational wave ripples from merger
        for i in range(3):
            wave = Circle(radius=0.35 + i*0.3, color="#4a90e2", fill_opacity=0.15)
            wave.move_to(merger_point)
            self.play(Create(wave), run_time=0.3)
            self.remove(wave)

        self.wait(0.5)

        # Remove old annotation and add result details
        # self.remove(annotation)

        result_properties = VGroup(
            Tex(r"Result: 2G Black Hole", font_size=28, color="#ff8c42"),
            Tex(r"Mass $\approx 2M$", font_size=28, color=WHITE),
            Tex(r"Spin $\chi \approx 0.7$ [Unique value for such mergers]", font_size=28, color="#ffff99")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        result_properties.to_edge(DOWN, buff=0.3)

        self.play(Write(result_properties), run_time=1)

        self.wait(2)


class SecondGenerationBH(Scene):
    """Scene 3: 2G black hole merges with 1G black hole"""
    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"$\mathrm{2G} + \mathrm{1G}$ Merger", font_size=80, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        explanation = Tex(r"Second generation ($2M,\, \chi \approx 0.7$) black hole merges with first-generation ($M$) black hole",
                          font_size=32, color="#e0e0e0")
        explanation.next_to(title, DOWN, buff=0.4)
        self.add(explanation)

        self.wait(1)

        # 2G Black hole at center
        bh_2g = Circle(radius=0.4, color="#ff8c42", fill_opacity=0.95)
        bh_2g.move_to([0, 0, 0])
        label_2g = Tex(r"$2M$", font_size=32, color=WHITE)
        label_2g.move_to([0, 0, 0])

        self.add(bh_2g, label_2g)

        # Spin annotation
        spin_label = Tex(r"Spin $\chi \approx 0.7$", font_size=32, color="#ffff99")
        spin_label.move_to([-2, -1.5, 0])
        self.add(spin_label)

        self.wait(1)

        # 1G black hole approaches from right
        bh_1g = Circle(radius=0.22, color="#ff6b6b", fill_opacity=0.85)
        bh_1g.move_to([3, 0.5, 0])
        label_1g = Tex(r"$M$", font_size=32, color=WHITE)
        label_1g.move_to([3, 0.5, 0])

        self.add(bh_1g, label_1g)

        # Mass ratio annotation
        mass_ratio_box = VGroup(
            Tex(r"Mass Ratio = 0.5", font_size=32, color="#ff8c42"),
            # Tex(r"(smaller: larger)", font_size=24, color="#e0e0e0")
        ).arrange(DOWN, buff=0.1)
        mass_ratio_box.move_to([2, -2, 0])
        self.add(mass_ratio_box)

        self.wait(1)

        # 1G BH spirals in toward 2G BH
        self.play(
            bh_1g.animate.move_to([0, 0, 0]),
            label_1g.animate.move_to([0, 0, 0]),
            run_time=2.5
        )

        self.wait(0.5)

        # Merger happens
        self.remove(bh_1g, label_1g)

        # Result: 3M black hole
        result_bh = Circle(radius=0.48, color="#e84c3d", fill_opacity=0.95)
        result_bh.move_to([0, 0, 0])
        result_label = Tex(r"$\approx 3M$", font_size=32, color=WHITE)
        result_label.move_to([0, 0, 0])

        self.add(result_bh, result_label)

        # Gravitational waves from merger
        for i in range(3):
            wave = Circle(radius=0.5 + i*0.3, color="#4a90e2", fill_opacity=0.15)
            wave.move_to([0, 0, 0])
            self.play(Create(wave), run_time=0.3)
            self.remove(wave)

        self.wait(1)

        # Result summary
        result_summary = VGroup(
            Tex(r"$2M + M \to \approx 3M$", font_size=36, color="#e84c3d"),
            Tex(r"Unequal-mass merger", font_size=32, color="#e0e0e0")
        ).arrange(DOWN, buff=0.15)
        result_summary.to_edge(DOWN, buff=0.5)

        self.play(Write(result_summary), run_time=1)
        self.wait(2)


class SecondGenerationBH_v2(Scene):
    """Scene 3 (Alternative): Starts from Scene 2 end, 2M BH merges with 1G, others fade"""
    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"$\mathrm{2G} + \mathrm{1G}$ Black Hole Mergers", font_size=80, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        explanation = Tex(r"Mass Ratio = 0.5; $\chi_1 \approx 0.7$",
                          font_size=32, color="#e0e0e0")
        explanation.next_to(title, DOWN, buff=0.4)
        self.add(explanation)

        self.wait(1)

        # Recreate the exact end-of-Scene-2 configuration
        # Create the same 50 BHs as Scene 2, zoomed in
        np.random.seed(42)
        core_bhs = []

        for i in range(50):
            r = np.random.uniform(0.1, 0.8)
            theta = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # Apply zoom transformation (same as Scene 2): 2.75x scale on positions
            x_zoomed = x * 2.75
            y_zoomed = y * 2.75

            bh = Circle(radius=0.08, color="#ff6b6b", fill_opacity=0.8)  # Pre-zoom size to match Scene 2 visually
            bh.move_to([x_zoomed, y_zoomed, 0])
            core_bhs.append(bh)
            self.add(bh)

        # 2M black hole at center (result from Scene 2)
        bh_2g = Circle(radius=0.28, color="#ff8c42", fill_opacity=0.9)
        bh_2g.move_to([0, 0, 0])
        label_2g = Tex(r"$2M$", font_size=32, color=WHITE)
        label_2g.move_to([0, 0, 0])

        self.add(bh_2g, label_2g)

        # Spin annotation
        # spin_label = Tex(r"Spin $\chi \approx 0.7$", font_size=32, color="#ffff99")
        # spin_label.move_to([-2, -1.5, 0])
        # self.add(spin_label)

        self.wait(1.5)

        # Select one specific BH to merge (same indices as Scene 2)
        target_idx = 22
        target_bh = core_bhs[target_idx]
        target_bh.set_color("#ffff00")

        annotation = Tex(r"Next merger: $2M + M$", font_size=32, color="#ffff00")
        annotation.to_edge(DOWN, buff=0.5)
        self.add(annotation)

        self.wait(1)

        # Fade out all other BHs while selected one merges
        fade_animations = []
        for i, bh in enumerate(core_bhs):
            if i != target_idx:
                fade_animations.append(bh.animate.set_opacity(0))

        # Move selected BH toward center for merger
        fade_animations.append(target_bh.animate.move_to([0, 0, 0]))
        fade_animations.append(annotation.animate.set_opacity(0))

        self.play(*fade_animations, run_time=2.5)

        self.wait(0.5)

        # Remove the merging BH
        self.remove(target_bh)
        for bh in core_bhs:
            self.remove(bh)
        self.remove(annotation)

        # Result: ~3M black hole
        result_bh = Circle(radius=0.48, color="#e84c3d", fill_opacity=0.95)
        result_bh.move_to([0, 0, 0])
        result_label = Tex(r"$\approx 3M$", font_size=32, color=WHITE)
        result_label.move_to([0, 0, 0])

        self.add(result_bh, result_label)

        # Gravitational waves from merger
        for i in range(3):
            wave = Circle(radius=0.5 + i*0.3, color="#4a90e2", fill_opacity=0.15)
            wave.move_to([0, 0, 0])
            self.play(Create(wave), run_time=0.3)
            self.remove(wave)

        self.wait(1)

        # Result summary
        result_properties = VGroup(
            Tex(r"Result: 3G Black Hole", font_size=32, color="#ff8c42"),
            Tex(r"Mass $\approx 3M$", font_size=28, color=WHITE),
            # Tex(r"Spin $\chi \approx 0.7$", font_size=28, color="#ffff99")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        result_properties.to_edge(DOWN, buff=0.3)

        self.play(Write(result_properties), run_time=1)

        self.wait(2)

class SecondGenerationMerger(Scene):
    """Scene 4: 2G BH merges with 1G BHs (2M:M ratio)"""
    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"\mathrm{2G} + \mathrm{1G} Merger", font_size=60, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        explanation = Tex(r"The 2G black hole merges with first-generation black holes",
                          font_size=26, color="#e0e0e0")
        explanation.next_to(title, DOWN, buff=0.4)
        self.add(explanation)

        # Center: the 2G black hole
        bh_2g = Circle(radius=0.45, color="#ff8c42", fill_opacity=0.95)
        bh_2g.move_to([0, 0, 0])
        label_2g = Tex(r"2M", font_size=20, color=WHITE)
        label_2g.move_to([0, 0, 0])

        self.add(bh_2g, label_2g)
        self.wait(1)

        # Show multiple 1G BHs approaching
        mass_ratio_text = Tex(r"Mass ratio: 1:2", font_size=20, color="#ffff99")
        mass_ratio_text.next_to(title, DOWN, buff=0.5)
        self.add(mass_ratio_text)

        # Merger 1: from right
        bh_1g_right = Circle(radius=0.25, color="#ff6b6b", fill_opacity=0.85)
        bh_1g_right.move_to([4, 0.5, 0])
        label_1g_right = Tex(r"M", font_size=18, color=WHITE)
        label_1g_right.move_to([4, 0.5, 0])

        self.add(bh_1g_right, label_1g_right)

        # Spiral in
        self.play(
            bh_1g_right.animate.move_to([0, 0, 0]),
            label_1g_right.animate.move_to([0, 0, 0]),
            run_time=2.5
        )

        # Merger animation
        self.play(bh_1g_right.animate.set_opacity(0.2), run_time=0.8)

        # GW from merger
        for i in range(3):
            wave = Circle(radius=0.6 + i*0.25, color="#4a90e2", fill_opacity=0.15)
            wave.move_to([0, 0, 0])
            self.play(Create(wave), run_time=0.3)
            self.remove(wave)

        self.remove(bh_1g_right, label_1g_right)
        self.wait(0.5)

        # Merger 2: from left
        bh_1g_left = Circle(radius=0.25, color="#ff6b6b", fill_opacity=0.85)
        bh_1g_left.move_to([-4, -0.5, 0])
        label_1g_left = Tex(r"M", font_size=18, color=WHITE)
        label_1g_left.move_to([-4, -0.5, 0])

        self.add(bh_1g_left, label_1g_left)

        self.play(
            bh_1g_left.animate.move_to([0, 0, 0]),
            label_1g_left.animate.move_to([0, 0, 0]),
            run_time=2.5
        )

        self.play(bh_1g_left.animate.set_opacity(0.2), run_time=0.8)

        for i in range(3):
            wave = Circle(radius=0.6 + i*0.25, color="#4a90e2", fill_opacity=0.15)
            wave.move_to([0, 0, 0])
            self.play(Create(wave), run_time=0.3)
            self.remove(wave)

        self.remove(bh_1g_left, label_1g_left)
        self.wait(0.5)

        # Result grows larger
        bh_result = Circle(radius=0.55, color="#e84c3d", fill_opacity=0.95)
        bh_result.move_to([0, 0, 0])
        label_result = Tex(r"~4M", font_size=20, color=WHITE)
        label_result.move_to([0, 0, 0])

        self.remove(bh_2g, label_2g)
        self.add(bh_result, label_result)

        result_text = Tex(r"Hierarchy of increasingly massive remnants",
                          font_size=20, color="#ffff99")
        result_text.to_edge(DOWN, buff=0.5)
        self.play(Write(result_text), run_time=1)

        self.wait(2)


class Summary(Scene):
    """Final summary scene"""
    def construct(self):
        self.camera.background_color = "#000000"

        title = Tex(r"Black Hole Merger Hierarchy", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        summary_steps = VGroup(
            Tex(r"① Mass segregation of stellar-mass black holes",
                 font_size=20, color="#e0e0e0"),
            Tex(r"② Repeated 1:1 mergers in the dense core",
                 font_size=20, color="#e0e0e0"),
            Tex(r"③ Formation of ~2M second-generation black hole",
                 font_size=20, color="#ff8c42"),
            Tex(r"    with unique spin parameter a ≈ 0.7",
                 font_size=18, color="#ffff99"),
            Tex(r"④ 2G BH becomes dynamically most active",
                 font_size=20, color="#e0e0e0"),
            Tex(r"⑤ Rapid 2M:M mergers with 1G black holes",
                 font_size=20, color="#e0e0e0"),
            Tex(r"⑥ Chain of increasingly massive remnants",
                 font_size=20, color="#ffff99"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        summary_steps.move_to(ORIGIN).shift(UP * 0.5)

        for step in summary_steps:
            self.play(Write(step), run_time=0.6)
            self.wait(0.2)

        self.wait(2)


if __name__ == "__main__":
    # Render with: manim -pql bh_globular_cluster.py
    pass
