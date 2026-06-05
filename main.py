import pygame
import numpy as np

from dj_engine import DJEngine
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands

pygame.init()

# -------------------------
# FULLSCREEN SETUP
# -------------------------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("DJ PAD ENGINE")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20, bold=True)

engine = DJEngine()
viz = Visualizer(WIDTH, HEIGHT)

# -------------------------
# COLORS
# -------------------------
PINK = (255, 60, 120)
WHITE = (255, 255, 255)
DARK = (10, 6, 8)

# -------------------------
# PAD CONFIG (3 rows × 2 cols)
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

cols = 2
size = (200, 120)

start_x = 60
start_y = 140

gap_x = 30
gap_y = 25

for i in range(len(pads)):
    col = i % cols
    row = i // cols

    x = start_x + col * (size[0] + gap_x)
    y = start_y + row * (size[1] + gap_y)

    pad_rects.append(pygame.Rect(x, y, *size))
    pad_anim.append(0.0)

# -------------------------
# KEY MAP
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
# AUDIO BUFFER (visual only)
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

            # -------------------------
            # ESC = SAFE EXIT (FULLSCREEN FIX)
            # -------------------------
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.set_mode((1150, 700))  # restore window before exit

            # -------------------------
            # PAD TRIGGER
            # -------------------------
            if event.key in key_map:
                i = key_map[event.key]

                engine.play(pads[i][1])
                pad_anim[i] = 1.0

                noise = np.random.randint(-8000, 8000, 256)
                audio_buffer = np.roll(audio_buffer, -256)
                audio_buffer[-256:] = noise

        # -------------------------
        # MOUSE PAD TRIGGER
        # -------------------------
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
    # BACKGROUND
    # -------------------------
    screen.fill((
        int(18 + bass * 80),
        int(10 + mids * 40),
        int(14 + highs * 70),
    ))

    # -------------------------
    # TITLE
    # -------------------------
    screen.blit(font.render("AY-DJ PAD (1-6 or click, ESC to exit)", True, WHITE), (40, 30))

    # -------------------------
    # PADS
    # -------------------------
    for i, rect in enumerate(pad_rects):
        pulse = pad_anim[i]

        color = (
            40 + int(160 * pulse),
            20 + int(90 * pulse),
            60 + int(140 * pulse),
        )

        pygame.draw.rect(
            screen,
            (255, 40, 120) if pulse > 0 else DARK,
            rect.inflate(10, 10),
            border_radius=14
        )

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, PINK, rect, 2, border_radius=12)

        label = font.render(f"{i+1} {pads[i][0]}", True, WHITE)
        screen.blit(label, (rect.x + 55, rect.y + 45))

    # -------------------------
    # CIRCULAR WAVEFORM
    # -------------------------
    viz.draw_wave(screen, audio_buffer, bass, mids, highs)

    pygame.display.flip()

pygame.quit()