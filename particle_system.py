import pygame
import random

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

        self.life = 255

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 4

    def draw(self, screen):

        if self.life > 0:

            pygame.draw.circle(
                screen,
                (255, max(0, self.life), max(0, self.life)),
                (int(self.x), int(self.y)),
                3
            )

class ParticleSystem:

    def __init__(self):
        self.particles = []

    def explode(self, x, y):

        for _ in range(50):
            self.particles.append(Particle(x, y))

    def update(self):

        for p in self.particles:
            p.update()

        self.particles = [
            p for p in self.particles
            if p.life > 0
        ]

    def draw(self, screen):

        for p in self.particles:
            p.draw(screen)