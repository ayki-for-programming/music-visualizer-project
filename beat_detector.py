import numpy as np

class BeatDetector:

    def __init__(self):
        self.prev_energy = 0

    def detect(self, samples):

        energy = np.mean(samples.astype(float) ** 2)

        beat = energy > self.prev_energy * 1.5

        self.prev_energy = energy

        return beat