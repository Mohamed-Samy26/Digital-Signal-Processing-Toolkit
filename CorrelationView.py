from tkinter import messagebox

import numpy as np

from TimeDomain import *
import tkinter as tk
import PlotDisplay as pd
import signal_io as sio
import main as t2
import ConvTest as covtest
import CompareSignal as cs


class Correlationview:

    def __init__(self):
        self.signal1 = None
        self.root = None
        self.signal2 = None
        self.canva = None

    def load_signal1(self):
        # Load signal from file
        try:
            self.signal1 = sio.read_signal_file()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "Invalid file, error " + str(e))

    def load_signal2(self):
        # Load signal from file
        try:
            self.signal2 = sio.read_signal_file()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "Invalid file, error " + str(e))

    def validate_input(self,signal:SignalData):
        if not signal:
            tk.messagebox.showerror("Error", "Please load a signal first")
            return False
        else:
            return True

    def perform_convolution(self):
        if not self.validate_input(self.signal1):
            return

        if not self.validate_input(self.signal2):
            return
        # Perform convolution between signal1 and signal2
        indices_signal1,s1,_=self.signal1.get_signal()
        indices_signal2,s2,_ = self.signal2.get_signal()
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
        covtest.ConvTest(result_indices,result)
        signal=SignalData("TIME", False,points)
        # Plot the convolution result
        self.canva.plot_single(signal)

    def perform_correlation(self):
        if not self.validate_input(self.signal1):
            return

        if not self.validate_input(self.signal2):
            return

        indices_signal1, s1, _ = self.signal1.get_signal()
        indices_signal2, s2, _ = self.signal2.get_signal()

        # Perform correlation
        correlation_length = len(s1)
        correlation_result = [0] * correlation_length
        s1_sq= [x**2 for x in s1]
        s2_sq =[x**2 for x in s2]
        mult=np.sum(s1_sq)*np.sum(s2_sq)
        dom=np.sqrt(mult)
        for i in range(len(s1)):
            for j in range(len(s2)):
                correlation_result[i] += s1[j] * s2[(j+i)%len(s2)]
        correlation_indices = np.arange(0, len(s1))
        print(correlation_result)
        correlation_result=correlation_result/dom
        correlation_points = list(zip(correlation_indices, correlation_result))
        correlation_signal = SignalData("TIME", False, correlation_points)
        # Plot the correlation result
        self.canva.plot_single(correlation_signal)

        cs.Compare_Signals('Point1 Correlation/CorrOutput.txt',correlation_indices,correlation_result)
        messagebox.showinfo("Correlation", "Correlation performed successfully!")

    def run(self):
        # Create GUI window
        root = tk.Tk()
        self.root = root
        root.title("Convolution Signal Processing")
        root.geometry("1350x800")
        root.configure(bg="white")
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=5)

        control_frame = tk.LabelFrame(root, text="Signal Controls", font=("Arial", 10), bg='#F5F5F5', padx=5, pady=5)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        signal_frame = tk.LabelFrame(root, text="Signal preview", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        signal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        self.canva = pd.PlotDisplay(signal_frame)

        def update_canvas(signal:SignalData):
            if signal:
                self.canva.plot_single(signal)

        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

        def load_signal1():
            self.load_signal1()
            update_canvas(self.signal1)


        def load_signal2():
            self.load_signal2()
            update_canvas(self.signal2)

        load_frame = tk.LabelFrame(control_frame, text="Signal Processing", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                   pady=5)
        load_frame.pack(pady=5)
        load_button1 = tk.Button(load_frame, text="Load Signal1", command=load_signal1, **button_style)
        load_button1.grid(row=0, column=0, padx=5, pady=5)

        load_button2 = tk.Button(load_frame, text="Load Signal2", command=load_signal2, **button_style)
        load_button2.grid(row=0, column=1, padx=5, pady=5)

        convolution_frame = tk.LabelFrame(control_frame, text="Moving Average", font=("Arial", 14), bg='#F5F5F5', padx=5,pady=5)
        convolution_frame.pack(pady=5)

        convolution_button = tk.Button(convolution_frame, text="Calculate Convolution",
                                       command=self.perform_convolution, **button_style)
        convolution_button.grid(row=1, columnspan=2, pady=5)

        correlation_frame = tk.LabelFrame(control_frame, text="Correlation", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                          pady=5)
        correlation_frame.pack(pady=5)

        correlation_button = tk.Button(correlation_frame, text="Perform Correlation", command=self.perform_correlation,
                                       **button_style)
        correlation_button.grid(row=2, columnspan=2, pady=5)

        def close():
            self.root.quit()
            self.root.destroy()

        # Close the window when the user presses the X button on the window
        self.root.protocol("WM_DELETE_WINDOW", close)
        # Run the GUI
        self.root.mainloop()
        t2.MainWindow().run()


if __name__ == "__main__":
    td = Correlationview()
    td.run()