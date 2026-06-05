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

WIDTH, HEIGHT = 1150, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpotifAY")

clock = pygame.time.Clock()

font_large = pygame.font.SysFont("arial", 40, bold=True)
font = pygame.font.SysFont("arial", 24)
font_small = pygame.font.SysFont("arial", 18)

visualizer = Visualizer(WIDTH, HEIGHT)

# ------------------
# COLORS (PINK THEME ONLY)
# ------------------

BASE_BG = (18, 10, 14)
SIDEBAR = (12, 8, 10)
CARD = (25, 15, 20)

PINK = (255, 60, 120)
HOT_PINK = (255, 20, 90)
LIGHT = (200, 180, 190)
WHITE = (255, 255, 255)

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

play_rect = pygame.Rect(WIDTH // 2 - 35, HEIGHT - 95, 70, 70)

# ------------------
# AUDIO
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

            # stereo → mono
            if len(samples) % 2 == 0:
                samples = samples.reshape(-1, 2)
                samples = samples.mean(axis=1)

            return samples

    except:
        return np.zeros(2048)


def get_track_duration(file_path):

    try:
        with wave.open(file_path, "rb") as wf:
            return wf.getnframes() / wf.getframerate()
    except:
        return 0


# ------------------
# GENERATION THREAD
# ------------------

def generate_async(text):

    global current_file, current_track, generating, playing, paused

    generating = True

    try:
        file = generate_music(text)

        current_file = file
        current_track = text

        if text not in track_history:
            track_history.insert(0, text)

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        playing = True
        paused = False

    except Exception as e:
        print("Error:", e)

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

                text = prompt
                prompt = ""

                threading.Thread(
                    target=generate_async,
                    args=(text,),
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
    # AUDIO DATA
    # ------------------

    if current_file and os.path.exists(current_file):

        pos = pygame.mixer.music.get_pos()
        sample_pos = int(max(pos, 0) * 44.1)

        samples = get_samples(current_file, sample_pos)

    else:
        samples = np.zeros(2048)

    bass, mids, highs = get_frequency_bands(samples)

    # ------------------
    # BACKGROUND (PINK REACTIVE)
    # ------------------

    screen.fill((
        int(18 + bass * 35),
        int(10 + mids * 20),
        int(14 + highs * 25)
    ))

    # ------------------
    # SIDEBAR
    # ------------------

    pygame.draw.rect(screen, SIDEBAR, (0, 0, 260, HEIGHT))

    screen.blit(
        font_large.render("SpotifAY", True, PINK),
        (25, 25)
    )

    screen.blit(
        font.render("Library", True, LIGHT),
        (25, 90)
    )

    y = 130
    for t in track_history[:10]:
        screen.blit(font_small.render(t[:22], True, WHITE), (25, y))
        y += 28

    # ------------------
    # MAIN TITLE
    # ------------------

    screen.blit(
        font_large.render(current_track, True, WHITE),
        (300, 40)
    )

    status = "Generating..." if generating else ("Paused" if paused else "Playing" if playing else "Idle")

    screen.blit(font.render(status, True, LIGHT), (300, 80))

    # ------------------
    # PROGRESS BAR
    # ------------------

    bar_x, bar_y, bar_w = 300, 110, 700

    pygame.draw.rect(screen, (50, 30, 40), (bar_x, bar_y, bar_w, 6), border_radius=4)

    if current_file:

        duration = get_track_duration(current_file)
        pos = pygame.mixer.music.get_pos() / 1000

        if duration > 0:
            progress = min(1, pos / duration)

            pygame.draw.rect(
                screen,
                HOT_PINK,
                (bar_x, bar_y, int(bar_w * progress), 6),
                border_radius=4
            )

    # ------------------
    # VISUALIZER (ONLY SOURCE OF WAVES)
    # ------------------

   # visualizer.draw_wave(screen, samples, bass, mids, highs)

    # ------------------
    # PLAY BUTTON
    # ------------------

    pygame.draw.circle(screen, PINK, play_rect.center, 35)

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

    pygame.draw.rect(screen, CARD, (300, HEIGHT - 55, 700, 40), border_radius=10)
    pygame.draw.rect(screen, PINK, (300, HEIGHT - 55, 700, 40), 2, border_radius=10)

    screen.blit(
        font.render(prompt or "Type a music prompt...", True, WHITE),
        (320, HEIGHT - 45)
    )

    pygame.display.flip()

pygame.quit()