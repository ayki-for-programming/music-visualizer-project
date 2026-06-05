import pygame
import numpy as np
import random


class Visualizer:

    def __init__(self, width, height):

        self.w = width
        self.h = height

        self.particles = []

    # ------------------
    # PARTICLES
    # ------------------

    def update_particles(self, bass):

        if bass > 0.25:

            for _ in range(3):

                self.particles.append(

                    [
                        random.randint(
                            300,
                            self.w - 100
                        ),

                        self.h // 2,

                        random.uniform(
                            -2,
                            2
                        ),

                        random.uniform(
                            -4,
                            -1
                        ),

                        random.randint(
                            2,
                            5
                        )
                    ]
                )

        alive = []

        for p in self.particles:

            p[0] += p[2]
            p[1] += p[3]

            p[4] -= 0.03

            if p[4] > 0:

                alive.append(p)

        self.particles = alive

    # ------------------
    # SPECTRUM
    # ------------------

    def draw_spectrum(
        self,
        screen,
        samples
    ):

        if len(samples) < 256:
            return

        try:

            samples = samples.astype(
                np.float32
            )

            fft = np.fft.rfft(samples)

            mag = np.abs(fft)

            bars = 64

            chunk = max(
                1,
                len(mag) // bars
            )

            start_x = 320

            width = 10

            spacing = 5

            for i in range(bars):

                begin = i * chunk
                end = begin + chunk

                value = np.mean(
                    mag[begin:end]
                )

                height = min(
                    250,
                    int(value / 300)
                )

                x = start_x + (
                    i * (
                        width + spacing
                    )
                )

                y = self.h - 180

                color = (
                    30,
                    min(
                        255,
                        180 + i
                    ),
                    96
                )

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        x,
                        y - height,
                        width,
                        height
                    ),
                    border_radius=3
                )

        except:
            pass

    # ------------------
    # WAVEFORM
    # ------------------

    def draw_wave(
        self,
        screen,
        samples,
        bass
    ):

        if len(samples) < 10:
            return

        try:

            samples = samples.astype(
                np.float32
            )

            center_y = (
                self.h // 2
            )

            step = max(
                1,
                len(samples) // (
                    self.w - 300
                )
            )

            points = []

            start_x = 300

            for x in range(
                self.w - 320
            ):

                idx = x * step

                if idx >= len(samples):
                    break

                amp = (
                    samples[idx]
                    / 32768
                )

                y = (
                    center_y
                    + int(
                        amp * 180
                    )
                )

                points.append(
                    (
                        start_x + x,
                        y
                    )
                )

            glow = int(
                120 + bass * 100
            )

            thickness = int(
                2 + bass * 10
            )

            if len(points) > 1:

                pygame.draw.lines(
                    screen,
                    (
                        40,
                        glow,
                        120
                    ),
                    False,
                    points,
                    thickness + 8
                )

                pygame.draw.lines(
                    screen,
                    (
                        100,
                        255,
                        180
                    ),
                    False,
                    points,
                    thickness + 4
                )

                pygame.draw.lines(
                    screen,
                    (
                        29,
                        185,
                        84
                    ),
                    False,
                    points,
                    thickness
                )

            self.draw_spectrum(
                screen,
                samples
            )

            self.update_particles(
                bass
            )

            for p in self.particles:

                pygame.draw.circle(

                    screen,

                    (
                        29,
                        185,
                        84
                    ),

                    (
                        int(p[0]),
                        int(p[1])
                    ),

                    int(p[4])
                )

        except Exception as e:

            print(
                "Visualizer error:",
                e
            )