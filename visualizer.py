import pygame
import numpy as np


class Visualizer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.phase = 0.0  # motion driver

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        samples = samples.astype(np.float32)

        if len(samples.shape) > 1:
            samples = samples.mean(axis=1)

        # -----------------------------
        # SMALL BOTTOM STRIP (NOT CENTER)
        # -----------------------------
        rect = pygame.Rect(
            300,
            self.h - 140,
            self.w - 340,
            90
        )

        pygame.draw.rect(screen, (10, 6, 8), rect, border_radius=12)

        inner_x = rect.x + 10
        inner_y = rect.y + 10
        inner_w = rect.width - 20
        inner_h = rect.height - 20

        center = inner_y + inner_h // 2

        step = max(1, len(samples) // inner_w)

        points = []

        # -----------------------------
        # "ALIVE" MOTION ENGINE
        # -----------------------------
        self.phase += 0.15 + highs * 0.5

        bass_boost = 1 + bass * 4
        mid_boost = 1 + mids * 2

        for x in range(inner_w):

            idx = x * step
            if idx >= len(samples):
                break

            val = samples[idx] / 32768

            # 🔥 add wave motion even when silent
            motion = np.sin(x * 0.08 + self.phase) * 0.15

            amp = val * bass_boost * mid_boost + motion * highs

            # sharpen + exaggerate peaks
            amp = np.sign(amp) * (abs(amp) ** 0.65)

            y = center + int(amp * 60)

            points.append((inner_x + x, y))

        # -----------------------------
        # DRAW MAIN WAVE
        # -----------------------------
        if len(points) > 2:
            pygame.draw.lines(screen, (255, 40, 120), False, points, 2)
            pygame.draw.lines(screen, (255, 160, 220), False, points, 1)

        # -----------------------------
        # "ENERGY DOTS" (makes it feel alive)
        # -----------------------------
        if highs > 0.2:
            for i in range(0, len(points), 18):
                x, y = points[i]
                pygame.draw.circle(
                    screen,
                    (255, 80, 160),
                    (x, y),
                    2
                )