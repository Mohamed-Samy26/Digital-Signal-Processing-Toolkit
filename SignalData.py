from typing import List

from matplotlib import pyplot as plt
import numpy as np

class SignalData:
    
    def __init__(self, signal_type: str, is_periodic: bool, points: List[tuple]):        
        if signal_type not in ["FREQ", "TIME"]:
            raise ValueError("Signal type must be either FREQ or TIME")
        
        self.signal_type = signal_type
        self.is_periodic = is_periodic
        self.points = points
        self.num_samples = len(points)
    
    def __str__(self):
        return f"Signal Type: {self.signal_type}\nIs Periodic: {self.is_periodic}\nNumber of Samples: {self.num_samples}\nPoints: {self.points}"
    
    def plot_signal(self):
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
            # plt.bar(time, points[:, 0], use_line_collection=True)
            # plt.title("Frequency Domain Signal")
            # plt.xlabel("Frequency")
            # plt.ylabel("Amplitude")
            
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
        plt.show()


