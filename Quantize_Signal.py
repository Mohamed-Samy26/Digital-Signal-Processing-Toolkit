import numpy as np
import math
import tkinter as tk
from tkinter import filedialog
from QuanTest2 import QuantizationTest2
from QuanTest1 import QuantizationTest1
import main as mainWindow
class SignalQuantizer:
    def __init__(self):
        self.filename = None
        self.signal = None

    def choose_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        print(self.filename)
        if self.filename:
            self.signal = self._read_signal_from_file()

    def _read_signal_from_file(self):
        x = []
        y = []
        index = 0
        with open(self.filename, 'r') as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2:
                    x.append(float(values[0]))
                    y.append(float(values[1]))
                elif index > 2:
                    break
                index += 1
        return np.array(y)

    def quantize_signal(self, levels):
        min_amp = np.min(self.signal)
        max_amp = np.max(self.signal)
        delta = (max_amp - min_amp) / levels

        mid_points = np.linspace(min_amp + delta / 2, max_amp - delta / 2, levels)

        quantized_signal = np.zeros_like(self.signal)

        bits_per_sample = math.ceil(math.log2(levels))
        encoded_signal = []
        encoded_signal_i = []
        for i, sample in enumerate(self.signal):
            sample -= 0.00001
            index = np.abs(mid_points - sample).argmin()
            encoded_signal_i.append(index + 1)
            quantized_signal[i] = mid_points[index]
            binary_sample = format(index, f"0{bits_per_sample}b")
            encoded_signal.append(binary_sample)
        quantization_error = quantized_signal - self.signal

        return quantized_signal, quantization_error, encoded_signal, encoded_signal_i

    def run_quantization(self):
        def start_quantization():
            if self.signal.size == 0:
                tk.messagebox.showerror("Error", "Please choose an input file.")
                return

            if level_var.get() == 1:
                num_of_levels = int(level_entry.get())
                quantized_signal, quantization_error, encoded_signal, encoded_signal_i = self.quantize_signal(num_of_levels)
                QuantizationTest2("Quan2_Out.txt", encoded_signal_i, encoded_signal, quantized_signal, quantization_error)
            else:
                num_of_bits = int(bits_entry.get())
                num_of_levels = 2 ** num_of_bits
                quantized_signal, quantization_error, encoded_signal, encoded_signal_i = self.quantize_signal(num_of_levels)
                QuantizationTest1("Quan1_Out.txt", encoded_signal, quantized_signal)

        root = tk.Tk()
        root.title("Signal Quantizer")
        root.geometry("400x300")

        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

        choose_file_button = tk.Button(root, text="Choose File", command=self.choose_file, **button_style)
        choose_file_button.pack(pady=10)

        level_frame = tk.LabelFrame(root, text="Quantization Levels", font=("Arial", 12))
        level_frame.pack(pady=10)

        level_var = tk.IntVar()
        level_var.set(1)

        level_radio = tk.Radiobutton(level_frame, text="Levels", variable=level_var, value=1, font=("Arial", 12))
        level_radio.pack()

        level_entry_label = tk.Label(level_frame, text="Number of Levels:", font=("Arial", 12))
        level_entry_label.pack()
        level_entry = tk.Entry(level_frame, font=("Arial", 12))
        level_entry.pack()

        bits_radio = tk.Radiobutton(level_frame, text="Bits", variable=level_var, value=2, font=("Arial", 12))
        bits_radio.pack()

        bits_entry_label = tk.Label(level_frame, text="Number of Bits:", font=("Arial", 12))
        bits_entry_label.pack()
        bits_entry = tk.Entry(level_frame, font=("Arial", 12))
        bits_entry.pack()

        start_button = tk.Button(root, text="Start Quantization", command=start_quantization, **button_style)
        start_button.pack(pady=10)

        root.mainloop()
        mainWindow.MainWindow().run()

