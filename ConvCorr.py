import cmath
from SignalData import SignalData
import ConvTest as covtest
import numpy as np
import CompareSignal as cs
import FourierTransform as fr


def convolution(signal1: SignalData, signal2: SignalData):
    indices_signal1, s1, _ = signal1.get_signal()
    indices_signal2, s2, _ = signal2.get_signal()
    min_i_x = min(indices_signal1)
    max_i_x = max(indices_signal1)
    min_i_h = min(indices_signal2)
    max_i_h = max(indices_signal2)

    min_n = min_i_x + min_i_h
    max_n = max_i_x + max_i_h

    result = [0] * (max_n - min_n + 1)
    result_indices = list(range(min_n, max_n + 1))
    for n in range(min_n, max_n + 1):
        for i in range(min_i_x, max_i_x + 1):
            if n - i in indices_signal2:
                result[n - min_n] += s1[i - min_i_x] * s2[indices_signal2.index(n - i)]

    points = list(zip(result_indices, result))
    signal = SignalData("TIME", False, points)
    return signal


def correlation(signal1: SignalData, signal2: SignalData):
    _, s1, _ = signal1.get_signal()
    _, s2, _ = signal2.get_signal()

    # Perform correlation
    correlation_length = len(s1)
    correlation_result = [0] * correlation_length
    s1_sq = [x**2 for x in s1]
    s2_sq = [x**2 for x in s2]
    mult = np.sum(s1_sq) * np.sum(s2_sq)
    dom = np.sqrt(mult)
    for i in range(len(s1)):
        for j in range(len(s2)):
            correlation_result[i] += s1[j] * s2[(j + i) % len(s2)]
    correlation_indices = np.arange(0, len(s1))
    print(correlation_result)
    correlation_result = correlation_result / dom
    correlation_points = list(zip(correlation_indices, correlation_result))
    correlation_signal = SignalData("TIME", False, correlation_points)
    return correlation_signal


def complex_multi(signal1: SignalData, signal2: SignalData, conjugate1=False):
    if signal1.signal_type != signal2.signal_type != "FREQ":
        raise ValueError("Signals must be in the frequency domain.")
    # Multiply the two signals amplitudes in the frequency domain
    complex1 = signal1.complex() if not conjugate1 else signal1.conjugate()
    fft_result = np.multiply(complex1, signal2.complex())
    # Convert to polar form
    fft_result = [(abs(point), cmath.phase(point)) for point in fft_result]
    points = [
        (freq, amp, phase)
        for freq, (amp, phase) in zip(np.arange(0, len(fft_result)), fft_result)
    ]
    if conjugate1:
        # divide amplitude by N
        N = len(points)
        points = [(freq, amp / N, phase) for freq, amp, phase in points]
    return SignalData("FREQ", False, points)


def fast_convolution(signal1: SignalData, signal2: SignalData):
    ft = fr.FourierTransform()
    padding = len(signal1.get_signal()[1]) + len(signal2.get_signal()[1]) - 1

    padded_signal1 = SignalData(
        "TIME",
        False,
        list(
            zip(
                np.arange(0, padding),
                np.pad(
                    signal1.get_signal()[1],
                    (0, padding - len(signal1.get_signal()[1])),
                    "constant",
                ),
            )
        ),
    )
    padded_signal2 = SignalData(
        "TIME",
        False,
        list(
            zip(
                np.arange(0, padding),
                np.pad(
                    signal2.get_signal()[1],
                    (0, padding - len(signal2.get_signal()[1])),
                    "constant",
                ),
            )
        ),
    )

    min_i_x = min(signal1.get_signal()[0])
    min_i_h = min(signal2.get_signal()[0])
    min_n = min(min_i_x, min_i_h)
    
    fft_signal1 = ft.DFT(padded_signal1)
    fft_signal2 = ft.DFT(padded_signal2)
    result = ft.IDFT(complex_multi(fft_signal1, fft_signal2))
    
    # shift indices
    result_indices = [i + min_n for i in result.get_signal()[0]]
    result_points = list(zip(result_indices, result.get_signal()[1]))
    return SignalData("TIME", False, result_points)


def fast_correlation(signal1: SignalData, signal2: SignalData = None):
    if signal1.signal_type != signal2.signal_type != "TIME":
        raise ValueError("Signals must be in the time domain.")
    if signal2 is None:
        signal2 = signal1
    ft = fr.FourierTransform()
    if len(signal1) != len(signal2):
        padding = len(signal1) + len(signal2) - 1
        signal1 = SignalData(
                "TIME",
                False,
                list(
                    zip(
                        np.arange(0, padding),
                        np.pad(
                            signal1.get_signal()[1],
                            (0, padding - len(signal1.get_signal()[1])),
                            "constant",
                        ),
                    )
                ),
            )
        signal2 = SignalData(
            "TIME",
            False,
            list(
                zip(
                    np.arange(0, padding),
                    np.pad(
                        signal2.get_signal()[1],
                        (0, padding - len(signal2.get_signal()[1])),
                        "constant",
                    ),
                )
            ),
        )

    fft_signal1 = ft.DFT(signal1)
    fft_signal2 = ft.DFT(signal2)
    return ft.IDFT(complex_multi(fft_signal1, fft_signal2, True))


