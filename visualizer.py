import pygame
import numpy as np


class Visualizer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.phase = 0.0

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        samples = samples.astype(np.float32)

        if len(samples.shape) > 1:
            samples = samples.mean(axis=1)

        # CIRCLE POSITION (RIGHT SIDE)
        cx = int(self.w * 0.78)
        cy = int(self.h * 0.50)

        base_radius = 110 + bass * 60

        self.phase += 0.08 + highs * 0.4

        points = []

        # CIRCLE WAVEFORM ENGINE
        steps = 140  # resolution of circle

        for i in range(steps):

            angle = (i / steps) * np.pi * 2

            idx = int((i / steps) * len(samples))
            val = samples[idx] / 32768

            # audio shaping
            audio = val * (1 + bass * 3)

            # living motion (keeps it moving even when silent)
            motion = np.sin(angle * 3 + self.phase) * 0.12

            # highs = jitter spikes
            jitter = (np.random.rand() - 0.5) * highs * 0.3

            radius = base_radius + (audio * 90) + (motion * 40) + (jitter * 80)

            x = cx + np.cos(angle) * radius
            y = cy + np.sin(angle) * radius

            points.append((x, y))

        # OUTER GLOW RINGS
        pygame.draw.circle(screen, (25, 10, 18), (cx, cy), int(base_radius + 60))
        pygame.draw.circle(screen, (255, 40, 120), (cx, cy), int(base_radius), 2)

        # WAVEFORM CIRCLE
        if len(points) > 2:

            pygame.draw.lines(screen, (255, 60, 140), True, points, 2)
            pygame.draw.lines(screen, (255, 180, 220), True, points, 1)

        # CENTER PULSE (kick reaction feel)
        pulse = 6 + bass * 20
        pygame.draw.circle(screen, (255, 80, 160), (cx, cy), int(pulse))