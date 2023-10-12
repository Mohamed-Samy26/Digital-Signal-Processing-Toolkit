import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def draw_signal():
    # Get user inputs
    amplitude = float(amplitude_entry.get())
    phase_shift = float(phase_shift_entry.get())
    analog_freq = float(analog_freq_entry.get())
    sample_rate = float(sample_rate_entry.get())
    duration = float(duration_entry.get())

    t = np.arange(0, duration, 1/sample_rate)

    angular_freq = 2 * np.pi * analog_freq

    if wave_choice.get() == "Sin":
        signal = amplitude * np.sin(angular_freq * t + phase_shift)
    else:
        signal = amplitude * np.cos(angular_freq * t + phase_shift)

    plt.plot(t, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Sinusoidal or Cosinusoidal Signal')
    plt.grid(True)
    plt.show()

window = tk.Tk()
window.title("Sinusoidal or Cosinusoidal Signal Generator")

# Create labels and entry fields for user input
wave_choice_label = tk.Label(window, text="Wave choice:")
wave_choice_label.pack()
wave_choice = tk.StringVar(window)
wave_choice.set("Sine")
wave_choice_menu = tk.OptionMenu(window, wave_choice, "Sin", "Cos")
wave_choice_menu.pack()

amplitude_label = tk.Label(window, text="Amplitude:")
amplitude_label.pack()
amplitude_entry = tk.Entry(window)
amplitude_entry.pack()

phase_shift_label = tk.Label(window, text="Phase Shift:")
phase_shift_label.pack()
phase_shift_entry = tk.Entry(window)
phase_shift_entry.pack()

analog_freq_label = tk.Label(window, text="Analog Frequency (Hz):")
analog_freq_label.pack()
analog_freq_entry = tk.Entry(window)
analog_freq_entry.pack()

sample_rate_label = tk.Label(window, text="Sample Rate (Hz):")
sample_rate_label.pack()
sample_rate_entry = tk.Entry(window)
sample_rate_entry.pack()

duration_label = tk.Label(window, text="Duration (s):")
duration_label.pack()
duration_entry = tk.Entry(window)
duration_entry.pack()
generate_button = tk.Button(window, text="Generate Signal", command=draw_signal)
generate_button.pack()

window.mainloop()