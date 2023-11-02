import numpy as np
import matplotlib.pyplot as plt
import Arithmatic_operations as op

def plot_fourier(signal, sampling_frequency):
    # Generate a time vector for the signal
    duration = len(signal) / sampling_frequency
    time = np.linspace(0, duration, len(signal))

    # Apply Fourier transform
    frequency = np.fft.fftfreq(len(signal), 1 / sampling_frequency)
    amplitude_spectrum = np.abs(np.fft.fft(signal))
    phase_spectrum = np.angle(np.fft.fft(signal))

    # Plot frequency versus amplitude
    plt.subplot(2, 1, 1)
    plt.plot(frequency, amplitude_spectrum)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency vs Amplitude')

    # Plot frequency versus phase
    plt.subplot(2, 1, 2)
    plt.plot(frequency, phase_spectrum)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (radians)')
    plt.title('Frequency vs Phase')

    plt.tight_layout()
    plt.show()


def apply_modification(signal, amplitude, phase):
    modified_signal = op.multiplication(signal,amplitude)  # Multiply signal by amplitude
    modified_signal = op.multiplication(modified_signal, np.exp(1j * phase))  # Multiply by complex exponential with phase
    return modified_signal
