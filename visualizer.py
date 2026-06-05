import pygame
import numpy as np

class Visualizer:

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def draw_wave(self, screen, samples, pulse=0):

        if len(samples) < 10:
            return

        samples = samples.astype(np.float32)

        center_y = self.h // 2 + 40

        step = max(1, len(samples) // self.w)

        points = []

        for x in range(self.w):

            i = x * step

            if i < len(samples):

                amp = samples[i] / 2000
                y = center_y + int(amp * 120)

                points.append((x, y))

        if len(points) > 1:

            # pulse affects glow intensity + thickness

            glow = int(80 + pulse * 175)

            thickness = int(2 + pulse * 6)

            # outer glow
            pygame.draw.lines(
                screen,
                (255, 60, 140),
                False,
                points,
                thickness + 6
            )

            # mid glow
            pygame.draw.lines(
                screen,
                (255, glow, 200),
                False,
                points,
                thickness + 3
            )

            # core line
            pygame.draw.lines(
                screen,
                (30, 215, 96),
                False,
                points,
                thickness
            )