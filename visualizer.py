import pygame
import numpy as np
import random


class Visualizer:

    def __init__(self, width, height):

        self.w = width
        self.h = height

        self.particles = []


    # ----------------------------
    # PARTICLES (music reactive)
    # ----------------------------

    def update_particles(self, bass, mids):

        intensity = bass + mids

        # spawn particles on beat energy
        if intensity > 0.25:

            for _ in range(int(1 + intensity * 6)):

                self.particles.append([

                    random.randint(320, self.w - 50),
                    self.h // 2,

                    random.uniform(-2.5, 2.5),
                    random.uniform(-6, -1),

                    random.randint(2, 5),   # size
                    random.uniform(0.7, 1.0) # life
                ])

        alive = []

        for p in self.particles:

            p[0] += p[2]
            p[1] += p[3]

            p[5] -= 0.02

            if p[5] > 0:
                alive.append(p)

        self.particles = alive


    # ----------------------------
    # SPECTRUM (Spotify bars)
    # ----------------------------

    def draw_spectrum(self, screen, samples):

        if len(samples) < 128:
            return

        try:
            samples = samples.astype(np.float32)

            # stereo → mono safety
            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            fft = np.fft.rfft(samples)
            mag = np.abs(fft)

            bars = 60
            chunk = max(1, len(mag) // bars)

            x_start = 320
            y_base = self.h - 170

            bar_w = 8
            spacing = 5

            for i in range(bars):

                start = i * chunk
                end = start + chunk

                value = np.mean(mag[start:end])

                height = int(min(260, value / 250))

                x = x_start + i * (bar_w + spacing)

                # gradient green
                color = (
                    30,
                    min(255, 120 + i * 2),
                    90
                )

                pygame.draw.rect(
                    screen,
                    color,
                    (x, y_base - height, bar_w, height),
                    border_radius=3
                )

        except Exception as e:
            print("Spectrum error:", e)


    # ----------------------------
    # WAVEFORM (main visual)
    # ----------------------------

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        try:

            samples = samples.astype(np.float32)

            # stereo → mono safety
            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            center_y = self.h // 2

            width_area = self.w - 320

            step = max(1, len(samples) // width_area)

            points = []

            reaction = 1 + bass * 4 + mids * 2

            for x in range(width_area):

                idx = x * step

                if idx >= len(samples):
                    break

                amp = (samples[idx] / 32768) * reaction

                y = center_y + int(
                    amp * (160 + bass * 250)
                )

                points.append((320 + x, y))

            glow = int(120 + bass * 120)
            thickness = int(2 + bass * 8)

            if len(points) > 1:

                # outer glow
                pygame.draw.lines(
                    screen,
                    (40, glow, 120),
                    False,
                    points,
                    thickness + 8
                )

                # mid glow
                pygame.draw.lines(
                    screen,
                    (90, 255, 180),
                    False,
                    points,
                    thickness + 4
                )

                # core line
                pygame.draw.lines(
                    screen,
                    (29, 185, 84),
                    False,
                    points,
                    thickness
                )

            # spectrum bars
            self.draw_spectrum(screen, samples)

            # particles
            self.update_particles(bass, mids)

            for p in self.particles:

                pygame.draw.circle(
                    screen,
                    (29, 185, 84),
                    (int(p[0]), int(p[1])),
                    int(p[4])
                )

        except Exception as e:
            print("Visualizer error:", e)