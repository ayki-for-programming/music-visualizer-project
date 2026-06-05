import numpy as np
import pygame

SR = 44100


class DJEngine:
    def __init__(self):
        pygame.mixer.pre_init(SR, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.sounds = {}
        self._build()

    def noise(self, n):
        return np.random.uniform(-1, 1, n)

    def stereo(self, mono):
        mono = np.clip(mono, -1, 1)
        return np.column_stack((mono * 32767, mono * 32767)).astype(np.int16)

    # ---------------- KICK ----------------
    def kick(self, dur=0.35):
        t = np.linspace(0, dur, int(SR * dur), False)
        wave = np.sin(2 * np.pi * 60 * t) * np.exp(-8 * t)
        return self.stereo(wave)

    # ---------------- SNARE ----------------
    def snare(self, dur=0.2):
        n = self.noise(int(SR * dur))
        env = np.exp(-12 * np.linspace(0, dur, len(n)))
        return self.stereo(n * env)

    # ---------------- HIHAT ----------------
    def hihat(self, dur=0.1):
        n = self.noise(int(SR * dur))
        env = np.exp(-25 * np.linspace(0, dur, len(n)))
        return self.stereo(n * env)

    # ---------------- BASS ----------------
    def bass(self, dur=0.4):
        t = np.linspace(0, dur, int(SR * dur), False)
        wave = np.sin(2 * np.pi * 55 * t) * np.exp(-5 * t)
        return self.stereo(wave)

    # ---------------- CLAP (NEW) ----------------
    def clap(self, dur=0.18):
        n = self.noise(int(SR * dur))
        env = np.exp(-18 * np.linspace(0, dur, len(n)))
        clap = n * env + 0.3 * np.sin(2 * np.pi * 200 * np.linspace(0, dur, len(n)))
        return self.stereo(clap)

    # ---------------- OPEN HIHAT (NEW) ----------------
    def openhat(self, dur=0.25):
        n = self.noise(int(SR * dur))
        env = np.exp(-10 * np.linspace(0, dur, len(n)))
        return self.stereo(n * env)

    def _build(self):
        self.sounds = {
            "kick": pygame.sndarray.make_sound(self.kick()),
            "snare": pygame.sndarray.make_sound(self.snare()),
            "hihat": pygame.sndarray.make_sound(self.hihat()),
            "bass": pygame.sndarray.make_sound(self.bass()),
            "clap": pygame.sndarray.make_sound(self.clap()),
            "openhat": pygame.sndarray.make_sound(self.openhat()),
        }

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()