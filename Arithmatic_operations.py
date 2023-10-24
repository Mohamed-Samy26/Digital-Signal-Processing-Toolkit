from SignalData import SignalData
import generate_signal as gs
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import generate_signal as gs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw(result):
    fig_continuous = gs.continuous(result)
    fig_discrete = gs.discrete(result)

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


def addition(signal1, signal2):
    result = []
    max_size = max(len(signal1), len(signal2))

    for i in range(max_size):
        if i >= len(signal1):
            result.append((signal2[i][0], signal2[i][1]))
        elif i >= len(signal2):
            result.append((signal1[i][0], signal1[i][1]))
        else:
            result.append((signal1[i][0], signal1[i][1] + signal2[i][1]))
    draw(result)

def subtraction(signal1, signal2):
    result = []
    max_size = max(len(signal1), len(signal2))

    for i in range(max_size):
        if i >= len(signal1):
            result.append((signal2[i][0], signal2[i][1]))
        elif i >= len(signal2):
            result.append((signal1[i][0], signal1[i][1]))
        else:
            result.append((signal1[i][0], abs(signal1[i][1] - signal2[i][1])))

    draw(result)

def multiplication(signal1, constant):
    result = []

    for i in range(len(signal1)):
       result.append((signal1[i][0],signal1[i][1]*constant))

    draw(result)

def square(signal1, signal2):
    result1 = []
    result2 = []

    for i in range(len(signal1)):
       result1.append((signal1[i][0],signal1[i][1]*signal1[i][1]))

    for i in range(len(signal2)):
       result2.append((signal2[i][0],signal2[i][1]*signal2[i][1]))

    draw(result1)

    draw(result2)
    
def shift(signal, shift_value):
    result = []
    for i in range(len(signal)):
        result.append((signal[i][0]+shift_value,signal[i][1]))
    draw(result)

def normalizeZeroToOne(signal):
    result = []
    max = signal[0][1]
    min = signal[0][1]
    for i in range(len(signal)):
        if signal[i][1] > max:
            max = signal[i][1]
        if signal[i][1] < min:
            min = signal[i][1]
    for i in range(len(signal)):
        result.append((signal[i][0],(signal[i][1]-min)/(max-min)))
    draw(result)
    
def normalizeMinusOneToOne(signal):
    result = []
    max = signal[0][1]
    min = signal[0][1]
    for i in range(len(signal)):
        if signal[i][1] > max:
            max = signal[i][1]
        if signal[i][1] < min:
            min = signal[i][1]
    for i in range(len(signal)):
        result.append((signal[i][0],((signal[i][1]-min)/(max-min))*2-1))
    draw(result)
    
def accumulate(signal):
    result = []
    sum = 0
    for i in range(len(signal)):
        sum += signal[i][1]
        result.append((signal[i][0],sum))
    draw(result)