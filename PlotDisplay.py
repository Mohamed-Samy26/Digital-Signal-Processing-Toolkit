import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from SignalData import SignalData

class PlotDisplay:
    def __init__(self, master):
        self.master = master
        self.figure, self.axes = plt.subplots(2, 1)  # Two subplots
        # set figure size to fit the window
        self.figure.set_figheight(6)
        self.figure.set_figwidth(8)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def update_plot(self, signal:SignalData):
        """Update the plot with the given signal data"""
        self.axes[0].clear()  # Clear the previous plot
        self.axes[1].clear()
        Xn, Yn, phase = signal.get_signal()  # Get the signal data
        if signal.signal_type == "TIME":
            self.axes[0].stem(Xn, Yn, use_line_collection=True)
            self.axes[0].set_title("Time Domain Signal")
            self.axes[0].set_xlabel("Time")
            self.axes[0].set_ylabel("Amplitude")
            self.axes[0].grid()
            self.axes[1].axis('off')
        elif signal.signal_type == "FREQ":
            # Plot frequency versus amplitude
            self.axes[0].bar(Xn, Yn)
            self.axes[0].set_xlabel('Frequency (Hz)')
            self.axes[0].set_ylabel('Amplitude')
            self.axes[0].set_title('Frequency vs Amplitude')
            
            # Plot frequency versus phase
            self.axes[1].bar(Xn, phase)
            self.axes[1].set_xlabel('Frequency (Hz)')
            self.axes[1].set_ylabel('Phase (radians)')
            self.axes[1].set_title('Frequency vs Phase')
            self.figure.tight_layout()
            
        self.canvas.draw()  # Redraw the canvas with the updated plot 
        
    def clear_plot(self):
        """Clear the plot"""
        self.axes[0].clear()
        self.axes[1].clear()
        self.canvas.draw()
    
    def compare_signals(self, signal1, signal2):
        # display the two signals in the same plot to compare them
        self.axes[0].clear()
        self.axes[1].clear()
        Xn1, Yn1, phase1 = signal1.get_signal()
        Xn2, Yn2, phase2 = signal2.get_signal()
        
        if signal1.signal_type == "TIME":
            self.axes[0].stem(Xn1, Yn1, use_line_collection=True, color='red')
            self.axes[0].stem(Xn2, Yn2, use_line_collection=True, color='green')
            self.axes[0].set_title("Time Domain Signal")
            self.axes[0].set_xlabel("Time")
            self.axes[0].set_ylabel("Amplitude")
    
        elif signal1.signal_type == "FREQ":
            # Plot frequency versus amplitude
            self.axes[0].bar(Xn1, Yn1, color='red')
            self.axes[0].bar(Xn2, Yn2, color='green')
            self.axes[0].set_xlabel('Frequency (Hz)')
            self.axes[0].set_ylabel('Amplitude')
            self.axes[0].set_title('Frequency vs Amplitude')
            
            # Plot frequency versus phase
            self.axes[1].bar(Xn1, phase1)
            self.axes[1].bar(Xn2, phase2)
            self.axes[1].set_xlabel('Frequency (Hz)')
            self.axes[1].set_ylabel('Phase (radians)')
            self.axes[1].set_title('Frequency vs Phase')
            self.figure.tight_layout()
            
        self.canvas.draw()
        
