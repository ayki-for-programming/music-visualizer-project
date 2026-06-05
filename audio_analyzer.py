import numpy as np

def get_frequency_bands(samples):

    fft = np.fft.rfft(samples)
    mag = np.abs(fft)

    bass = np.mean(mag[:50])
    mids = np.mean(mag[50:200])
    highs = np.mean(mag[200:])

    return bass, mids, highs