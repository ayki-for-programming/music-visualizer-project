import pygame
import numpy as np
import wave
import random

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands
from album_art import AlbumArt

# ------------------
# INIT
# ------------------

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Music Visualizer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)

# ------------------
# AUDIO READER
# ------------------

def get_audio_samples(filename):
    try:
        with wave.open(filename, "rb") as wf:
            frames = wf.readframes(2048)
            samples = np.frombuffer(frames, dtype=np.int16)
            return samples
    except:
        return np.zeros(1024)

# ------------------
# SYSTEMS
# ------------------

visualizer = Visualizer(WIDTH, HEIGHT)
album = AlbumArt(WIDTH, HEIGHT)

prompt = ""
current_audio = None

playing = False
beat_pulse = 0  # NEW

# ------------------
# LOOP
# ------------------

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # ------------------
            # PLAY / PAUSE
            # ------------------

            if event.key == pygame.K_SPACE:
                if playing:
                    pygame.mixer.music.pause()
                    playing = False
                else:
                    pygame.mixer.music.unpause()
                    playing = True

            elif event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_RETURN:

                if prompt.strip():

                    current_audio = generate_music(prompt)

                    pygame.mixer.music.load(current_audio)
                    pygame.mixer.music.play()

                    playing = True
                    beat_pulse = 1.0  # trigger pulse on new song

                    prompt = ""

            elif event.key == pygame.K_BACKSPACE:
                prompt = prompt[:-1]

            else:
                prompt += event.unicode

    # ------------------
    # AUDIO DATA
    # ------------------

    if current_audio:
        samples = get_audio_samples(current_audio)
    else:
        samples = np.zeros(1024)

    bass, mids, highs = get_frequency_bands(samples)

    # ------------------
    # BEAT PULSE LOGIC
    # ------------------

    beat_pulse *= 0.92  # decay

    if bass > 5:  # simple beat trigger
        beat_pulse = min(1.0, beat_pulse + 0.25)

    # ------------------
    # BACKGROUND (dark Spotify)
    # ------------------

    intensity = int(20 + beat_pulse * 30)

    screen.fill((10, 10, 15))

    pygame.draw.rect(
        screen,
        (intensity, 20, intensity + 10),
        (0, 0, WIDTH, HEIGHT)
    )

    # ------------------
    # DRAW SYSTEMS
    # ------------------

    album.draw(screen)

    visualizer.draw_wave(screen, samples, beat_pulse)

    # ------------------
    # TEXT
    # ------------------

    title = font.render("Now Playing", True, (200, 200, 200))
    screen.blit(title, (380, 80))

    if current_audio:
        name = small_font.render(prompt.upper(), True, (255, 255, 255))
        screen.blit(name, (380, 120))

    # ------------------
    # PLAY / PAUSE UI
    # ------------------

    status = "PLAYING ▶" if playing else "PAUSED ⏸"

    status_text = small_font.render(status, True, (30, 215, 96))
    screen.blit(status_text, (WIDTH - 180, 30))

    hint = small_font.render("SPACE = play/pause", True, (120, 120, 120))
    screen.blit(hint, (WIDTH - 220, 55))

    # ------------------
    # INPUT BAR
    # ------------------

    pygame.draw.rect(screen, (25, 25, 35), (40, HEIGHT - 90, WIDTH - 80, 50), border_radius=15)

    pygame.draw.rect(screen, (30, 215, 96), (40, HEIGHT - 90, WIDTH - 80, 50), 2, border_radius=15)

    text = prompt if prompt else "Type a music prompt..."
    color = (255, 255, 255) if prompt else (140, 140, 140)

    screen.blit(font.render(text, True, color), (60, HEIGHT - 78))

    pygame.display.flip()

pygame.quit()