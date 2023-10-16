from typing import List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SignalData import SignalData
import tkinter as tk
from comparesignals import SignalSamplesAreEqual

def sinusoidal(amplitude: float, phase_shift: float,
               analog_freq: float, sample_rate: float,
               duration: float, wave_choice: str):
    if sample_rate==0:
        sample_rate=analog_freq*3
    t = np.arange(0,sample_rate)

    if analog_freq == 0:
        signal = np.full_like(t, amplitude)  # Set signal to a constant value
    else:
        angular_freq = 2 * np.pi * analog_freq
        if wave_choice == "Sin":
            signal = amplitude * np.sin(angular_freq/sample_rate * t + phase_shift)
            SignalSamplesAreEqual("SinOutput.txt", 0.1, signal)
        else:
            signal = amplitude * np.cos(angular_freq/sample_rate * t + phase_shift)
            SignalSamplesAreEqual("CosOutput.txt", 0.1, signal)


    plt.plot(t, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    if wave_choice == "Sin":
        plt.title('Sin wave Signal')
    else:
        plt.title('Cos wave Signal')
    plt.grid(True)
    plt.show()

    plt.stem(t, signal, use_line_collection=True)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    if wave_choice == "Sin":
        plt.title('Sin wave Signal')
    else:
        plt.title('Cos wave Signal')
    plt.grid(True)
    plt.show()


def continuous(points: List[tuple]):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    fig_continuous = Figure(figsize=(5, 4), dpi=100)
    plot_continuous = fig_continuous.add_subplot(111)
    plot_continuous.plot(x, y, 'b-')
    plot_continuous.set_xlabel('X')
    plot_continuous.set_ylabel('Y')
    plot_continuous.set_title('Continuous Signal')
    plot_continuous.grid(True)

    return fig_continuous

def discrete(points: List[tuple]):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    fig_discrete = Figure(figsize=(5, 4), dpi=100)
    plot_discrete = fig_discrete.add_subplot(111)
    plot_discrete.stem(x, y, 'r')
    plot_discrete.set_xlabel('X')
    plot_discrete.set_ylabel('Y')
    plot_discrete.set_title('Discrete Signal')
    plot_discrete.grid(True)

    return fig_discrete

def draw_signal(signal_data: SignalData):
    fig_continuous = continuous(signal_data.points)
    fig_discrete = discrete(signal_data.points)
        
    # create a new window
    root = tk.Tk()
    root.title("Signal")
    root.geometry("1000x500")
    root.configure(bg='#F5F5F5')
    
    canvas_continuous = FigureCanvasTkAgg(fig_continuous, master=root)
    canvas_continuous.draw()
    canvas_continuous.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    canvas_discrete = FigureCanvasTkAgg(fig_discrete, master=root)
    canvas_discrete.draw()
    canvas_discrete.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
