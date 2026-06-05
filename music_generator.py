import numpy as np
import wave
import random

SAMPLE_RATE = 44100


def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)


def make_chord(freqs, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    audio = sum(sine(f, t) for f in freqs) / len(freqs)

    envelope = np.sin(np.linspace(0, np.pi, len(audio)))

    return audio * envelope


def generate_music(prompt):

    prompt = prompt.lower()

    if "lofi" in prompt:

        chords = [
            [220, 261, 330],
            [196, 247, 294],
            [174, 220, 261],
        ] * 10

        bpm = 80

    elif "jazz" in prompt:

        chords = [
            [261, 311, 392],
            [246, 293, 370],
            [220, 277, 349],
        ] * 10

        bpm = 110

    elif "rock" in prompt:

        chords = [
            [110, 165, 220],
            [98, 147, 196],
            [110, 147, 220],
        ] * 12

        bpm = 140

    else:

        base = [220, 247, 262, 294, 330, 349, 392]

        chords = [
            random.sample(base, 3)
            for _ in range(25)
        ]

        bpm = 100

    beat = 60 / bpm

    audio = np.concatenate([
        make_chord(ch, beat)
        for ch in chords
    ])

    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)

    file = "generated_music.wav"

    with wave.open(file, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio.tobytes())

    return file