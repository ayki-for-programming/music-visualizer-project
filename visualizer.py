import pygame
import numpy as np
import random


class Visualizer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.particles = []

    def draw_wave(self, screen, samples, bass, mids, highs):

        if len(samples) < 10:
            return

        try:
            samples = samples.astype(np.float32)

            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            rect = pygame.Rect(
                self.w // 2 - 400,
                self.h // 2 - 200,
                800,
                360
            )

            pygame.draw.rect(screen, (18, 10, 14), rect, border_radius=20)

            step = max(1, len(samples) // rect.width)
            center_y = rect.y + rect.height // 2

            points = []

            reaction = 1 + bass * 5

            for x in range(rect.width - 60):
                idx = x * step
                if idx >= len(samples):
                    break

                amp = samples[idx] / 32768 * reaction
                y = center_y + int(amp * 140)

                points.append((rect.x + 30 + x, y))

            if len(points) > 2:
                pygame.draw.lines(screen, (255, 60, 120), False, points, 4)

            # particles
            if bass > 0.2:
                for _ in range(3):
                    self.particles.append([
                        random.randint(rect.x, rect.x + rect.width),
                        rect.y + rect.height // 2,
                        random.uniform(-2, 2),
                        random.uniform(-5, -1),
                        random.randint(2, 4),
                        1.0
                    ])

            new_particles = []
            for p in self.particles:
                p[0] += p[2]
                p[1] += p[3]
                p[5] -= 0.02

                if p[5] > 0:
                    new_particles.append(p)

            self.particles = new_particles

            for p in self.particles:
                pygame.draw.circle(
                    screen,
                    (255, 80, 140),
                    (int(p[0]), int(p[1])),
                    int(p[4])
                )

        except:
            pass