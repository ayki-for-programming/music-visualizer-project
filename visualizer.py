import pygame
import numpy as np
import random


class Visualizer:

    def __init__(self, w, h):

        self.w = w
        self.h = h
        self.particles = []


    # ------------------
    # PARTICLES
    # ------------------

    def update_particles(self, bass, mids):

        if bass + mids > 0.25:

            for _ in range(3):

                self.particles.append([

                    random.randint(self.w // 2 - 250, self.w // 2 + 250),
                    self.h // 2,

                    random.uniform(-2, 2),
                    random.uniform(-5, -1),

                    random.randint(2, 4),
                    1.0
                ])

        alive = []

        for p in self.particles:

            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 0.02

            if p[5] > 0:
                alive.append(p)

        self.particles = alive


    # ------------------
    # SPECTRUM
    # ------------------

    def draw_spectrum(self, screen, samples, rect):

        if len(samples) < 128:
            return

        try:

            samples = samples.astype(np.float32)

            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            fft = np.fft.rfft(samples)
            mag = np.abs(fft)

            bars = 50
            chunk = max(1, len(mag) // bars)

            x_start = rect.x + 40
            y_base = rect.y + rect.height - 40

            for i in range(bars):

                value = np.mean(mag[i * chunk:(i + 1) * chunk])

                height = int(min(200, value / 300))

                x = x_start + i * 12

                pygame.draw.rect(
                    screen,
                    (255, 40, 100),
                    (x, y_base - height, 6, height),
                    border_radius=3
                )

        except:
            pass


    # ------------------
    # WAVEFORM (CENTERED ONLY)
    # ------------------

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        try:

            samples = samples.astype(np.float32)

            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            rect = pygame.Rect(
                self.w // 2 - 380,
                self.h // 2 - 200,
                760,
                360
            )

            pygame.draw.rect(screen, (18, 10, 14), rect, border_radius=20)

            inner_x = rect.x + 30
            inner_y = rect.y + 40
            inner_w = rect.width - 60
            inner_h = rect.height - 80

            center_y = inner_y + inner_h // 2

            step = max(1, len(samples) // inner_w)

            points = []

            reaction = 1 + bass * 4

            for x in range(inner_w):

                idx = x * step

                if idx >= len(samples):
                    break

                amp = (samples[idx] / 32768) * reaction

                y = center_y + int(amp * 120)

                points.append((inner_x + x, y))

         

                pygame.draw.lines(screen, (255, 60, 120), False, points, 6)
                pygame.draw.lines(screen, (255, 20, 90), False, points, 3)

            self.draw_spectrum(screen, samples, rect)
            self.update_particles(bass, mids)

            for p in self.particles:

                pygame.draw.circle(
                    screen,
                    (255, 80, 140),
                    (int(p[0]), int(p[1])),
                    int(p[4])
                )

        except:
            pass