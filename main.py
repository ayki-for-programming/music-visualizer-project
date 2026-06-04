import pygame
import pyaudio
import numpy as np

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands
from beat_detector import BeatDetector
from particle_system import ParticleSystem
from album_art import AlbumArt
from renderer import Renderer

# ------------------
# MUSIC GENERATION
# ------------------

prompt = input("Enter music prompt: ")

music_file = generate_music(prompt)

# ------------------
# PYGAME
# ------------------

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Music Visualizer")

clock = pygame.time.Clock()

pygame.mixer.music.load(music_file)
pygame.mixer.music.play()

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

detector = BeatDetector()

particles = ParticleSystem()

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
        continue

    # ------------------
    # ANALYSIS
    # ------------------

    bass, mids, highs = get_frequency_bands(samples)

    beat = detector.detect(samples)

    # ------------------
    # REACTIONS
    # ------------------

    if beat:

        particles.explode(
            WIDTH // 2,
            HEIGHT // 2
        )

    particles.update()

    renderer.update(bass)

    # ------------------
    # DRAW
    # ------------------

    screen.fill((10, 10, 20))

    album_art.draw(screen)

    renderer.draw(screen)

    visualizer.draw_wave(
        screen,
        samples
    )

    particles.draw(screen)

    pygame.display.flip()

# ------------------
# CLEANUP
# ------------------

stream.stop_stream()
stream.close()

p.terminate()

pygame.mixer.music.stop()

pygame.quit()