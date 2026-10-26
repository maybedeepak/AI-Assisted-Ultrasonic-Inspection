import numpy as np
from scipy.signal import find_peaks


def detect_peaks(data):

    signal = data["Amplitude"].values

    peaks, _ = find_peaks(
        signal,
        height=0.2,
        distance=30
    )

    return peaks