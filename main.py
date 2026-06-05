import pygame
import numpy as np
import random

from music_generator import generate_music
from visualizer import Visualizer
from audio_analyzer import get_frequency_bands
from renderer import Renderer
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
font = pygame.font.SysFont(None, 32)

# ------------------
# STARS
# ------------------

stars = [
    [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
    for _ in range(150)
]

def draw_space(screen):
    screen.fill((0, 0, 0))

    for s in stars:
        s[1] += s[2] * 0.2
        if s[1] > HEIGHT:
            s[1] = 0
            s[0] = random.randint(0, WIDTH)

        pygame.draw.circle(screen, (255, 255, 255), (int(s[0]), int(s[1])), s[2])

# ------------------
# SYSTEMS
# ------------------

visualizer = Visualizer(WIDTH, HEIGHT)
renderer = Renderer(WIDTH, HEIGHT)
album = AlbumArt(WIDTH, HEIGHT)

# ------------------
# INPUT STATE
# ------------------

prompt = ""

running = True

# ------------------
# LOOP
# ------------------

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_RETURN:

                if prompt.strip():

                    music_file = generate_music(prompt)
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play()

                    prompt = ""

            elif event.key == pygame.K_BACKSPACE:
                prompt = prompt[:-1]

            else:
                prompt += event.unicode

    # ------------------
    # AUDIO (for visuals only)
    # ------------------

    samples = np.zeros(1024)
    bass, mids, highs = get_frequency_bands(samples)

    renderer.update(bass)

    # ------------------
    # DRAW
    # ------------------

    draw_space(screen)

    album.draw(screen)
    renderer.draw(screen)
    visualizer.draw_wave(screen, samples)

    # ------------------
    # PROMPT BAR
    # ------------------

    bar_h = 60

    pygame.draw.rect(
        screen,
        (20, 20, 30),
        (20, HEIGHT - 80, WIDTH - 40, bar_h),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (255, 80, 160),
        (20, HEIGHT - 80, WIDTH - 40, bar_h),
        2,
        border_radius=12
    )

    text = prompt if prompt else "Type a music prompt..."
    color = (255, 255, 255) if prompt else (150, 150, 150)

    screen.blit(
        font.render(text, True, color),
        (40, HEIGHT - 62)
    )

    pygame.display.flip()

pygame.quit()