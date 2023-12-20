from typing import List

from matplotlib import pyplot as plt
import numpy as np

class SignalData:
    
    def __init__(self, signal_type: str, is_periodic: bool, points: List[tuple]): 
        
        """Constructor for SignalData class which represents a signal in either the time or frequency domain.
        """
               
        if signal_type not in ["FREQ", "TIME"]:
            raise ValueError("Signal type must be either FREQ or TIME")
        
        self.signal_type = signal_type
        self.is_periodic = is_periodic
        self.points = points
        self.num_samples = len(points)
        if self.signal_type == "FREQ" and len(points[0]) == 2:
            self.points = [(point[0], point[1], 0) for point in points]
    
    def __str__(self):
        return f"Signal Type: {self.signal_type}\nIs Periodic: {self.is_periodic}\nNumber of Samples: {self.num_samples}\nPoints: {self.points}"
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, index):
        return self.points[index]
    
    def __setitem__(self, index, value):
        self.points[index] = value
        
    def __iter__(self):
        return iter(self.points)
    
    def __eq__(self, other):
        return self.points == other.points and self.signal_type == other.signal_type and self.is_periodic == other.is_periodic
    
    def get_figure(self):
        """Returns the figure of the signal"""
        Xn = [point[0] for point in self.points]
        Yn = [point[1] for point in self.points]
        phase = None
        if self.signal_type == "FREQ":
            phase = [point[2] for point in self.points]
        plt.figure(figsize=(10, 5))

        if self.signal_type == "TIME":
            plt.stem(Xn, Yn, use_line_collection=True)
            plt.title("Time Domain Signal")
            plt.xlabel("Time")
            plt.ylabel("Amplitude")
        elif self.signal_type == "FREQ":
                        
            # Plot frequency versus amplitude
            plt.subplot(2, 1, 1)
            plt.bar(Xn, Yn)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.title('Frequency vs Amplitude')
            
            # Plot frequency versus phase
            plt.subplot(2, 1, 2)
            plt.bar(Xn, phase)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Phase (radians)')
            plt.title('Frequency vs Phase')
            
            plt.tight_layout()
            
        plt.grid()
        return plt

    def plot_signal(self):
        """Plot signal in time or frequency domain depending on signal type"""
        self.get_figure().show()

    def get_signal(self):
        """Returns the signal as a tuple of lists (Xn, Yn, phase)
            Xn: time or frequency (depending on signal type / domain)
            Yn: amplitude
            phase: phase angle (only for frequency domain signals)
        """
        Xn = [point[0] for point in self.points]
        Yn = [point[1] for point in self.points]
        phase = None
        if self.signal_type == "FREQ":
            try:
                phase = [point[2] for point in self.points]
            except IndexError:
                phase = [0 for _ in range(len(Xn))]
        return Xn, Yn, phase
  
    def conjugate(self):
        if self.signal_type == "TIME":
            raise ValueError("Cannot get conjugate of a time domain signal.")
        freq, amplitude, phase = self.get_signal()
        conjugate = [(freq, np.conjugate(val)) for freq, val in zip(freq, amplitude)]
        return SignalData("FREQ", phase.is_periodic, conjugate)
