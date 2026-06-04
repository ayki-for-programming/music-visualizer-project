import numpy as np

def get_frequency_bands(samples):

    fft = np.fft.rfft(samples)
    magnitude = np.abs(fft)

    bass = np.mean(magnitude[:50])
    mids = np.mean(magnitude[50:300])
    highs = np.mean(magnitude[300:])

    return bass, mids, highs
