import pygame

def create_glow(width, height):

    return pygame.Surface(
        (width, height),
        pygame.SRCALPHA
    )