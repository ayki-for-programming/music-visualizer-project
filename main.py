import pygame
import numpy as np
from collections import deque

from dj_engine import DJEngine
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands


pygame.init()

WIDTH, HEIGHT = 1150, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DJ ENGINE")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)

engine = DJEngine()
viz = Visualizer(WIDTH, HEIGHT)

# -------------------------
# AUDIO BUFFER (FOR VISUALS)
# -------------------------
audio_buffer = deque(maxlen=2048)

# -------------------------
# COLORS
# -------------------------
BG = (18, 10, 14)
PINK = (255, 60, 120)
WHITE = (255, 255, 255)

# -------------------------
# KEY MAP (PAD MODE)
# -------------------------
key_map = {
    pygame.K_1: "kick",
    pygame.K_2: "snare",
    pygame.K_3: "hihat",
    pygame.K_4: "bass"
}

running = True

while running:
    clock.tick(60)

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key in key_map:
                sound = key_map[event.key]
                engine.play(sound)

                # fake buffer boost for visualization punch
                audio_buffer.extend(np.random.randint(-5000, 5000, 256))

    # -------------------------
    # AUDIO VISUAL INPUT
    # -------------------------
    if len(audio_buffer) < 2048:
        samples = np.zeros(2048)
    else:
        samples = np.array(audio_buffer)

    bass, mids, highs = get_frequency_bands(samples)

    # -------------------------
    # BACKGROUND
    # -------------------------
    screen.fill((
        int(18 + bass * 60),
        int(10 + mids * 40),
        int(14 + highs * 60)
    ))

    # -------------------------
    # TITLE
    # -------------------------
    screen.blit(font.render("DJ ENGINE (1-4 pads)", True, WHITE), (30, 30))

    screen.blit(font.render("1=Kick  2=Snare  3=HiHat  4=Bass", True, PINK), (30, 70))

    # -------------------------
    # VISUALIZER
    # -------------------------
    viz.draw_wave(screen, samples, bass, mids, highs)

    pygame.display.flip()

pygame.quit()