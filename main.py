import pygame
import numpy as np
import wave
import threading
import os

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands

# ------------------
# INIT
# ------------------

pygame.init()
pygame.mixer.init()

# Smaller, cleaner Spotify-like size
WIDTH, HEIGHT = 1150, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpotifAY")

clock = pygame.time.Clock()

font_large = pygame.font.SysFont("arial", 40, bold=True)
font = pygame.font.SysFont("arial", 24)
font_small = pygame.font.SysFont("arial", 18)

visualizer = Visualizer(WIDTH, HEIGHT)

# ------------------
# COLORS
# ------------------

BASE_BG = (18, 18, 18)
SIDEBAR = (12, 12, 12)
CARD = (35, 35, 35)
GREEN = (29, 185, 84)
WHITE = (255, 255, 255)
LIGHT = (180, 180, 180)

# ------------------
# STATE
# ------------------

prompt = ""
current_file = None
current_track = "No Track Loaded"

playing = False
paused = False
generating = False

track_history = []

# Play button
play_rect = pygame.Rect(WIDTH // 2 - 35, HEIGHT - 100, 70, 70)

# ------------------
# AUDIO HELPERS
# ------------------

def get_samples(file_path, sample_pos):
    try:
        with wave.open(file_path, "rb") as wf:
            total = wf.getnframes()

            if total < 2048:
                return np.zeros(2048)

            sample_pos = max(0, min(sample_pos, total - 2048))
            wf.setpos(sample_pos)

            data = wf.readframes(2048)

            samples = np.frombuffer(data, dtype=np.int16)

            # FIX: stereo → mono
            if len(samples) % 2 == 0:
                samples = samples.reshape(-1, 2)
                samples = samples.mean(axis=1)

            if len(samples) == 0:
                return np.zeros(2048)

            return samples

    except Exception as e:
        print("Audio read error:", e)
        return np.zeros(2048)


def get_track_duration(file_path):
    try:
        with wave.open(file_path, "rb") as wf:
            return wf.getnframes() / wf.getframerate()
    except:
        return 0


# ------------------
# MUSIC THREAD
# ------------------

def generate_async(user_prompt):
    global current_file, current_track, generating, playing, paused

    generating = True

    try:
        filename = generate_music(user_prompt)

        current_file = filename
        current_track = user_prompt

        if user_prompt not in track_history:
            track_history.insert(0, user_prompt)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        playing = True
        paused = False

    except Exception as e:
        print("Generation error:", e)

    generating = False


# ------------------
# LOOP
# ------------------

running = True

while running:
    clock.tick(60)

    # ------------------
    # EVENTS
    # ------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_RETURN and prompt.strip() and not generating:
                user_prompt = prompt
                prompt = ""

                threading.Thread(
                    target=generate_async,
                    args=(user_prompt,),
                    daemon=True
                ).start()

            elif event.key == pygame.K_BACKSPACE:
                prompt = prompt[:-1]

            elif event.key == pygame.K_SPACE:
                if current_file:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused = True

            else:
                if event.unicode:
                    prompt += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos) and current_file:
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True

    # ------------------
    # AUDIO
    # ------------------

    if current_file and os.path.exists(current_file):
        pos_ms = pygame.mixer.music.get_pos()
        sample_pos = int(max(pos_ms, 0) * 44.1)
        samples = get_samples(current_file, sample_pos)
    else:
        samples = np.zeros(2048)

    bass, mids, highs = get_frequency_bands(samples)

    # ------------------
    # MUSIC-REACTIVE BACKGROUND
    # ------------------

    screen.fill((
        int(18 + bass * 30),
        int(18 + mids * 20),
        int(18 + highs * 25)
    ))

    # ------------------
    # SIDEBAR
    # ------------------

    pygame.draw.rect(screen, SIDEBAR, (0, 0, 260, HEIGHT))

    screen.blit(
        font_large.render("SpotifAY", True, GREEN),
        (25, 25)
    )

    screen.blit(
        font.render("Your Library", True, LIGHT),
        (25, 90)
    )

    y = 130
    for t in track_history[:10]:
        screen.blit(font_small.render(t[:22], True, WHITE), (25, y))
        y += 28

    # ------------------
    # MAIN CARD
    # ------------------

    pygame.draw.rect(screen, CARD, (320, 90, 520, 520), border_radius=20)

    pulse = int(80 + bass * 120)

    pygame.draw.circle(screen, GREEN, (580, 340), pulse)
    pygame.draw.circle(screen, BASE_BG, (580, 340), pulse // 2)

    screen.blit(
        font_large.render(current_track, True, WHITE),
        (320, 630)
    )

    status = "Generating..." if generating else ("Paused" if paused else "Playing" if playing else "Idle")

    screen.blit(font.render(status, True, LIGHT), (320, 665))

    # ------------------
    # PROGRESS BAR
    # ------------------

    bar_x, bar_y, bar_w = 320, 690, 700

    pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, 6), border_radius=4)

    if current_file:
        duration = get_track_duration(current_file)
        pos = pygame.mixer.music.get_pos() / 1000

        if duration > 0:
            progress = min(1, pos / duration)

            pygame.draw.rect(
                screen,
                GREEN,
                (bar_x, bar_y, int(bar_w * progress), 6),
                border_radius=4
            )

    # ------------------
    # VISUALS
    # ------------------

    visualizer.draw_wave(screen, samples, bass, mids, highs)

    # ------------------
    # PLAY BUTTON
    # ------------------

    pygame.draw.circle(screen, GREEN, play_rect.center, 35)

    if paused or not playing:
        pygame.draw.polygon(screen, (0, 0, 0), [
            (play_rect.centerx - 8, play_rect.centery - 15),
            (play_rect.centerx - 8, play_rect.centery + 15),
            (play_rect.centerx + 15, play_rect.centery)
        ])
    else:
        pygame.draw.rect(screen, (0, 0, 0), (play_rect.centerx - 12, play_rect.centery - 15, 8, 30))
        pygame.draw.rect(screen, (0, 0, 0), (play_rect.centerx + 4, play_rect.centery - 15, 8, 30))

    # ------------------
    # INPUT BOX
    # ------------------

    pygame.draw.rect(screen, CARD, (300, HEIGHT - 50, WIDTH - 340, 40), border_radius=10)
    pygame.draw.rect(screen, GREEN, (300, HEIGHT - 50, WIDTH - 340, 40), 2, border_radius=10)

    screen.blit(
        font.render(prompt or "Type a music prompt...", True, WHITE),
        (320, HEIGHT - 42)
    )

    pygame.display.flip()

pygame.quit()