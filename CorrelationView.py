from tkinter import messagebox

import numpy as np

from TimeDomain import *
import tkinter as tk
import PlotDisplay as pd
import signal_io as sio
import main as t2
import ConvTest as covtest
import CompareSignal as cs
import ConvCorr as cc


class Correlationview:

    def __init__(self):
        self.signal1 = None
        self.root = None
        self.signal2 = None
        self.canva = None
        self.result = None

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
        signal = cc.convolution(self.signal1, self.signal2)
        self.result = signal
        self.canva.plot_single(signal, title="Convolution")

    def perform_correlation(self):
        if not self.validate_input(self.signal1):
            return

        if not self.validate_input(self.signal2):
            return

        correlation_signal = cc.correlation(self.signal1, self.signal2)
        correlation_indices, correlation_result, _ = correlation_signal.get_signal()
        self.canva.plot_single(correlation_signal, title="Correlation")
        self.result = correlation_signal

        cs.Compare_Signals('Point1 Correlation/CorrOutput.txt',correlation_indices,correlation_result)
        messagebox.showinfo("Correlation", "Correlation performed successfully!")

    def fast_convolution(self):
        if not self.validate_input(self.signal1):
            return

        if not self.validate_input(self.signal2):
            return

        signal = cc.fast_convolution(self.signal1, self.signal2)
        self.result = signal
        self.canva.plot_single(signal, title="Fast Convolution")
        
    def fast_correlation(self):
        if not self.validate_input(self.signal1):
            return

        if not self.validate_input(self.signal2):
            return

        correlation_signal = cc.fast_correlation(self.signal1, self.signal2)
        self.result = correlation_signal
        self.canva.plot_single(correlation_signal, title="Fast Correlation")
        
    def auto_correlation1(self):
        if not self.validate_input(self.signal1):
            return

        correlation_signal = cc.fast_correlation(self.signal1)
        self.result = correlation_signal
        self.canva.update_plot1(correlation_signal, title="Auto Correlation Signal 1")
        
    def auto_correlation2(self):
        if not self.canva.update_plot2(self.signal2, title="Auto Correlation Signal 2"):
            return

        correlation_signal = cc.fast_correlation(self.signal2)
        self.result = correlation_signal
        self.canva.plot_single(correlation_signal)
    
    def corr_test(self):
        if not self.result:
            messagebox.showerror("Can't compare", "Please perform convolution or correlation first")
            return
        comp = sio.get_file_path()
        indices, values, _ = self.result.get_signal()
        cs.Compare_Signals(comp,indices,values)
        messagebox.showinfo("Comparison", "Comparison performed successfully!")
    
    def conv_test(self):
        if not self.result:
            messagebox.showerror("Can't compare", "Please perform convolution first")
            return
        indices, values, _ = self.result.get_signal()
        covtest.ConvTest(indices,values)
        messagebox.showinfo("Comparison", "Comparison performed successfully!")
    
    def run(self):
        # Create GUI window
        root = tk.Tk()
        self.root = root
        root.title("Convolution & Correlation Signal Processing")
        root.geometry("1350x800")
        root.configure(bg="white")
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=5)

        control_frame = tk.LabelFrame(root, text="Signal Controls", font=("Arial", 10), bg='#F5F5F5', padx=5, pady=5)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        signal_frame = tk.LabelFrame(root, text="Signal preview", font=("Arial", 10), bg='#F5F5F5', padx=5, pady=5)
        signal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        self.canva = pd.PlotDisplay(signal_frame)


        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

        def load_signal1():
            self.load_signal1()
            self.canva.update_plot1(self.signal1)


        def load_signal2():
            self.load_signal2()
            self.canva.update_plot2(self.signal2)

        def clear():
            self.signal1 = None
            self.signal2 = None
            self.canva.clear()

        load_frame = tk.LabelFrame(control_frame, text="Signal Processing", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                   pady=5)
        load_frame.pack(pady=5)
        load_button1 = tk.Button(load_frame, text="Load Signal1", command=load_signal1, **button_style)
        load_button1.grid(row=0, column=0, padx=5, pady=5)

        load_button2 = tk.Button(load_frame, text="Load Signal2", command=load_signal2, **button_style)
        load_button2.grid(row=0, column=1, padx=5, pady=5)
        
        show_button = tk.Button(load_frame, text="Show Signals",
                                 command=lambda: self.canva.update_all(self.signal1, self.signal2), **button_style)
        show_button.grid(row=1, column=0, padx=5, pady=5)
        
        clear_button = tk.Button(load_frame, text="Clear", command=clear, **button_style)
        clear_button.grid(row=1, column=1, padx=5, pady=5)

        convolution_frame = tk.LabelFrame(control_frame, text="Convolution", font=("Arial", 14), bg='#F5F5F5', padx=5,pady=5)
        convolution_frame.pack(pady=5)

        convolution_button = tk.Button(convolution_frame, text="Calculate Convolution",
                                       command=self.perform_convolution, **button_style)
        convolution_button.grid(row=1, columnspan=2, pady=5)
        
        fast_convolution_button = tk.Button(convolution_frame, text="Fast Convolution",
                                        command=self.fast_convolution, **button_style)
        fast_convolution_button.grid(row=2, columnspan=2, pady=5)

        correlation_frame = tk.LabelFrame(control_frame, text="Correlation", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                          pady=5)
        correlation_frame.pack(pady=5)

        correlation_button = tk.Button(correlation_frame, text="Perform Correlation", command=self.perform_correlation,
                                       **button_style)
        correlation_button.grid(row=2, columnspan=2, pady=5)
        
        fast_correlation_button = tk.Button(correlation_frame, text="Fast Correlation",
                                        command=self.fast_correlation, **button_style)
        fast_correlation_button.grid(row=3, columnspan=2, pady=5)
        
        auto_correlation1_button = tk.Button(correlation_frame, text="Auto Correlation Signal 1",
                                        command=self.auto_correlation1, **button_style)
        auto_correlation1_button.grid(row=4, columnspan=2, pady=5)
        
        auto_correlation2_button = tk.Button(correlation_frame, text="Auto Correlation Signal 2",
                                        command=self.auto_correlation2, **button_style)
        auto_correlation2_button.grid(row=5, columnspan=2, pady=5)
        
        test_frame = tk.LabelFrame(control_frame, text="Test", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                          pady=5)
        test_frame.pack(pady=5)
        
        corr_test_button = tk.Button(test_frame, text="Compare Correlation", command=self.corr_test, **button_style)
        corr_test_button.grid(row=2, columnspan=2, pady=5)
        
        conv_test_button = tk.Button(test_frame, text="Compare Convolution", command=self.conv_test, **button_style)
        conv_test_button.grid(row=1, columnspan=2, pady=5)
        
        def show_result():
            if not self.result:
                messagebox.showerror("Can't show", "Please perform convolution or correlation first")
                return
            self.canva.plot_single(self.result)
        
        show_result = tk.Button(test_frame, text="Show Result", command=lambda: show_result, **button_style)
        show_result.grid(row=3, columnspan=2, pady=5)
        
        
        def close():
            self.root.quit()
            self.root.destroy()

        # Close the window when the user presses the X button on the window
        self.root.protocol("WM_DELETE_WINDOW", close)
        # Run the GUI
        self.root.mainloop()
        # t2.MainWindow().run()


if __name__ == "__main__":
    td = Correlationview()
    td.run()