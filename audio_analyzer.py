import numpy as np


def get_frequency_bands(samples):

    if len(samples) < 128:
        return 0.0, 0.0, 0.0

    try:

        samples = samples.astype(np.float32)

        # Stereo → Mono
        if len(samples.shape) > 1:

            samples = np.mean(
                samples,
                axis=1
            )

        # Remove DC offset
        samples = samples - np.mean(samples)

        # FFT
        fft = np.fft.rfft(samples)

        magnitude = np.abs(fft)

        if len(magnitude) < 10:
            return 0.0, 0.0, 0.0

        bass = np.mean(
            magnitude[:40]
        )

        mids = np.mean(
            magnitude[40:200]
        )

        highs = np.mean(
            magnitude[200:]
        )

        # Normalize
        bass = np.clip(
            bass / 50000,
            0,
            1
        )

        mids = np.clip(
            mids / 30000,
            0,
            1
        )

        highs = np.clip(
            highs / 20000,
            0,
            1
        )

        return bass, mids, highs

    except Exception as e:

        print(
            "FFT error:",
            e
        )

        return 0.0, 0.0, 0.0