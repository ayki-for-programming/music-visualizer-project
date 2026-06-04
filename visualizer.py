import pygame

class Visualizer:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_wave(self, screen, samples):

        if len(samples) < 2:
            return

        points = []

        step = max(1, len(samples) // self.width)

        for x in range(self.width):

            index = x * step

            if index < len(samples):

                y = self.height // 2 + int(samples[index] / 300)

                points.append((x, y))

        if len(points) > 1:

            pygame.draw.lines(
                screen,
                (0, 255, 255),
                False,
                points,
                2
            )