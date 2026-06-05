import numpy as np
import wave
import random

SR = 44100


def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)


def envelope(n):
    attack = np.linspace(0, 1, n // 8)
    decay = np.linspace(1, 0.6, n // 8)
    sustain = np.ones(n - len(attack) - len(decay))
    return np.concatenate([attack, decay, sustain])


def chord(freqs, dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    audio = sum(sine(f, t) for f in freqs) / len(freqs)

    env = envelope(len(audio))
    return audio[:len(env)] * env


def kick(dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    return np.sin(2 * np.pi * 60 * t) * np.exp(-6 * t)


def snare(dur):
    noise = np.random.uniform(-1, 1, int(SR * dur))
    return noise * np.exp(-10 * np.linspace(0, dur, len(noise)))


def generate_music(prompt):

    p = prompt.lower()

    # 🎧 LOFI / STUDY
    if "lofi" in p or "study" in p or "calm" in p:
        chords = [[220, 261, 329], [196, 247, 294], [174, 220, 261]]
        bpm = 75

    # 🌧️ SAD / RAIN
    elif "sad" in p or "rain" in p:
        chords = [[130, 165, 196], [146, 174, 220], [123, 155, 185]]
        bpm = 65

    # 🌌 CYBER / DARK
    elif "cyber" in p or "dark" in p:
        chords = [[65, 98, 130], [73, 110, 146], [82, 123, 164]]
        bpm = 95

    # 🔥 ENERGY / ROCK
    elif "rock" in p or "angry" in p:
        chords = [[110, 165, 220], [98, 147, 196], [82, 123, 165]]
        bpm = 150

    # 🎲 DEFAULT
    else:
        base = [220, 247, 262, 294, 330, 349, 392]
        chords = [random.sample(base, 3) for _ in range(12)]
        bpm = 100

    beat = 60 / bpm

    audio = []

    for i, c in enumerate(chords):

        layer = chord(c, beat)

        # drum groove (this is what makes it feel “real”)
        if i % 2 == 0:
            layer += kick(beat) * 0.35
        else:
            layer += snare(beat) * 0.25

        audio.append(layer)

    audio = np.concatenate(audio)

    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)

    filename = "generated_music.wav"

    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(audio.tobytes())

    return filename