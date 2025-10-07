"""
Manim scene(s) that visualize a Brownian motion / random walk.

Usage (Manim Community):
    manim -pql brownian_motion.py BrownianMotion

Adjust parameters inside the scene (n_steps, sigma, scale, run_time) to change the simulation.
"""
from manim import *
import numpy as np


class BrownianMotion(Scene):
    """A single-particle 2D Brownian motion / random walk with a trailing path."""

    def construct(self):
        # Parameters
        np.random.seed(1)
        n_steps = 1000          # number of discrete steps in the random walk
        sigma = 0.06            # step-size standard deviation (in normalized units)
        scale = 6.0             # visual scale factor to make motion visible in the scene
        run_time = 12           # seconds to animate the whole walk

        # Generate a 2D random walk (Gaussian steps)
        steps = np.random.normal(loc=0.0, scale=sigma, size=(n_steps, 2))
        positions_2d = np.cumsum(steps, axis=0)
        # Insert the origin as the starting point
        positions = [np.array([0.0, 0.0, 0.0])] + [np.array([x * scale, y * scale, 0.0]) for x, y in positions_2d]

        # ValueTracker drives the animation index
        index = ValueTracker(0)

        # Moving dot
        particle = Dot(point=positions[0], color=YELLOW)
        particle.add_updater(lambda m: m.move_to(positions[int(index.get_value())]))

        # Trailing path (VMobject updated each frame to include points up to current index)
        trail = VMobject()
        trail.set_stroke(color=BLUE, width=2, opacity=0.9)

        def update_trail(mob):
            idx = int(index.get_value())
            if idx < 1:
                mob.set_points_as_corners([positions[0], positions[0]])
            else:
                mob.set_points_as_corners(positions[: idx + 1])

        trail.add_updater(update_trail)

        # Optionally add axes for reference
        axes = Axes(x_range=[-10, 10, 2], y_range=[-6, 6, 2], axis_config={"include_tip": False, "stroke_opacity": 0.4})
        axes.shift(LEFT * 0.5)

        self.add(axes, trail, particle)

        # Animate index from 0 -> n_steps
        self.play(index.animate.set_value(len(positions) - 1), run_time=run_time, rate_func=linear)
        self.wait(1)


class MultiBrownian(Scene):
    """Multiple independent Brownian particles shown together with short trails."""

    def construct(self):
        np.random.seed(2)
        n_particles = 30
        n_steps = 400
        sigma = 0.08
        scale = 4.0
        run_time = 10

        all_positions = []
        for i in range(n_particles):
            steps = np.random.normal(loc=0.0, scale=sigma, size=(n_steps, 2))
            pos2d = np.cumsum(steps, axis=0)
            positions = [np.array([0.0, 0.0, 0.0])] + [np.array([x * scale, y * scale, 0.0]) for x, y in pos2d]
            all_positions.append(positions)

        index = ValueTracker(0)

        particles = VGroup()
        trails = VGroup()
        colors = color_gradient([BLUE, TEAL, PURPLE, PINK, YELLOW], n_particles)

        for i in range(n_particles):
            p = Dot(point=all_positions[i][0], color=colors[i], radius=0.06)
            t = VMobject()
            t.set_stroke(color=colors[i], width=2, opacity=0.8)

            def make_dot_updater(dot, positions):
                return lambda m: m.move_to(positions[int(index.get_value())])

            def make_trail_updater(trail, positions):
                def _up(tr):
                    idx = int(index.get_value())
                    if idx < 1:
                        tr.set_points_as_corners([positions[0], positions[0]])
                    else:
                        tr.set_points_as_corners(positions[: idx + 1])
                return _up

            p.add_updater(make_dot_updater(p, all_positions[i]))
            t.add_updater(make_trail_updater(t, all_positions[i]))
            particles.add(p)
            trails.add(t)

        axes = Axes(x_range=[-10, 10, 2], y_range=[-6, 6, 2], axis_config={"include_tip": False, "stroke_opacity": 0.4})

        self.add(axes, trails, particles)
        self.play(index.animate.set_value(n_steps), run_time=run_time, rate_func=linear)
        self.wait(1)
