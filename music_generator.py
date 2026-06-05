import numpy as np
import wave
import random

SR = 44100


def sine(f, t):
    return np.sin(2 * np.pi * f * t)


def make_layer(freqs, dur, amp=1.0):
    t = np.linspace(0, dur, int(SR * dur), False)
    return sum(sine(f, t) for f in freqs) / len(freqs) * amp


def drum_kick(dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    return np.sin(2 * np.pi * 60 * t) * np.exp(-5 * t)


def snare(dur):
    noise = np.random.uniform(-1, 1, int(SR * dur))
    return noise * np.exp(-8 * np.linspace(0, dur, len(noise)))


def generate_music(prompt):

    p = prompt.lower()

    if "lofi" in p or "chill" in p:

        chords = [
            [220, 261, 329],
            [196, 247, 294],
            [174, 220, 261],
        ]

        bpm = 80

    elif "jazz" in p:

        chords = [
            [261, 311, 392],
            [246, 293, 370],
            [220, 277, 349],
        ]

        bpm = 110

    elif "rock" in p:

        chords = [
            [110, 165, 220],
            [98, 147, 196],
            [110, 147, 220],
        ]

        bpm = 140

    elif "dark" in p or "cyber" in p:

        chords = [
            [65, 98, 130],
            [73, 110, 146],
            [65, 82, 130],
        ]

        bpm = 95

    else:

        base = [220, 247, 262, 294, 330, 349, 392]

        chords = [
            random.sample(base, 3)
            for _ in range(20)
        ]

        bpm = 100

    beat = 60 / bpm

    audio = []

    for i, ch in enumerate(chords):

        layer = make_layer(ch, beat)

        # drums for rhythm (VERY IMPORTANT FIX)
        if i % 2 == 0:
            layer += drum_kick(beat) * 0.4
        else:
            layer += snare(beat) * 0.3

        audio.append(layer)

    audio = np.concatenate(audio)

    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)

    file = "generated_music.wav"

    with wave.open(file, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(audio.tobytes())

    return file