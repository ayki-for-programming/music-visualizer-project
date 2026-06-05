import numpy as np


def get_frequency_bands(samples):
    if len(samples) < 64:
        return 0, 0, 0

    samples = samples.astype(np.float32)

    if len(samples.shape) > 1:
        samples = samples.mean(axis=1)

    fft = np.abs(np.fft.rfft(samples))

    if len(fft) < 10:
        return 0, 0, 0

    bass = np.mean(fft[:10]) / 10000
    mids = np.mean(fft[10:40]) / 10000
    highs = np.mean(fft[40:]) / 10000

    return (
        float(np.clip(bass, 0, 1)),
        float(np.clip(mids, 0, 1)),
        float(np.clip(highs, 0, 1)),
    )