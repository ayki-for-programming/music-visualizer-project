import pygame
import numpy as np

from dj_engine import DJEngine
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands

pygame.init()

# FULLSCREEN SETUP
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("AY-DJ PAD")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24, bold=True)

engine = DJEngine()
viz = Visualizer(WIDTH, HEIGHT)

# COLORS
PINK = (255, 60, 120)
WHITE = (255, 255, 255)
DARK = (10, 6, 8)

# PAD CONFIG (LEFT SIDE GRID)
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

cols = 2
rows = 3

# LEFT SIDE AREA (40% of screen)
left_width = int(WIDTH * 0.42)

pad_w = int(left_width * 0.38)
pad_h = int(HEIGHT * 0.18)

gap_x = int(left_width * 0.08)
gap_y = int(HEIGHT * 0.04)

start_x = int(WIDTH * 0.05)
start_y = (HEIGHT - (rows * pad_h + (rows - 1) * gap_y)) // 2

for i in range(len(pads)):
    col = i % cols
    row = i // cols

    x = start_x + col * (pad_w + gap_x)
    y = start_y + row * (pad_h + gap_y)

    pad_rects.append(pygame.Rect(x, y, pad_w, pad_h))
    pad_anim.append(0.0)

# KEY MAP
key_map = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_5: 4,
    pygame.K_6: 5,
}

# AUDIO BUFFER (visual only)
audio_buffer = np.zeros(2048)

running = True

while running:
    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # ESC = clean exit from fullscreen
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.set_mode((1150, 700))

            # PAD TRIGGER
            if event.key in key_map:
                i = key_map[event.key]
                engine.play(pads[i][1])
                pad_anim[i] = 1.0

                noise = np.random.randint(-9000, 9000, 256)
                audio_buffer = np.roll(audio_buffer, -256)
                audio_buffer[-256:] = noise

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, r in enumerate(pad_rects):
                if r.collidepoint(event.pos):
                    engine.play(pads[i][1])
                    pad_anim[i] = 1.0

                    noise = np.random.randint(-9000, 9000, 256)
                    audio_buffer = np.roll(audio_buffer, -256)
                    audio_buffer[-256:] = noise

    # decay animations
    pad_anim = [max(0, p - 0.07) for p in pad_anim]

    # AUDIO ANALYSIS
    bass, mids, highs = get_frequency_bands(audio_buffer)

    # BACKGROUND (reactive)
    screen.fill((
        int(18 + bass * 90),
        int(10 + mids * 50),
        int(14 + highs * 80),
    ))

    # TITLE
    screen.blit(font.render("AY-DJ PAD (1-6 / click / ESC exit)", True, WHITE), (40, 30))

    # LEFT SIDE PADS
    for i, rect in enumerate(pad_rects):
        pulse = pad_anim[i]

        color = (
            40 + int(170 * pulse),
            20 + int(100 * pulse),
            60 + int(150 * pulse),
        )

        # glow
        pygame.draw.rect(
            screen,
            (255, 40, 120) if pulse > 0 else DARK,
            rect.inflate(12, 12),
            border_radius=16
        )

        # pad body
        pygame.draw.rect(screen, color, rect, border_radius=14)

        # border
        pygame.draw.rect(screen, PINK, rect, 3, border_radius=14)

        # label
        label = font.render(f"{i+1} {pads[i][0]}", True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    # RIGHT SIDE CIRCULAR WAVEFORM
    viz.draw_wave(screen, audio_buffer, bass, mids, highs)

    pygame.display.flip()

pygame.quit()