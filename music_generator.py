import numpy as np
import wave
import random

SAMPLE_RATE = 44100


# -------------------------
# WAV SHAPES
# -------------------------

def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

def square(freq, t):
    return np.sign(np.sin(2 * np.pi * freq * t))


# -------------------------
# NOTE BUILDER
# -------------------------

def make_note(freqs, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    audio = np.zeros_like(t)

    for f in freqs:
        audio += sine(f, t)

    audio /= len(freqs)

    # envelope (removes clicks)
    envelope = np.sin(np.linspace(0, np.pi, len(audio)))

    return audio * envelope


# -------------------------
# DRUM BEAT
# -------------------------

def kick(dur):
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    return np.sin(2 * np.pi * 60 * t) * np.exp(-5 * t)

def snare(dur):
    noise = np.random.uniform(-1, 1, int(SAMPLE_RATE * dur))
    return noise * np.exp(-8 * np.linspace(0, dur, len(noise)))


# -------------------------
# TRACK BUILDER
# -------------------------

def build_track(chords, bpm=90):
    beat = 60 / bpm
    audio = []

    for i, chord in enumerate(chords):

        # chord
        audio.append(make_note(chord, beat))

        # simple drums
        if i % 2 == 0:
            audio[-1] += kick(beat)
        else:
            audio[-1] += snare(beat)

    return np.concatenate(audio)


# -------------------------
# PROMPT → MUSIC MAP
# -------------------------

def generate_music(prompt):

    prompt = prompt.lower()

    if "lofi" in prompt or "chill" in prompt:

        chords = [
            [220, 261, 330],
            [196, 247, 294],
            [174, 220, 261],
            [196, 247, 330],
        ] * 8

        bpm = 80

    elif "jazz" in prompt:

        chords = [
            [261, 311, 392],
            [246, 293, 370],
            [220, 277, 349],
            [196, 247, 330],
        ] * 8

        bpm = 110

    elif "rock" in prompt:

        chords = [
            [110, 165, 220],
            [110, 147, 196],
            [98, 147, 196],
            [110, 165, 220],
        ] * 10

        bpm = 140

    elif "sad" in prompt:

        chords = [
            [220, 261, 329],
            [196, 246, 311],
            [174, 220, 261],
        ] * 10

        bpm = 70

    else:

        base = [220, 247, 262, 294, 330, 349, 392]

        chords = [
            random.sample(base, 3)
            for _ in range(30)
        ]

        bpm = 100

    audio = build_track(chords, bpm)

    audio = audio / np.max(np.abs(audio)) * 32767

    audio = audio.astype(np.int16)

    filename = "generated_music.wav"

    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio.tobytes())

    return filename