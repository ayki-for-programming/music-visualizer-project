import pygame
import pyaudio
import numpy as np

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands
from album_art import AlbumArt
from renderer import Renderer

# ------------------
# PYGAME
# ------------------

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
)
pygame.display.set_caption("Music Visualizer")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)

# ------------------
# PROMPT
# ------------------

prompt = ""

music_loaded = False

# ------------------
# AUDIO STREAM
# ------------------

CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# ------------------
# SYSTEMS
# ------------------

visualizer = Visualizer(WIDTH, HEIGHT)

album_art = AlbumArt(WIDTH, HEIGHT)

renderer = Renderer(WIDTH, HEIGHT)

# ------------------
# LOOP
# ------------------

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if prompt.strip():

                    try:

                        music_file = generate_music(
                            prompt
                        )

                        pygame.mixer.music.load(
                            music_file
                        )

                        pygame.mixer.music.play()

                        music_loaded = True

                    except Exception as e:

                        print(
                            "Music generation error:",
                            e
                        )

                    prompt = ""

            elif event.key == pygame.K_BACKSPACE:

                prompt = prompt[:-1]

            else:

                prompt += event.unicode

    # ------------------
    # AUDIO INPUT
    # ------------------

    try:

        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        samples = np.frombuffer(
            data,
            dtype=np.int16
        )

    except:

        samples = np.zeros(CHUNK)

    # ------------------
    # ANALYSIS
    # ------------------

    bass, mids, highs = get_frequency_bands(
        samples
    )

    renderer.update(bass)

    # ------------------
    # DRAW
    # ------------------

    draw_space_background(screen)

    album_art.draw(screen)

    renderer.draw(screen)

    visualizer.draw_wave(
        screen,
        samples
    )

    # ------------------
    # PROMPT BAR
    # ------------------

    bar_height = 60

    pygame.draw.rect(
        screen,
        (30, 30, 45),
        (
            20,
            HEIGHT - 80,
            WIDTH - 40,
            bar_height
        ),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (120, 140, 200),
        (
            20,
            HEIGHT - 80,
            WIDTH - 40,
            bar_height
        ),
        2,
        border_radius=12
    )

    display_text = (
        prompt
        if prompt
        else "Type a music prompt and press Enter..."
    )

    color = (
        (255, 255, 255)
        if prompt
        else (150, 150, 150)
    )

    prompt_surface = font.render(
        display_text,
        True,
        color
    )

    screen.blit(
        prompt_surface,
        (
            40,
            HEIGHT - 63
        )
    )

    pygame.display.flip()

# ------------------
# CLEANUP
# ------------------

stream.stop_stream()
stream.close()

p.terminate()

pygame.mixer.music.stop()

pygame.quit()