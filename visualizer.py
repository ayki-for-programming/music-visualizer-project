import pygame
import numpy as np
import random


class Visualizer:

    def __init__(self, width, height):

        self.w = width
        self.h = height

        self.particles = []


    # ----------------------------
    # PARTICLES (red/pink glow)
    # ----------------------------

    def update_particles(self, bass, mids):

        intensity = bass + mids

        if intensity > 0.25:

            for _ in range(int(1 + intensity * 5)):

                self.particles.append([

                    random.randint(self.w // 2 - 250, self.w // 2 + 250),
                    self.h // 2,

                    random.uniform(-2.2, 2.2),
                    random.uniform(-5, -1),

                    random.randint(2, 5),
                    random.uniform(0.7, 1.0)
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
    # SPECTRUM (red/pink bars)
    # ----------------------------

    def draw_spectrum(self, screen, samples, rect):

        if len(samples) < 128:
            return

        try:

            samples = samples.astype(np.float32)

            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            fft = np.fft.rfft(samples)
            mag = np.abs(fft)

            bars = 55
            chunk = max(1, len(mag) // bars)

            x_start = rect.x + 40
            y_base = rect.y + rect.height - 40

            bar_w = 6
            spacing = 4

            for i in range(bars):

                start = i * chunk
                end = start + chunk

                value = np.mean(mag[start:end])

                height = int(min(220, value / 300))

                x = x_start + i * (bar_w + spacing)

                # red → pink gradient
                color = (
                    min(255, 180 + i * 2),
                    40,
                    min(255, 120 + i * 3)
                )

                pygame.draw.rect(
                    screen,
                    color,
                    (x, y_base - height, bar_w, height),
                    border_radius=3
                )

        except:
            pass


    # ----------------------------
    # WAVEFORM (centered panel only)
    # ----------------------------

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        try:

            samples = samples.astype(np.float32)

            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            # ----------------------------
            # CENTER PANEL (NO ALBUM VISUAL)
            # ----------------------------

            rect = pygame.Rect(
                self.w // 2 - 380,
                self.h // 2 - 200,
                760,
                360
            )

            # dark panel (no circle, no blob)
            pygame.draw.rect(
                screen,
                (20, 20, 22),
                rect,
                border_radius=20
            )

            inner_x = rect.x + 30
            inner_y = rect.y + 40
            inner_w = rect.width - 60
            inner_h = rect.height - 80

            center_y = inner_y + inner_h // 2

            step = max(1, len(samples) // inner_w)

            points = []

            reaction = 1 + bass * 4 + mids * 2

            for x in range(inner_w):

                idx = x * step

                if idx >= len(samples):
                    break

                amp = (samples[idx] / 32768) * reaction

                y = center_y + int(amp * 120)

                # clamp inside panel
                y = max(rect.y + 20, min(rect.y + rect.height - 20, y))

                points.append((inner_x + x, y))

            glow = int(120 + bass * 120)
            thickness = int(2 + bass * 6)

            if len(points) > 1:

                # outer glow (pink/red)
                pygame.draw.lines(
                    screen,
                    (255, 80, 140),
                    False,
                    points,
                    thickness + 7
                )

                # mid glow
                pygame.draw.lines(
                    screen,
                    (255, 40, 90),
                    False,
                    points,
                    thickness + 4
                )

                # core line
                pygame.draw.lines(
                    screen,
                    (255, 20, 60),
                    False,
                    points,
                    thickness
                )

            # spectrum inside panel
            self.draw_spectrum(screen, samples, rect)

            # particles (pink/red)
            self.update_particles(bass, mids)

            for p in self.particles:

                pygame.draw.circle(
                    screen,
                    (255, 60, 120),
                    (int(p[0]), int(p[1])),
                    int(p[4])
                )

        except Exception as e:
            print("Visualizer error:", e)