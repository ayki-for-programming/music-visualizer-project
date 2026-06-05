import pygame
import numpy as np

from dj_engine import DJEngine
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands

pygame.init()

WIDTH, HEIGHT = 1150, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DJ PAD ENGINE")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 22, bold=True)

engine = DJEngine()
viz = Visualizer(WIDTH, HEIGHT)

# COLORS
BG = (18, 10, 14)
PINK = (255, 60, 120)
WHITE = (255, 255, 255)
DARK = (10, 6, 8)

# PADS
pads = [
    ("KICK", "kick"),
    ("SNARE", "snare"),
    ("HIHAT", "hihat"),
    ("BASS", "bass"),
]

pad_rects = []
pad_anim = []

cols = 2
size = (200, 140)
start = (70, 140)
gap = 40

for i in range(len(pads)):
    x = start[0] + (i % cols) * (size[0] + gap)
    y = start[1] + (i // cols) * (size[1] + gap)
    pad_rects.append(pygame.Rect(x, y, *size))
    pad_anim.append(0.0)

audio_buffer = np.zeros(2048)

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: 0,
                pygame.K_2: 1,
                pygame.K_3: 2,
                pygame.K_4: 3,
            }

            if event.key in key_map:
                i = key_map[event.key]
                engine.play(pads[i][1])
                pad_anim[i] = 1.0

                noise = np.random.randint(-8000, 8000, 256)
                audio_buffer = np.roll(audio_buffer, -256)
                audio_buffer[-256:] = noise

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, r in enumerate(pad_rects):
                if r.collidepoint(event.pos):
                    engine.play(pads[i][1])
                    pad_anim[i] = 1.0

                    noise = np.random.randint(-8000, 8000, 256)
                    audio_buffer = np.roll(audio_buffer, -256)
                    audio_buffer[-256:] = noise

    pad_anim = [max(0, p - 0.08) for p in pad_anim]

    bass, mids, highs = get_frequency_bands(audio_buffer)

    screen.fill((
        int(18 + bass * 80),
        int(10 + mids * 40),
        int(14 + highs * 70),
    ))

    screen.blit(font.render("DJ PAD ENGINE (1-4 or click)", True, WHITE), (40, 30))

    # PADS
    for i, rect in enumerate(pad_rects):
        pulse = pad_anim[i]

        color = (
            40 + int(150 * pulse),
            20 + int(80 * pulse),
            60 + int(120 * pulse),
        )

        pygame.draw.rect(screen, DARK, rect.inflate(10, 10), border_radius=16)
        pygame.draw.rect(screen, color, rect, border_radius=14)

        pygame.draw.rect(screen, PINK, rect, 2, border_radius=14)

        label = font.render(f"{i+1} {pads[i][0]}", True, WHITE)
        screen.blit(label, (rect.x + 60, rect.y + 55))

    viz.draw_wave(screen, audio_buffer, bass, mids, highs)

    pygame.display.flip()

pygame.quit()