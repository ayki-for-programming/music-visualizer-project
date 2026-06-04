# music_generator.py

import numpy as np
import wave

def generate_music(prompt):
    filename = "generated_music.wav"

    sample_rate = 44100
    duration = 5
    frequency = 440

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        False
    )

    audio = np.sin(
        2 * np.pi * frequency * t
    )

    audio = (audio * 32767).astype(np.int16)

    with wave.open(filename, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio.tobytes())

    return filename
