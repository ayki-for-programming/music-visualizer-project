# music_generator.py

import numpy as np
import wave
import random

SAMPLE_RATE = 44100


# -------------------------
# BASIC WAVE FORMS
# -------------------------

def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

def square(freq, t):
    return np.sign(np.sin(2 * np.pi * freq * t))

def saw(freq, t):
    return 2 * (t * freq - np.floor(0.5 + t * freq))


# -------------------------
# SOUND SYNTH
# -------------------------

def make_tone(freq, duration, wave_type="sine"):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    if wave_type == "sine":
        audio = sine(freq, t)
    elif wave_type == "square":
        audio = square(freq, t)
    else:
        audio = saw(freq, t)

    # fade in/out to avoid clicks
    envelope = np.linspace(0, 1, len(audio))
    envelope = np.minimum(envelope, np.linspace(1, 0, len(audio)))

    return audio * envelope


def build_track(pattern):
    track = np.array([], dtype=np.float32)

    for freq, dur, wave_type in pattern:
        tone = make_tone(freq, dur, wave_type)
        track = np.concatenate((track, tone))

    # normalize
    if np.max(np.abs(track)) > 0:
        track = track / np.max(np.abs(track))

    return (track * 32767).astype(np.int16)


# -------------------------
# PROMPT → MUSIC MAPPING
# -------------------------

def generate_music(prompt):

    prompt = prompt.lower()

    # LOFI
    if "lofi" in prompt or "chill" in prompt:
        pattern = [
            (220, 0.4, "sine"),
            (196, 0.4, "sine"),
            (174, 0.6, "sine"),
            (196, 0.4, "sine"),
        ] * 8

    # JAZZ
    elif "jazz" in prompt:
        pattern = [
            (261, 0.3, "sine"),
            (311, 0.3, "sine"),
            (370, 0.3, "sine"),
            (440, 0.4, "sine"),
        ] * 10

    # ROCK
    elif "rock" in prompt:
        pattern = [
            (110, 0.2, "square"),
            (110, 0.2, "square"),
            (165, 0.2, "square"),
            (220, 0.2, "square"),
        ] * 12

    # DARK / CYBERPUNK
    elif "dark" in prompt or "cyber" in prompt:
        pattern = [
            (60, 0.5, "saw"),
            (65, 0.5, "saw"),
            (70, 0.5, "saw"),
            (65, 0.5, "saw"),
        ] * 8

    # HAPPY / POP
    elif "happy" in prompt or "pop" in prompt:
        pattern = [
            (261, 0.3, "sine"),
            (329, 0.3, "sine"),
            (392, 0.3, "sine"),
            (523, 0.3, "sine"),
        ] * 10

    # DEFAULT RANDOM MUSIC
    else:
        base_notes = [220, 247, 262, 294, 330, 349, 392]
        pattern = [
            (
                random.choice(base_notes),
                random.choice([0.2, 0.3, 0.4]),
                random.choice(["sine", "square"])
            )
            for _ in range(30)
        ]

    audio = build_track(pattern)

    filename = "generated_music.wav"

    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio.tobytes())

    return filename