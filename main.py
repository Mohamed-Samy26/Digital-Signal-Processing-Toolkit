import tkinter as tk
import MultiSignalOperations as Ms
import SingleSignalOperations as Ss
import GenerateWindow as fw
import Frequency_Domain as freq_domain
import TimeDomainView as time_domain
import Quantize_Signal as quant_sig
import CorrelationView as correlation
class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Signal Processor")
        self.window.geometry("400x500")
        self.window.configure(bg="#f2f2f2")
        self.create_widgets()

    def create_widgets(self):
        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0, "width": 25}

        # Create Task1 Button
        button1 = tk.Button(self.window, text="Sinusoidal Signal Generation", command=self.open_signal_generation, **button_style)
        button1.pack(pady=10)

        # Create Single Signal Operation Button
        button2 = tk.Button(self.window, text="Single Signal Operation", command=self.open_single_signal_operation, **button_style)
        button2.pack(pady=10)

        # Create Multiple Signal Operation Button
        button3 = tk.Button(self.window, text="Multiple Signal Operation", command=self.open_multiple_signal_operation, **button_style)
        button3.pack(pady=10)

        # Create New Button
        button4 = tk.Button(self.window, text="Quantizer Signal", command=self.open_quantizer, **button_style)
        button4.pack(pady=10)

        # Create New Button
        button5 = tk.Button(self.window, text="Frequency Domain", command=self.open_freq_domain, **button_style)
        button5.pack(pady=10)
        
        # create time domain button
        button6 = tk.Button(self.window, text="Time Domain", command=self.open_time_domain, **button_style)
        button6.pack(pady=10)

        # create Correlation button
        button6 = tk.Button(self.window, text="Conv. & Correlation", command=self.open_correlation, **button_style)
        button6.pack(pady=10)

    def open_signal_generation(self):
        self.window.destroy()
        x = fw.SignalProcessingApp()
        x.run()

    def open_single_signal_operation(self):
        self.window.destroy()
        x = Ss.SingleSignalOperations()
        x.run()

    def open_multiple_signal_operation(self):
        self.window.destroy()
        x = Ms.MultiSignalOperations()

    def open_freq_domain(self):
        self.window.destroy()
        x = freq_domain.FrequencyDomain()
        x.run()

    def open_quantizer(self):
        self.window.destroy()
        x = quant_sig.SignalQuantizer().run_quantization()

    def open_time_domain(self):
        self.window.destroy()
        x = time_domain.TimeDomainView()
        x.run()

    def open_correlation(self):
        self.window.destroy()
        x = correlation.Correlationview()
        x.run()
        
    def close(self):
        self.window.quit()
        self.window.destroy()
        
    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.mainloop()


if __name__ == "__main__":
    window = MainWindow()
    window.run()
