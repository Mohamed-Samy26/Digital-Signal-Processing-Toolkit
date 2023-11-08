import tkinter as tk

from matplotlib import pyplot as plt
import signal_io as sio
import main as t2
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import FourierTransform as ft
import PlotDisplay as pd

import signalcompare as sc

class FrequencyDomain:

    def __init__(self):
        self.signal = None
        self.root = None
        self.old_signal = None

    def load_signal(self):
        # Load signal from file
        try:
            self.signal = sio.read_signal_file()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "Invalid file, error "+str(e))

    def save_signal(self):
        # Save signal to file
        if self.validate_input():
            try:
                sio.write_signal_file(self.signal)
                tk.messagebox.showinfo("Success", "Signal saved successfully")
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to save signal")

    def validate_input(self):
        if not self.signal:
            tk.messagebox.showerror("Error", "Please load a signal first")
            return False
        else:
            return True

    def modify_signal(self, signal, index, amplitude, phase):
        # Modify the amplitude and phase of the signal components
        try:
            modified_signal = ft.FourierTransform().modify_index(signal, index-1, amplitude, phase)
            return modified_signal
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return None

    def transform_signal(self, signal, freq):
        try:
            transformed_signal = ft.FourierTransform().DFT(signal, freq)
            frequencies = [point[0] for point in transformed_signal.points]
            return transformed_signal
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return None

    def reconstruct_signal(self, signal):
        try:
            transformed_signal = ft.FourierTransform().IDFT(signal)
            return transformed_signal
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return None

    def run(self):
        # Create GUI window
        root = tk.Tk()
        root.title("Frequency Domain Signal Processing")
        root.geometry("1100x700")
        root.configure(bg="white")
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=5)
        
        control_frame = tk.LabelFrame(root, text="Signal Controls", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        signal_frame = tk.LabelFrame(root, text="Signal preview", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        signal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        canva = pd.PlotDisplay(signal_frame)
        
        def update_canvas():
            if self.signal:
                canva.update_plot(self.signal)

        button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

        def load_signal():
            self.load_signal()
            update_canvas()
        
        load_frame = tk.LabelFrame(control_frame, text="Signal Processing", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        load_frame.pack(pady=5)
        load_button = tk.Button(load_frame, text="Load Signal", command=load_signal, **button_style)
        load_button.grid(row=0, column=0, padx=5, pady=5)

        save_button = tk.Button(load_frame, text="Save Signal", command=self.save_signal, **button_style)
        save_button.grid(row=0, column=1, padx=5, pady=5)

        transform_frame = tk.LabelFrame(control_frame, text="Fourier transform", font=("Arial", 14), bg='#F5F5F5', padx=5,
                                        pady=5)
        transform_frame.pack(pady=5)

        transform_label = tk.Label(transform_frame, text="Frequency:", font=("Arial", 14), bg="#f2f2f2")
        transform_label.grid(row=0, column=0, padx=5, pady=5)

        transform_entry = tk.Entry(transform_frame, font=("Arial", 12))
        transform_entry.grid(row=0, column=1, padx=5, pady=5)

        def transform_signal():
            try:
                freq = float(transform_entry.get())
                trasform_signal = self.transform_signal(self.signal,freq)
                if trasform_signal:
                    self.signal = trasform_signal
                    # trasform_signal.plot_signal()
                    update_canvas()
                    tk.messagebox.showinfo("Success", "Signal transformed successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude value")

        transform_button = tk.Button(transform_frame, text="Transform Signal", command=transform_signal, **button_style)
        transform_button.grid(row=2, columnspan=2, pady=5)

        ################################################################################################
        
        itransform_frame = tk.LabelFrame(control_frame, text="Inverse Fourier transform", font=("Arial", 14), bg='#F5F5F5', padx=20,
                                        pady=5)
        itransform_frame.pack(pady=5)

        def itransform_signal():
            try:
                trasform_signal = self.reconstruct_signal(self.signal)
                if trasform_signal:
                    self.signal = trasform_signal
                    # trasform_signal.plot_signal()
                    update_canvas()
                    tk.messagebox.showinfo("Success", "Signal reconstructed successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude value")

        itransform_button = tk.Button(itransform_frame, text="Reconstruct Signal", command=itransform_signal, **button_style)
        itransform_button.grid(row=2, columnspan=2, pady=5)
        
        
        ################################################################################################


        modify_frame = tk.LabelFrame(control_frame, text="Signal Modify", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        modify_frame.pack(pady=5)

        index_label = tk.Label(modify_frame, text="Component index:", font=("Arial", 14), bg="#f2f2f2")
        index_label.grid(row=0, column=0, padx=5, pady=5)

        index_entry = tk.Entry(modify_frame, font=("Arial", 12))
        index_entry.grid(row=0, column=1, padx=5, pady=5)

        amplitude_label = tk.Label(modify_frame, text="Amplitude:", font=("Arial", 14), bg="#f2f2f2")
        amplitude_label.grid(row=1, column=0, padx=5, pady=5)

        amplitude_entry = tk.Entry(modify_frame, font=("Arial", 12))
        amplitude_entry.grid(row=1, column=1, padx=5, pady=5)

        phase_label = tk.Label(modify_frame, text="Phase:", font=("Arial", 14), bg="#f2f2f2")
        phase_label.grid(row=2, column=0, padx=5, pady=5)

        phase_entry = tk.Entry(modify_frame, font=("Arial", 12))
        phase_entry.grid(row=2, column=1, padx=5, pady=5)

        def validate_modify():
            try:
                index = int(index_entry.get())
                
                amplitude = None
                if amplitude_entry.get():
                    amplitude = float(amplitude_entry.get())
                
                phase = None
                if phase_entry.get():
                    phase = float(phase_entry.get())
                
                modified_signal = self.modify_signal(self.signal, index, amplitude, phase)
                if modified_signal:
                    self.signal = modified_signal
                    self.old_signal = modified_signal
                    # modified_signal.plot_signal()
                    canva.compare_signals(self.old_signal, self.signal)
                    tk.messagebox.showinfo("Success", "Signal modified successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude or phase value")

        modify_button = tk.Button(modify_frame, text="Modify Signal", command=validate_modify, **button_style)
        modify_button.grid(row=4, columnspan=2, pady=5)

        ################################################################################################
        
        def validate_test():
            try:
                test_signal = sio.read_signal_file()
                _, amplitudes1, phase1 = self.signal.get_signal()
                _, amplitudes2, phase2 = test_signal.get_signal()
                amplitudes1 = [round(x, 8) for x in amplitudes1]
                amplitudes2 = [round(x, 8) for x in amplitudes2]           
                    
                    
                b1 = sc.SignalComapreAmplitude(amplitudes1, amplitudes2) # 0.905007438022
                b2= True
                
                if self.signal.signal_type == "FREQ":
                    phase1 = [round(x, 8) for x in phase1]
                    phase2 = [round(x, 8) for x in phase2]
                    b2 = sc.SignalComaprePhaseShift(phase1, phase2)  
                
                if b1 and b2:
                    print("Signal compared successfully")
                    tk.messagebox.showinfo("Success", "Tests passed successfully")
    
                else:
                    print("Signal compared failed")
                    tk.messagebox.showinfo("Success", f"Tests failed Amplitude passed: {b1}, phase passed: {b2}")
            except Exception as e:
                tk.messagebox.showerror("Error", "Invalid amplitude or phase value, error: "+str(e))
            
        
        testing = tk.LabelFrame(control_frame, text="Compare signal", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=10)
        testing.pack(pady=5)
        load_button_polar = tk.Button(testing, text="Load Test Signal", command=validate_test, **button_style)
        load_button_polar.pack()

        root.mainloop()
        t2.MainWindow()


if __name__ == "__main__":
    processor = FrequencyDomain()
    processor.run()
