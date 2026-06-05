import pygame
import random

class AlbumArt:

    def __init__(self, w, h):
        self.surface = pygame.Surface((w, h))

        self.surface.fill((10, 10, 20))

        for _ in range(200):

            x = random.randint(0, w)
            y = random.randint(0, h)

            color = (
                random.randint(80, 255),
                random.randint(80, 255),
                random.randint(80, 255)
            )

            pygame.draw.circle(
                self.surface,
                color,
                (x, y),
                random.randint(1, 5)
            )

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))