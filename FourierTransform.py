import cmath
from pprint import pprint
import numpy as np
import signal_io as sio
from typing import List, Tuple

from SignalData import SignalData


class FourierTransform:
    
    def __init__(self):
        pass

    def DFT(self, signal: SignalData, sampling_frequency = None) -> SignalData:
        N = len(signal.points)
        
        if sampling_frequency is None:
            sampling_frequency = N
        
        amplitudes = np.zeros(N, dtype=complex)

        for k in range(N):
            for n in range(N):
                e = cmath.exp(-2j * cmath.pi * k * n / N)
                value = signal.points[n][1] * e
                amplitudes[k] += value

        frequencies = np.arange(N) * (sampling_frequency / N)
        print(amplitudes)
        new_points = [(freq, abs(val), cmath.phase(val)) for freq, val in zip(frequencies, amplitudes)]
        new_signal = SignalData("FREQ", signal.is_periodic, new_points)
        return new_signal

    def IDFT(self, signal: SignalData) -> SignalData:
        
        if signal.signal_type == "TIME":
            return signal
        
        N = len(signal.points)
        points = []
        
        for n in range(N):
            re = 0
            im = 0
            for k, (freq, amp, phase) in enumerate(signal.points):
                angle = 2 * np.pi * k * n / N
                re += amp * np.cos(angle + phase)
                im += amp * np.sin(angle + phase)
            
            value = (n, (re + im * 1j))
            points.append(value)
        
        return SignalData("TIME", signal.is_periodic, points)
    
    def modify_amplitude(self, signal: SignalData, new_amplitude: float) -> SignalData:
        new_points = []
        for point in signal.points:
            new_points.append((point[0], new_amplitude, point[2]))
        new_signal = SignalData(signal.signal_type, signal.is_periodic, new_points)
        return new_signal
    
    def modify_phase(self, signal: SignalData, new_phase: float) -> SignalData:
        new_points = []
        for point in signal.points:
            new_points.append((point[0], point[1], new_phase))
        new_signal = SignalData(signal.signal_type, signal.is_periodic, new_points)
        return new_signal        
    
    def modify(self, signal: SignalData, new_amplitude: float, new_phase: float) -> SignalData:
        new_points = []
        for point in signal.points:
            new_points.append((point[0], new_amplitude, new_phase))
        new_signal = SignalData(signal.signal_type, signal.is_periodic, new_points)
        return new_signal
    
