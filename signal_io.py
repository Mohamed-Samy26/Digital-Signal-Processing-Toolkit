import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SignalData import SignalData
import generate_signal as gs

def read_signal(file_path: str):
    points = []
    with open(file_path, 'r') as file:
        signal_data = file.readlines()
        signal_type = "FREQ" if int(signal_data[0].strip()) == 1 else "TIME"
        is_periodic =  True if int(signal_data[1].strip()) == 1 else False
        num_samples = int(signal_data[2].strip())
        
        if signal_type == "TIME":
            for line in signal_data[3:]:
                # split the line on ',' or ' ' into index and amplitude        
                index, amplitude = line.strip().replace(',', ' ').split(' ')
                index = index.replace('f', '')
                amplitude = amplitude.replace('f', '')
                points.append((int(index), float(amplitude)))
                if len(points) == num_samples:
                    break
        else:
            for index, line in enumerate(signal_data[3:]):
                amplitude, phase = line.strip().replace(',', ' ').split(' ')
                amplitude = amplitude.replace('f', '')
                phase = phase.replace('f', '')
                freq = index / num_samples
                points.append((float(freq), float(amplitude), float(phase)))
                if len(points) == num_samples:
                    break
            
    return SignalData(signal_type, is_periodic, points)

def read_signal_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])       
    return read_signal(file_path)

def write_signal(file_path: str, signal_data: SignalData):
    with open(file_path, 'w') as file:
        file.write(f"{1 if signal_data.signal_type == 'FREQ' else 0}\n")
        file.write(f"{1 if signal_data.is_periodic else 0}\n")
        file.write(f"{len(signal_data.points)}\n")
                
        if signal_data.signal_type == "TIME":
            for index, amplitude in signal_data.points:
                file.write(f"{index} {amplitude}\n")
        else:
            for freq, amplitude, phase in signal_data.points:
                file.write(f"{amplitude} {phase}\n")

def write_signal_file(signal_data: SignalData):
    file_path = filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')], defaultextension='.txt')
    if file_path:
        write_signal(file_path, signal_data)

def get_file_path():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    return file_path

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        points = read_signal(file_path).points

        fig_continuous = gs.continuous(points)
        fig_discrete = gs.discrete(points)
        
        # create a new window
        root = tk.Tk()
        root.title("Signal")
        root.geometry("1000x500")
        root.configure(bg='#F5F5F5')
        
        canvas_continuous = FigureCanvasTkAgg(fig_continuous, master=root)
        canvas_continuous.draw()
        canvas_continuous.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        canvas_discrete = FigureCanvasTkAgg(fig_discrete, master=root)
        canvas_discrete.draw()
        canvas_discrete.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
    
