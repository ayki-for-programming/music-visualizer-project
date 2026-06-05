import numpy as np
import pygame

SR = 44100


class DJEngine:
    def __init__(self):
        pygame.mixer.pre_init(SR, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

        self.sounds = {}
        self.make_sounds()

    # -------------------------
    # SOUND SYNTHS
    # -------------------------

    def sine(self, freq, t):
        return np.sin(2 * np.pi * freq * t)

    def noise(self, n):
        return np.random.uniform(-1, 1, n)

    def to_stereo(self, mono):
        mono = np.clip(mono, -1, 1)
        audio = (mono * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return stereo

    # -------------------------
    # INSTRUMENTS
    # -------------------------

    def kick(self, dur=0.4):
        t = np.linspace(0, dur, int(SR * dur), False)
        tone = np.sin(2 * np.pi * 60 * t) * np.exp(-8 * t)
        return self.to_stereo(tone)

    def snare(self, dur=0.25):
        n = self.noise(int(SR * dur))
        env = np.exp(-12 * np.linspace(0, dur, len(n)))
        return self.to_stereo(n * env)

    def hihat(self, dur=0.12):
        n = self.noise(int(SR * dur))
        env = np.exp(-25 * np.linspace(0, dur, len(n)))
        return self.to_stereo(n * env)

    def bass(self, dur=0.4, freq=55):
        t = np.linspace(0, dur, int(SR * dur), False)
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
        return self.to_stereo(wave)

    # -------------------------
    # CACHE SOUNDS
    # -------------------------

    def make_sounds(self):
        self.sounds["kick"] = pygame.sndarray.make_sound(self.kick())
        self.sounds["snare"] = pygame.sndarray.make_sound(self.snare())
        self.sounds["hihat"] = pygame.sndarray.make_sound(self.hihat())
        self.sounds["bass"] = pygame.sndarray.make_sound(self.bass())

    # -------------------------
    # PLAY
    # -------------------------

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()