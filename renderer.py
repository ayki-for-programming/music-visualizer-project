import pygame
import random

class Renderer:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.particles = []

        for _ in range(100):

            self.particles.append([
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(1, 10)
            ])

    def update(self, bass=0):

        for p in self.particles:

            speed = 0.05 + bass * 0.000001

            p[2] -= speed

            if p[2] < 1:
                p[2] = 10

    def draw(self, screen):

        center_x = self.width // 2
        center_y = self.height // 2

        for x, y, z in self.particles:

            scale = 200 / z

            px = int(center_x + x * scale)
            py = int(center_y + y * scale)

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (px, py),
                2
            )
            