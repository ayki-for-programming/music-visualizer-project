import pygame
import random

class AlbumArt:

    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))

        self.surface.fill((20, 20, 40))

        for _ in range(300):
            x = random.randint(0, width)
            y = random.randint(0, height)

            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )

            pygame.draw.circle(
                self.surface,
                color,
                (x, y),
                random.randint(2, 12)
            )

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
        