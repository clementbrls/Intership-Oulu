import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from pydub import AudioSegment


def find_x_for_max_y(x_values, y_values):
    # find the index of the max value
    max_index = np.argmax(y_values)
    x_for_max_y = x_values[max_index]
    return x_for_max_y


def crosscorrelate(audio0, audio1):
    """
    Given two AudioSegment objects, returns the time lag (in milliseconds) between the two signals.

    Parameters:
    - audio0 (AudioSegment): The first audio signal.
    - audio1 (AudioSegment): The second audio signal.

    Returns:
    - lag (float): The time lag (in milliseconds) between the two signals.
    """

    sig0 = np.array(audio0.get_array_of_samples())
    sig1 = np.array(audio1.get_array_of_samples())

    sig0 = sig0 / np.max(sig0)
    sig1 = sig1 / np.max(sig1)

    corr = signal.correlate(sig0, sig1, 'full')
    lag = signal.correlation_lags(len(sig0), len(sig1), mode='full')

    lag = find_x_for_max_y(lag, corr) / audio0.frame_rate * 1000
    return lag
