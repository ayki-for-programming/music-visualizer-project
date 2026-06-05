import pygame
import numpy as np
import wave

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands

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

visualizer = Visualizer(WIDTH, HEIGHT)

prompt = ""
current_file = None
frame = 0

playing = False

# ------------------
# AUDIO READER (FIXED STREAMING)
# ------------------

def get_samples(file, pos):
    try:
        with wave.open(file, "rb") as wf:
            wf.setpos(min(pos, wf.getnframes() - 2048))
            data = wf.readframes(2048)
            return np.frombuffer(data, dtype=np.int16)
    except:
        return np.zeros(1024)

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

            if event.key == pygame.K_SPACE:

                if playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

                playing = not playing

            elif event.key == pygame.K_RETURN:

                if prompt.strip():

                    current_file = generate_music(prompt)
                    pygame.mixer.music.load(current_file)
                    pygame.mixer.music.play()

                    playing = True
                    frame = 0
                    prompt = ""

            elif event.key == pygame.K_BACKSPACE:
                prompt = prompt[:-1]

            else:
                prompt += event.unicode

    # ------------------
    # AUDIO SYNC
    # ------------------

    if current_file:
        samples = get_samples(current_file, frame)
        frame += 800
    else:
        samples = np.zeros(1024)

    # ------------------
    # BACKGROUND (Spotify dark)
    # ------------------

    screen.fill((10, 10, 15))

    pygame.draw.rect(screen, (18, 18, 25), (0, 0, WIDTH, HEIGHT))

    pygame.draw.rect(screen, (14, 14, 20), (260, 0, WIDTH-260, HEIGHT))

    # ------------------
    # TITLE
    # ------------------

    title = font.render("Now Playing", True, (255, 255, 255))
    screen.blit(title, (300, 30))

    # ------------------
    # WAVEFORM
    # ------------------

    bass, mids, highs = get_frequency_bands(samples)

    visualizer.draw_wave(screen, samples, bass)

    # ------------------
    # INPUT BAR
    # ------------------

    pygame.draw.rect(screen, (30, 30, 40), (40, HEIGHT - 80, WIDTH - 80, 50), border_radius=12)

    pygame.draw.rect(screen, (30, 215, 96), (40, HEIGHT - 80, WIDTH - 80, 50), 2, border_radius=12)

    text = prompt if prompt else "Type a music prompt..."
    screen.blit(font.render(text, True, (255, 255, 255)), (60, HEIGHT - 65))

    pygame.display.flip()

pygame.quit()