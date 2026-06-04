# music_generator.py

import numpy as np
import wave

SAMPLE_RATE = 44100


def note(freq, duration):

    t = np.linspace(
        0,
        duration,
        int(SAMPLE_RATE * duration),
        False
    )

    wave_data = np.sin(
        2 * np.pi * freq * t
    )

    envelope = np.linspace(
        1,
        0.3,
        len(wave_data)
    )

    return wave_data * envelope


def generate_song(notes):

    audio = np.array([])

    for freq, dur in notes:

        audio = np.concatenate([
            audio,
            note(freq, dur)
        ])

    audio = (
        audio / np.max(np.abs(audio))
        * 32767
    )

    return audio.astype(np.int16)


def generate_music(prompt):

    prompt = prompt.lower()

    if "lofi" in prompt:

        notes = [
            (261.63, 0.5),
            (329.63, 0.5),
            (392.00, 0.5),
            (329.63, 0.5),
            (261.63, 0.8),
            (196.00, 0.8),
        ] * 6

    elif "jazz" in prompt:

        notes = [
            (261.63, 0.3),
            (311.13, 0.3),
            (392.00, 0.4),
            (466.16, 0.4),
            (349.23, 0.3),
            (440.00, 0.5),
        ] * 6

    elif "rock" in prompt:

        notes = [
            (196.00, 0.2),
            (196.00, 0.2),
            (293.66, 0.2),
            (392.00, 0.2),
            (293.66, 0.2),
            (196.00, 0.2),
        ] * 10

    elif "sad" in prompt:

        notes = [
            (220.00, 0.8),
            (261.63, 0.8),
            (293.66, 0.8),
            (261.63, 0.8),
        ] * 6

    else:

        notes = [
            (261.63, 0.4),
            (293.66, 0.4),
            (329.63, 0.4),
            (392.00, 0.4),
        ] * 8

    audio = generate_song(notes)

    filename = "generated_music.wav"

    with wave.open(filename, "w") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(
            audio.tobytes()
        )

    return filename