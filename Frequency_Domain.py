from matplotlib import pyplot as plt
import comparesignal2 as cs
import signal_io as sio
import main as t2
import tkinter as tk
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

    def plot_signal(self, signal, title):
        plt.figure()
        plt.plot(signal)
        plt.title(title)
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.show()

    def compute_dct(self):
        try:
            if not self.validate_input():
                return

            # Perform DCT on the current signal
            dct_result = ft.FourierTransform().custom_DCT(self.signal)
            cs.SignalSamplesAreEqual(file_name='task4/DCT/DCT_output.txt',samples=dct_result.points)

            # Display the DCT result
            self.plot_signal(dct_result.points,"DCT Result")
            # Allow the user to choose the first m coefficients to save in a txt file
            m = tk.simpledialog.askinteger("DCT Coefficients", "Enter the number of coefficients to save:", minvalue=1)
            if m is not None:
                filename = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if filename:
                    ft.FourierTransform().save_coefficients_to_file(dct_result, filename, m)
                    tk.messagebox.showinfo("Success", f"{m} DCT coefficients saved to {filename}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to compute DCT: {str(e)}")

    def remove_dc_component(self):
        try:
            if not self.validate_input():
                return

            # Perform IDFT without DC component
            idft_result_without_dc = ft.FourierTransform().remove_dc_component(self.signal)

            # Display the result
            self.plot_signal(idft_result_without_dc.points, "DC Removal")

            self.old_signal = self.signal
            self.signal = idft_result_without_dc
            cs.SignalSamplesAreEqual(file_name='task4/Remove DC component/DC_component_output.txt',samples=self.signal.points)
            tk.messagebox.showinfo("Success", "DC component removed successfully")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to remove DC component: {str(e)}")

    def run(self):
        # Create GUI window
        root = tk.Tk()
        self.root = root
        root.title("Frequency Domain Signal Processing")
        root.geometry("1100x750")
        root.configure(bg="white")
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=5)

        control_frame = tk.LabelFrame(root, text="Signal Controls", font=("Arial", 10), bg='#F5F5F5', padx=5, pady=5)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        signal_frame = tk.LabelFrame(root, text="Signal preview", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        signal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        canva = pd.PlotDisplay(signal_frame)

        def update_canvas():
            if self.signal:
                canva.plot_single(self.signal)

        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}

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
                    self.old_signal = self.signal
                    self.signal = modified_signal
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

        dct_button = tk.Button(transform_frame, text="Compute DCT", command=self.compute_dct, **button_style)
        dct_button.grid(row=3, columnspan=2, pady=5)

        remove_dc_button = tk.Button(itransform_frame, text="Remove DC Component", command=self.remove_dc_component,
                                     **button_style)
        remove_dc_button.grid(row=3, columnspan=2, pady=5)

        
        def close():
            self.root.quit()
            self.root.destroy()
            
        # Close the window when the user presses the X button on the window
        self.root.protocol("WM_DELETE_WINDOW", close)
        # Run the GUI
        self.root.mainloop()
        t2.MainWindow().run()


if __name__ == "__main__":
    processor = FrequencyDomain()
    processor.run()
