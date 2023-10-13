import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import generate_signal as gs
import signal_io as sio


# main window

root = tk.Tk()
root.title("Signal Processing")
root.geometry("600x800")
root.configure(bg='#F5F5F5')

# menu bar

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# create a label frame to group the input fields together
input_frame = tk.LabelFrame(root, text="Signal Parameters", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
input_frame.pack(pady=20)

# # signal type

# signal_type_label = tk.Label(input_frame, text="Signal Type:", font=("Arial", 14), bg='#F5F5F5')
# signal_type_label.pack(pady=10)
# signal_type = tk.StringVar(input_frame)
# signal_type.set("Continuous")
# signal_type_menu = tk.OptionMenu(input_frame, signal_type, "Continuous", "Discrete")
# signal_type_menu.config(font=("Arial", 12))
# signal_type_menu.pack()

# signal choice

signal_choice_label = tk.Label(input_frame, text="Signal Generation:", font=("Arial", 14), bg='#F5F5F5')
signal_choice_label.pack(pady=10)
signal_choice = tk.StringVar(input_frame)
signal_choice.set("Sin")
signal_choice_menu = tk.OptionMenu(input_frame, signal_choice, "Sin", "Cos")
signal_choice_menu.config(font=("Arial", 12))
signal_choice_menu.pack()



# amplitude

amplitude_label = tk.Label(input_frame, text="Amplitude:", font=("Arial", 14), bg='#F5F5F5')
amplitude_label.pack(pady=10)
amplitude_entry = tk.Entry(input_frame, font=("Arial", 12))
amplitude_entry.pack()

# phase shift

phase_shift_label = tk.Label(input_frame, text="Phase Shift:", font=("Arial", 14), bg='#F5F5F5')
phase_shift_label.pack(pady=10)
phase_shift_entry = tk.Entry(input_frame, font=("Arial", 12))
phase_shift_entry.pack()

# analog frequency

analog_freq_label = tk.Label(input_frame, text="Analog Frequency (Hz):", font=("Arial", 14), bg='#F5F5F5')
analog_freq_label.pack(pady=10)
analog_freq_entry = tk.Entry(input_frame, font=("Arial", 12))
analog_freq_entry.pack()

# sample rate

sample_rate_label = tk.Label(input_frame, text="Sample Rate (Hz):", font=("Arial", 14), bg='#F5F5F5')
sample_rate_label.pack(pady=10)
sample_rate_entry = tk.Entry(input_frame, font=("Arial", 12))
sample_rate_entry.pack()

# duration

duration_label = tk.Label(input_frame, text="Duration (s):", font=("Arial", 14), bg='#F5F5F5')
duration_label.pack(pady=10)
duration_entry = tk.Entry(input_frame, font=("Arial", 12))
duration_entry.pack()

# generate button

def validate_input():
    try:
        float(amplitude_entry.get())
        float(phase_shift_entry.get())
        float(analog_freq_entry.get())
        float(sample_rate_entry.get())
        float(duration_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Invalid input value")
        return False
    return True

def generate_signal():
    if validate_input():
        gs.sinusoidal(float(amplitude_entry.get()),
                       float(phase_shift_entry.get()),
                       float(analog_freq_entry.get()),
                       float(sample_rate_entry.get()),
                       float(duration_entry.get()),
                       signal_choice.get())

generate_button = tk.Button(root, text="Generate Signal", command=generate_signal)
generate_button.config(font=("Arial", 14), bg='#4CAF50', fg='#FFFFFF', padx=20, pady=10)
generate_button.pack(pady=20)

# button to open file and draw signal in canvas discrete and continuous

open_file_button = tk.Button(root, text="Open File", command=lambda: sio.choose_file())
open_file_button.config(font=("Arial", 14), bg='#4CAF50', fg='#FFFFFF', padx=20, pady=10)
open_file_button.pack(pady=20)


# run
root.mainloop()