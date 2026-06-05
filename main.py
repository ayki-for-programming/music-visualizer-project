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

font = pygame.font.SysFont("arial", 20, bold=True)

engine = DJEngine()
viz = Visualizer(WIDTH, HEIGHT)

# -------------------------
# COLORS
# -------------------------
BG = (18, 10, 14)
PINK = (255, 60, 120)
WHITE = (255, 255, 255)
DARK = (10, 6, 8)

# -------------------------
# PAD CONFIG (6 pads)
# -------------------------
pads = [
    ("KICK", "kick"),
    ("SNARE", "snare"),
    ("HIHAT", "hihat"),
    ("BASS", "bass"),
    ("CLAP", "clap"),
    ("OPEN", "openhat"),
]

pad_rects = []
pad_anim = []

cols = 3
size = (160, 110)
start_x, start_y = 60, 140
gap = 30

for i in range(len(pads)):
    x = start_x + (i % cols) * (size[0] + gap)
    y = start_y + (i // cols) * (size[1] + gap)
    pad_rects.append(pygame.Rect(x, y, *size))
    pad_anim.append(0.0)

# -------------------------
# KEY MAPPING
# -------------------------
key_map = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_5: 4,
    pygame.K_6: 5,
}

# -------------------------
# AUDIO BUFFER (visual fake input)
# -------------------------
audio_buffer = np.zeros(2048)

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
                i = key_map[event.key]
                engine.play(pads[i][1])
                pad_anim[i] = 1.0

                noise = np.random.randint(-8000, 8000, 256)
                audio_buffer = np.roll(audio_buffer, -256)
                audio_buffer[-256:] = noise

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, r in enumerate(pad_rects):
                if r.collidepoint(event.pos):
                    engine.play(pads[i][1])
                    pad_anim[i] = 1.0

                    noise = np.random.randint(-8000, 8000, 256)
                    audio_buffer = np.roll(audio_buffer, -256)
                    audio_buffer[-256:] = noise

    # decay animations
    pad_anim = [max(0, p - 0.07) for p in pad_anim]

    # -------------------------
    # AUDIO ANALYSIS
    # -------------------------
    bass, mids, highs = get_frequency_bands(audio_buffer)

    # -------------------------
    # BACKGROUND (reactive)
    # -------------------------
    screen.fill((
        int(18 + bass * 80),
        int(10 + mids * 40),
        int(14 + highs * 70),
    ))

    # -------------------------
    # TITLE
    # -------------------------
    screen.blit(font.render("DJ PAD ENGINE (1-6 or click)", True, WHITE), (40, 30))

    # -------------------------
    # PAD RENDERING
    # -------------------------
    for i, rect in enumerate(pad_rects):
        pulse = pad_anim[i]

        base = 40 + int(160 * pulse)

        color = (
            base,
            int(20 + pulse * 100),
            int(60 + pulse * 140),
        )

        # glow
        pygame.draw.rect(
            screen,
            (255, 40, 120) if pulse > 0 else DARK,
            rect.inflate(10, 10),
            border_radius=14
        )

        # pad body
        pygame.draw.rect(screen, color, rect, border_radius=12)

        # border
        pygame.draw.rect(screen, PINK, rect, 2, border_radius=12)

        label = font.render(f"{i+1} {pads[i][0]}", True, WHITE)
        screen.blit(label, (rect.x + 35, rect.y + 45))

    # -------------------------
    # CIRCULAR WAVEFORM (RIGHT SIDE)
    # -------------------------
    viz.draw_wave(screen, audio_buffer, bass, mids, highs)

    pygame.display.flip()

pygame.quit()