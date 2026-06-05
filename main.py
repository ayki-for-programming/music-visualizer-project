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

WIDTH, HEIGHT = 1400, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spotify AI Music")

clock = pygame.time.Clock()

font_large = pygame.font.SysFont("arial", 34, bold=True)
font = pygame.font.SysFont("arial", 24)
font_small = pygame.font.SysFont("arial", 18)

visualizer = Visualizer(WIDTH, HEIGHT)

# ------------------
# COLORS
# ------------------

BACKGROUND = (18, 18, 18)
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

# ------------------
# PLAY BUTTON
# ------------------

play_rect = pygame.Rect(
    WIDTH // 2 - 35,
    HEIGHT - 100,
    70,
    70
)

# ------------------
# AUDIO HELPERS
# ------------------

def get_samples(file_path, sample_pos):

    try:

        with wave.open(file_path, "rb") as wf:

            total = wf.getnframes()

            if total < 2048:
                return np.zeros(2048)

            sample_pos = max(
                0,
                min(sample_pos, total - 2048)
            )

            wf.setpos(sample_pos)

            data = wf.readframes(2048)

            samples = np.frombuffer(
                data,
                dtype=np.int16
            )

            if len(samples) == 0:
                return np.zeros(2048)

            return samples

    except Exception as e:

        print("Audio read error:", e)

        return np.zeros(2048)


def get_track_duration(file_path):

    try:

        with wave.open(file_path, "rb") as wf:

            frames = wf.getnframes()
            rate = wf.getframerate()

            return frames / rate

    except:

        return 0


# ------------------
# MUSIC GENERATION THREAD
# ------------------

def generate_async(user_prompt):

    global current_file
    global current_track
    global generating
    global playing
    global paused

    try:

        generating = True

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
# MAIN LOOP
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

            elif event.key == pygame.K_RETURN:

                if prompt.strip() and not generating:

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

                if playing:

                    if paused:

                        pygame.mixer.music.unpause()
                        paused = False

                    else:

                        pygame.mixer.music.pause()
                        paused = True

            else:

                if len(event.unicode) > 0:
                    prompt += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if play_rect.collidepoint(event.pos):

                if current_file:

                    if paused:

                        pygame.mixer.music.unpause()
                        paused = False

                    else:

                        pygame.mixer.music.pause()
                        paused = True

    # ------------------
    # AUDIO ANALYSIS
    # ------------------

    if current_file and os.path.exists(current_file):

        pos_ms = pygame.mixer.music.get_pos()

        if pos_ms < 0:
            pos_ms = 0

        sample_pos = int(pos_ms * 44.1)

        samples = get_samples(
            current_file,
            sample_pos
        )

    else:

        samples = np.zeros(2048)

    bass, mids, highs = get_frequency_bands(samples)

    # ------------------
    # DRAW UI
    # ------------------

    screen.fill(BACKGROUND)

    # Sidebar
    pygame.draw.rect(
        screen,
        SIDEBAR,
        (0, 0, 260, HEIGHT)
    )

    # Main area
    pygame.draw.rect(
        screen,
        BACKGROUND,
        (260, 0, WIDTH - 260, HEIGHT)
    )

    # Logo
    screen.blit(
        font_large.render(
            "Spotify AI",
            True,
            WHITE
        ),
        (25, 25)
    )

    # History title
    screen.blit(
        font.render(
            "Generated Tracks",
            True,
            LIGHT
        ),
        (25, 90)
    )

    # Track history
    y = 130

    for track in track_history[:10]:

        txt = track[:22]

        screen.blit(
            font_small.render(
                txt,
                True,
                WHITE
            ),
            (25, y)
        )

        y += 30

    # Album card
    pygame.draw.rect(
        screen,
        CARD,
        (350, 100, 500, 500),
        border_radius=20
    )

    # Album graphic
    pulse = int(120 + bass * 0.02)

    pygame.draw.circle(
        screen,
        GREEN,
        (600, 350),
        pulse
    )

    pygame.draw.circle(
        screen,
        BACKGROUND,
        (600, 350),
        pulse // 2
    )

    # Track title
    screen.blit(
        font_large.render(
            current_track,
            True,
            WHITE
        ),
        (350, 630)
    )

    # Status
    status = "Generating..." if generating else (
        "Paused" if paused else (
            "Playing" if playing else "Idle"
        )
    )

    screen.blit(
        font.render(
            status,
            True,
            LIGHT
        ),
        (350, 675)
    )

    # Progress bar
    bar_x = 350
    bar_y = 720
    bar_w = 700
    bar_h = 8

    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (bar_x, bar_y, bar_w, bar_h),
        border_radius=5
    )

    if current_file:

        duration = get_track_duration(current_file)

        pos_ms = pygame.mixer.music.get_pos()

        if pos_ms > 0 and duration > 0:

            progress = min(
                1.0,
                (pos_ms / 1000) / duration
            )

            pygame.draw.rect(
                screen,
                GREEN,
                (
                    bar_x,
                    bar_y,
                    int(bar_w * progress),
                    bar_h
                ),
                border_radius=5
            )

    # Visualizer
    visualizer.draw_wave(
        screen,
        samples,
        bass
    )

    # Play/Pause Button
    pygame.draw.circle(
        screen,
        GREEN,
        play_rect.center,
        35
    )

    if paused or not playing:

        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            [
                (play_rect.centerx - 8, play_rect.centery - 15),
                (play_rect.centerx - 8, play_rect.centery + 15),
                (play_rect.centerx + 15, play_rect.centery)
            ]
        )

    else:

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                play_rect.centerx - 12,
                play_rect.centery - 15,
                8,
                30
            )
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                play_rect.centerx + 4,
                play_rect.centery - 15,
                8,
                30
            )
        )

    # Prompt box
    pygame.draw.rect(
        screen,
        CARD,
        (300, HEIGHT - 50, WIDTH - 340, 40),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (300, HEIGHT - 50, WIDTH - 340, 40),
        2,
        border_radius=12
    )

    prompt_text = (
        prompt
        if prompt
        else "Type a music prompt and press Enter..."
    )

    screen.blit(
        font.render(
            prompt_text,
            True,
            WHITE
        ),
        (320, HEIGHT - 42)
    )

    pygame.display.flip()

pygame.quit()