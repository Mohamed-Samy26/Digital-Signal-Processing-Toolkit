import cmath
import numpy as np

from SignalData import SignalData


class FourierTransform:
    
    def __init__(self):
        pass

    def DFT(self, signal: SignalData, sampling_frequency:int = 0) -> SignalData:
        N = len(signal.points)
        
        if sampling_frequency == 0:
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
    
    def modify_index(self, signal:SignalData, index:int, new_amplitude:float, new_phase:float):
        
        freq, amplitude, phase = signal.get_signal()
        if index < 0 or index >= len(amplitude):
            print("Invalid index.")
            return signal

        modified_amplitude = list(amplitude)
        modified_phase = list(phase)

        if new_amplitude is None and new_phase is None:
            print("Invalid input, amplitude and phase cannot both be None.")
            raise ValueError("Invalid input, amplitude and phase cannot both be None.")
        
        if new_amplitude is not None and new_amplitude < 0:
            print("Invalid amplitude.")
            raise ValueError("Invalid amplitude.")
        
        
        if new_amplitude is not None:
            modified_amplitude[index] = new_amplitude
            
        if new_phase is not None:
            modified_phase[index] = new_phase

        return SignalData(signal.signal_type, signal.is_periodic,
                          list(zip(freq, modified_amplitude, modified_phase)))

