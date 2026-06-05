import numpy as np
import wave
import random

SR = 44100


# ------------------
# BASIC OSCILLATORS
# ------------------

def sine(freq, t):
    return np.sin(2 * np.pi * freq * t)


def square(freq, t):
    return np.sign(np.sin(2 * np.pi * freq * t))


# ------------------
# ENVELOPE
# ------------------

def envelope(n):

    attack = int(n * 0.1)
    decay = int(n * 0.15)

    attack_env = np.linspace(0, 1, attack)

    decay_env = np.linspace(1, 0.75, decay)

    sustain = np.ones(
        n - attack - decay
    ) * 0.75

    return np.concatenate([
        attack_env,
        decay_env,
        sustain
    ])


# ------------------
# CHORDS
# ------------------

def chord(freqs, dur):

    t = np.linspace(
        0,
        dur,
        int(SR * dur),
        False
    )

    audio = np.zeros(len(t))

    for f in freqs:
        audio += sine(f, t)

    audio /= len(freqs)

    env = envelope(len(audio))

    return audio * env * 0.5


# ------------------
# BASS
# ------------------

def bass_note(freq, dur):

    t = np.linspace(
        0,
        dur,
        int(SR * dur),
        False
    )

    audio = (
        sine(freq, t)
        + 0.3 * sine(freq / 2, t)
    )

    env = envelope(len(audio))

    return audio * env * 0.45


# ------------------
# MELODY
# ------------------

def melody_note(freq, dur):

    t = np.linspace(
        0,
        dur,
        int(SR * dur),
        False
    )

    audio = (
        0.8 * sine(freq, t)
        + 0.2 * square(freq * 2, t)
    )

    env = envelope(len(audio))

    return audio * env * 0.25


# ------------------
# DRUMS
# ------------------

def kick(dur):

    t = np.linspace(
        0,
        dur,
        int(SR * dur),
        False
    )

    pitch = 90 * np.exp(-6 * t)

    wave_data = np.sin(
        2 * np.pi * pitch * t
    )

    return wave_data * np.exp(-8 * t)


def snare(dur):

    noise = np.random.uniform(
        -1,
        1,
        int(SR * dur)
    )

    return noise * np.exp(
        -12 * np.linspace(
            0,
            dur,
            len(noise)
        )
    )


def hihat(dur):

    noise = np.random.uniform(
        -1,
        1,
        int(SR * dur)
    )

    return noise * np.exp(
        -70 * np.linspace(
            0,
            dur,
            len(noise)
        )
    )


# ------------------
# BUILD SECTION
# ------------------

def build_section(
    progression,
    bpm,
    melody_scale
):

    beat = 60 / bpm

    section = []

    for chord_notes in progression:

        layer = chord(
            chord_notes,
            beat
        )

        # bass root
        layer += bass_note(
            chord_notes[0] / 2,
            beat
        )

        # random melody
        mel_freq = random.choice(
            melody_scale
        )

        layer += melody_note(
            mel_freq,
            beat
        )

        # drums

        layer += hihat(
            beat
        ) * 0.05

        if random.random() < 0.6:
            layer += kick(
                beat
            ) * 0.35

        if random.random() < 0.45:
            layer += snare(
                beat
            ) * 0.20

        section.append(layer)

    return section


# ------------------
# MAIN GENERATOR
# ------------------

def generate_music(prompt):

    p = prompt.lower()

    # ------------------
    # LOFI
    # ------------------

    if (
        "lofi" in p
        or "study" in p
        or "calm" in p
    ):

        bpm = 72

        verse = [
            [220, 277, 330],
            [196, 247, 294],
            [174, 220, 261],
            [196, 247, 294]
        ]

        chorus = [
            [261, 330, 392],
            [220, 277, 330],
            [196, 247, 294],
            [174, 220, 261]
        ]

        melody = [
            261, 294, 330,
            349, 392, 440
        ]

    # ------------------
    # SAD
    # ------------------

    elif (
        "sad" in p
        or "rain" in p
        or "melancholy" in p
    ):

        bpm = 65

        verse = [
            [130, 165, 196],
            [146, 174, 220],
            [123, 155, 185],
            [146, 174, 220]
        ]

        chorus = [
            [196, 247, 294],
            [174, 220, 261],
            [146, 174, 220],
            [123, 155, 185]
        ]

        melody = [
            220, 247, 261,
            294, 330
        ]

    # ------------------
    # CYBERPUNK
    # ------------------

    elif (
        "cyber" in p
        or "dark" in p
        or "synth" in p
    ):

        bpm = 110

        verse = [
            [65, 98, 130],
            [73, 110, 146],
            [82, 123, 164],
            [73, 110, 146]
        ]

        chorus = [
            [130, 196, 261],
            [146, 220, 293],
            [164, 246, 329],
            [146, 220, 293]
        ]

        melody = [
            261, 293, 329,
            392, 440, 523
        ]

    # ------------------
    # ROCK / ENERGY
    # ------------------

    elif (
        "rock" in p
        or "angry" in p
        or "energy" in p
    ):

        bpm = 150

        verse = [
            [110, 165, 220],
            [98, 147, 196],
            [82, 123, 165],
            [98, 147, 196]
        ]

        chorus = [
            [165, 220, 330],
            [147, 196, 294],
            [123, 165, 247],
            [147, 196, 294]
        ]

        melody = [
            330, 392,
            440, 494,
            523
        ]

    # ------------------
    # DEFAULT
    # ------------------

    else:

        bpm = 100

        verse = [
            [220, 277, 330],
            [247, 311, 370],
            [262, 330, 392],
            [294, 370, 440]
        ]

        chorus = [
            [330, 415, 494],
            [294, 370, 440],
            [262, 330, 392],
            [247, 311, 370]
        ]

        melody = [
            261, 294,
            330, 349,
            392, 440
        ]

    # ------------------
    # SONG STRUCTURE
    # ------------------

    song = []

    song.extend(
        build_section(
            verse,
            bpm,
            melody
        )
    )

    song.extend(
        build_section(
            verse,
            bpm,
            melody
        )
    )

    song.extend(
        build_section(
            chorus,
            bpm,
            melody
        )
    )

    song.extend(
        build_section(
            verse,
            bpm,
            melody
        )
    )

    song.extend(
        build_section(
            chorus,
            bpm,
            melody
        )
    )

    # ------------------
    # RENDER
    # ------------------

    audio = np.concatenate(song)

    max_val = np.max(
        np.abs(audio)
    )

    if max_val > 0:
        audio /= max_val

    # stereo widening

    left = audio

    delay = 300

    right = np.roll(
        audio,
        delay
    )

    stereo = np.column_stack(
        (left, right)
    )

    stereo = (
        stereo * 32767
    ).astype(np.int16)

    filename = "generated_music.wav"

    with wave.open(
        filename,
        "wb"
    ) as f:

        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)

        f.writeframes(
            stereo.tobytes()
        )

    return filename