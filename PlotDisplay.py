import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from SignalData import SignalData


class PlotDisplay:
    def __init__(self, master):
        self.master = master
        self.figure, self.axes = plt.subplots(2, 1)  # Two subplots
        # set figure size to fit the window
        self.SPACE_FACTOR = 0.9
        self.FIG_WIDTH = 10
        self.figure.set_figheight(7)
        self.figure.set_figwidth(self.FIG_WIDTH)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def calculate_bar_width(self, num_bars):
        return (self.FIG_WIDTH / num_bars) * (1 - self.SPACE_FACTOR)

    def plot_single(self, signal: SignalData):
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
            self.axes[1].axis("off")
        elif signal.signal_type == "FREQ":
            # Plot frequency versus amplitude
            width = self.calculate_bar_width(len(Xn))
            self.axes[0].bar(Xn, Yn, width=width)
            self.axes[0].set_xlabel("Frequency (Hz)")
            self.axes[0].set_ylabel("Amplitude")
            self.axes[0].set_title("Frequency vs Amplitude")

            # Plot frequency versus phase
            self.axes[1].bar(Xn, phase, width=width)
            self.axes[1].set_xlabel("Frequency (Hz)")
            self.axes[1].set_ylabel("Phase (radians)")
            self.axes[1].set_title("Frequency vs Phase")
            self.figure.tight_layout()

        self.canvas.draw()  # Redraw the canvas with the updated plot

    def clear_plot(self):
        """Clear the plot"""
        self.axes[0].clear()
        self.axes[1].clear()
        self.canvas.draw()

    def update_plot1(
        self, signal: SignalData, freq_type: ["AMP", "PHASE"] = "AMP", title: str = None
    ):
        """Update the plot with the given signal data"""
        self.axes[0].clear()  # Clear the previous plot
        Xn, Yn, phase = signal.get_signal()
        if signal.signal_type == "TIME":
            self.axes[0].stem(Xn, Yn, use_line_collection=True)
            if title:
                self.axes[0].set_title(title)
            else:
                self.axes[0].set_title("Time Domain Signal")
            self.axes[0].set_xlabel("Time")
            self.axes[0].set_ylabel("Amplitude")
            self.axes[0].grid()
        elif signal.signal_type == "FREQ":
            # Plot frequency versus amplitude
            width = self.calculate_bar_width(len(Xn))

            if freq_type == "AMP":
                self.axes[0].bar(Xn, Yn, width=width)
                self.axes[0].set_xlabel("Frequency (Hz)")
                self.axes[0].set_ylabel("Amplitude")
                if title:
                    self.axes[0].set_title(title)
                else:
                    self.axes[0].set_title("Frequency vs Amplitude")
            elif freq_type == "PHASE":
                self.axes[0].bar(Xn, phase, width=width)
                self.axes[0].set_xlabel("Frequency (Hz)")
                self.axes[0].set_ylabel("Phase (radians)")
                if title:
                    self.axes[0].set_title(title)
                else:
                    self.axes[0].set_title("Frequency vs Phase")

            self.figure.tight_layout()

        self.canvas.draw()  # Redraw the canvas with the updated plot

    def update_plot2(self, signal: SignalData, freq_type: ["AMP", "PHASE"] = "AMP", title: str = None):
        """Update the plot with the given signal data"""
        self.axes[1].clear()  # Clear the previous plot
        self.axes[1].axis("on")
        Xn, Yn, phase = signal.get_signal()
        if signal.signal_type == "TIME":
            self.axes[1].stem(Xn, Yn, use_line_collection=True)
            if title:
                self.axes[1].set_title(title)
            else:
                self.axes[1].set_title("Time Domain Signal")
            self.axes[1].set_xlabel("Time")
            self.axes[1].set_ylabel("Amplitude")
            self.axes[1].grid()
        elif signal.signal_type == "FREQ":
            # Plot frequency versus amplitude
            width = self.calculate_bar_width(len(Xn))

            if freq_type == "AMP":
                self.axes[1].bar(Xn, Yn, width=width)
                self.axes[1].set_xlabel("Frequency (Hz)")
                self.axes[1].set_ylabel("Amplitude")
                if title:
                    self.axes[1].set_title(title)
                else:
                    self.axes[1].set_title("Frequency vs Amplitude")
                
            elif freq_type == "PHASE":
                self.axes[1].bar(Xn, phase, width=width)
                self.axes[1].set_xlabel("Frequency (Hz)")
                self.axes[1].set_ylabel("Phase (radians)")
                
                if title:
                    self.axes[1].set_title(title)
                else:
                    self.axes[1].set_title("Frequency vs Phase")

            self.figure.tight_layout()

        self.canvas.draw()  # Redraw the canvas with the updated plot

    def update_all(
        self,
        signal1: SignalData,
        signal2: SignalData,
        freq_type1: ["AMP", "PHASE"] = "AMP",
        freq_type2: ["AMP", "PHASE"] = "AMP",
        title1: str = None,
        title2: str = None,
    ):
        """Update the plot with the given signal data"""
        self.axes[0].clear()
        self.axes[1].clear()
        self.update_plot1(signal1, freq_type1, title1)
        self.update_plot2(signal2, freq_type2, title2)
        self.canvas.draw()

    def compare_signals(self, signal1, signal2):
        # display the two signals in the same plot to compare them
        self.axes[0].clear()
        self.axes[1].clear()
        Xn1, Yn1, phase1 = signal1.get_signal()
        Xn2, Yn2, phase2 = signal2.get_signal()

        if signal1.signal_type == "TIME":
            self.axes[0].stem(Xn1, Yn1, use_line_collection=True, color="red")
            self.axes[0].stem(Xn2, Yn2, use_line_collection=True, color="green")
            self.axes[0].set_title("Time Domain Signal")
            self.axes[0].set_xlabel("Time")
            self.axes[0].set_ylabel("Amplitude")

        elif signal1.signal_type == "FREQ":
            # Plot frequency versus amplitude
            width = self.calculate_bar_width(len(Xn1))
            self.axes[0].bar(Xn1, Yn1, color="blue", width=width)
            self.axes[0].bar(Xn2, Yn2, color="green", witdh=width)
            self.axes[0].set_xlabel("Frequency (Hz)")
            self.axes[0].set_ylabel("Amplitude")
            self.axes[0].set_title("Frequency vs Amplitude")

            # Plot frequency versus phase
            self.axes[1].bar(Xn1, phase1, color="blue", width=width)
            self.axes[1].bar(Xn2, phase2, color="green")
            self.axes[1].set_xlabel("Frequency (Hz)")
            self.axes[1].set_ylabel("Phase (radians)")
            self.axes[1].set_title("Frequency vs Phase")
            self.figure.tight_layout()

        self.canvas.draw()
