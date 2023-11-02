import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import generate_signal as gs
import signal_io as sio
import main as t2

class SignalProcessingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Signal Processing")
        self.root.geometry("600x800")
        self.root.configure(bg='#F5F5F5')

        self.create_menu()
        self.create_input_frame()
        self.create_generate_button()
        self.create_open_file_button()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def create_input_frame(self):
        input_frame = tk.LabelFrame(self.root, text="Signal Parameters", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
        input_frame.pack(pady=20)

        signal_choice_label = tk.Label(input_frame, text="Signal Generation:", font=("Arial", 14), bg='#F5F5F5')
        signal_choice_label.pack(pady=10)

        signal_choice = tk.StringVar(input_frame)
        signal_choice.set("Sin")
        signal_choice_menu = tk.OptionMenu(input_frame, signal_choice, "Sin", "Cos")
        signal_choice_menu.config(font=("Arial", 12))
        signal_choice_menu.pack()

        amplitude_label = tk.Label(input_frame, text="Amplitude:", font=("Arial", 14), bg='#F5F5F5')
        amplitude_label.pack(pady=10)
        self.amplitude_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.amplitude_entry.pack()

        phase_shift_label = tk.Label(input_frame, text="Phase Shift:", font=("Arial", 14), bg='#F5F5F5')
        phase_shift_label.pack(pady=10)
        self.phase_shift_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.phase_shift_entry.pack()

        analog_freq_label = tk.Label(input_frame, text="Analog Frequency (Hz):", font=("Arial", 14), bg='#F5F5F5')
        analog_freq_label.pack(pady=10)
        self.analog_freq_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.analog_freq_entry.pack()

        sample_rate_label = tk.Label(input_frame, text="Sample Rate (Hz):", font=("Arial", 14), bg='#F5F5F5')
        sample_rate_label.pack(pady=10)
        self.sample_rate_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.sample_rate_entry.pack()

    def create_generate_button(self):
        generate_button = tk.Button(self.root, text="Generate Signal", command=self.generate_signal)
        generate_button.config(font=("Arial", 14), bg='#4CAF50', fg='#FFFFFF', padx=20, pady=10)
        generate_button.pack(pady=20)

    def validate_input(self):
        try:
            float(self.amplitude_entry.get())
            float(self.phase_shift_entry.get())
            float(self.analog_freq_entry.get())
            float(self.sample_rate_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input value")
            return False
        return True

    def generate_signal(self):
        if self.validate_input():
            gs.sinusoidal(
                float(self.amplitude_entry.get()),
                float(self.phase_shift_entry.get()),
                float(self.analog_freq_entry.get()),
                float(self.sample_rate_entry.get()),
                self.signal_choice.get()
            )

    def create_open_file_button(self):
        open_file_button = tk.Button(self.root, text="Open File", command=lambda: sio.choose_file())
        open_file_button.config(font=("Arial", 14), bg='#4CAF50', fg='#FFFFFF', padx=20, pady=10)
        open_file_button.pack(pady=20)

    def run(self):
        self.root.mainloop()
        t2.MainWindow().run()

if __name__ == "__main__":
    app = SignalProcessingApp()
    app.run()