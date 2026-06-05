import pygame
import numpy as np


class Visualizer:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        samples = samples.astype(np.float32)

        if len(samples.shape) > 1:
            samples = samples.mean(axis=1)

        rect = pygame.Rect(self.w // 2 - 420, self.h // 2 - 220, 820, 420)

        pygame.draw.rect(screen, (12, 8, 10), rect, border_radius=18)

        inner_x = rect.x + 20
        inner_y = rect.y + 20
        inner_w = rect.width - 40
        inner_h = rect.height - 40

        center = inner_y + inner_h // 2

        step = max(1, len(samples) // inner_w)

        points = []

        bass_boost = 1 + bass * 6
        mids_boost = 1 + mids * 2

        for x in range(inner_w):

            idx = x * step
            if idx >= len(samples):
                break

            val = samples[idx] / 32768

            amp = val * bass_boost * (1 + mids_boost * 0.3)

            amp = np.sign(amp) * (abs(amp) ** 0.75)

            y = center + int(amp * 170)

            points.append((inner_x + x, y))

        if len(points) > 2:
            pygame.draw.lines(screen, (255, 60, 140), False, points, 3)
            pygame.draw.lines(screen, (255, 160, 220), False, points, 1)