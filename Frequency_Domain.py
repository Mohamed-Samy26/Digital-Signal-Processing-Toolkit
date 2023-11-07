import tkinter as tk
import signal_io as sio
import main as t2
import Frequency_domain_operations as freq_op
import FourierTransform as ft

class FrequencyDomain:

    def __init__(self):
        self.signal = None
        self.root = None

    def load_signal(self):
        # Load signal from file
        try:
            self.signal = sio.read_signal_file().points
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid file")

    def save_signal(self):
        # Save signal to file
        if self.validate_input():
            try:
                sio.save_signal_file(self.signal)
                tk.messagebox.showinfo("Success", "Signal saved successfully")
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to save signal")

    def validate_input(self):
        if not self.signal:
            tk.messagebox.showerror("Error", "Please load a signal first")
            return False
        else:
            return True

    def modify_signal(self, signal, amplitude, phase):
        # Modify the amplitude and phase of the signal components
        try:
            modified_signal = ft.FourierTransform().modify_signal(signal, amplitude, phase)
            return modified_signal
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return None

    def transform_signal(self, signal, freq):
        try:
            transformed_signal = ft.FourierTransform().DFT(signal, freq)
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
        root.title("Signal Processing")
        root.geometry("500x800")
        root.configure(bg="white")

        button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

        load_frame = tk.LabelFrame(root, text="Signal Processing", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=10)
        load_frame.pack(pady=10)
        load_button = tk.Button(load_frame, text="Load Signal", command=self.load_signal, **button_style)
        load_button.grid(row=0, column=0, padx=5, pady=5)

        save_button = tk.Button(load_frame, text="Save Signal", command=self.save_signal, **button_style)
        save_button.grid(row=0, column=1, padx=5, pady=5)

        transform_frame = tk.LabelFrame(root, text="Fourier transform", font=("Arial", 14), bg='#F5F5F5', padx=20,
                                        pady=10)
        transform_frame.pack(pady=10)

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
                    tk.messagebox.showinfo("Success", "Signal transformed successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude value")

        transform_button = tk.Button(transform_frame, text="Transform Signal", command=transform_signal, **button_style)
        transform_button.grid(row=2, columnspan=2, pady=10)

        ################################################################################################
        
        itransform_frame = tk.LabelFrame(root, text="Inverse Fourier transform", font=("Arial", 14), bg='#F5F5F5', padx=20,
                                        pady=10)
        itransform_frame.pack(pady=10)

        def itransform_signal():
            try:
                trasform_signal = self.reconstruct_signal(self.signal)
                if trasform_signal:
                    self.signal = trasform_signal
                    tk.messagebox.showinfo("Success", "Signal transformed successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude value")

        itransform_button = tk.Button(itransform_frame, text="Reconstruct Signal", command=itransform_signal, **button_style)
        itransform_button.grid(row=2, columnspan=2, pady=10)
        
        
        ################################################################################################


        modify_frame = tk.LabelFrame(root, text="Signal Modify", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=10)
        modify_frame.pack(pady=10)

        amplitude_label = tk.Label(modify_frame, text="Amplitude:", font=("Arial", 14), bg="#f2f2f2")
        amplitude_label.grid(row=0, column=0, padx=5, pady=5)

        amplitude_entry = tk.Entry(modify_frame, font=("Arial", 12))
        amplitude_entry.grid(row=0, column=1, padx=5, pady=5)

        phase_label = tk.Label(modify_frame, text="Phase:", font=("Arial", 14), bg="#f2f2f2")
        phase_label.grid(row=1, column=0, padx=5, pady=5)

        phase_entry = tk.Entry(modify_frame, font=("Arial", 12))
        phase_entry.grid(row=1, column=1, padx=5, pady=5)

        def validate_modify():

            try:
                amplitude = float(amplitude_entry.get())
                phase = float(phase_entry.get())
                modified_signal = self.modify_signal(self.signal, amplitude, phase)
                if modified_signal:
                    self.signal = modified_signal
                    tk.messagebox.showinfo("Success", "Signal modified successfully")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid amplitude or phase value")

        modify_button = tk.Button(modify_frame, text="Modify Signal", command=validate_modify, **button_style)
        modify_button.grid(row=2, columnspan=2, pady=10)

        load_polar = tk.LabelFrame(root, text="Signal Load", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=10)
        load_polar.pack(pady=10)
        load_button_polar = tk.Button(load_polar, text="Load Text", command=self.load_signal, **button_style)
        load_button_polar.pack()

        root.mainloop()
        t2.MainWindow()


if __name__ == "__main__":
    processor = FrequencyDomain()
    processor.run()
