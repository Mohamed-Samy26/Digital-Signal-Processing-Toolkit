import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TimeDomain import *
import tkinter as tk
import PlotDisplay as pd
import signal_io as sio
import main as t2

class TimeDomainView:
    
    def __init__(self):
        self.signal = None
        self.root = None
        self.old_signal = None
        self.canva = None

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

    def plot_signal(self, signal, title):
        plt.figure()
        plt.plot(signal)
        plt.title(title)
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.show()

    def smooth_signal(self, window_size):
        try:
            if not self.validate_input():
                return

            # Perform moving average on the current signal
            smooth_result = moving_average(self.signal, window_size)
            self.signal = smooth_result
            # Display the moving average result
            self.canva.update_plot2(self.signal, title="Smooth Result")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to smooth signal: {str(e)}")

    def sharpen_signal(self):
        try:
            if not self.validate_input():
                return

            # Perform sharpening on the current signal
            first_derivative, second_derivative = sharpen(self.signal)

            # Display the first derivative result
            self.canva.update_plot1(first_derivative, "AMP", "First Derivative Result")

            # Display the second derivative result
            self.canva.update_plot2(second_derivative, "AMP", "Second Derivative Result")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to sharpen signal: {str(e)}")    

    def fold_signal(self):
        try:
            if not self.validate_input():
                return

            # Perform folding on the current signal
            fold_result = fold_signal(self.signal)
            self.signal = fold_result
            # Display the folding result
            # self.plot_signal(fold_result.points, "Fold Result")
            self.canva.update_plot2(self.signal, title="Fold Result")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to fold signal: {str(e)}")

    def shift_signal(self, shift):
        try:
            if not self.validate_input():
                return

            # Perform shift on the current signal
            self.canva.update_plot1(self.signal, title="Original Signal")
            self.signal =  shift_signal(self.signal, shift)
            # Display the shift result
            self.canva.update_plot2(self.signal, title="Shift Result")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to shift signal: {str(e)}")

    def run(self):
        # Create GUI window
        root = tk.Tk()
        self.root = root
        root.title("Time Domain Signal Processing")
        root.geometry("1200x750")
        root.configure(bg="white")
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=5)

        control_frame = tk.LabelFrame(root, text="Signal Controls", font=("Arial", 10), bg='#F5F5F5', padx=5, pady=5)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        signal_frame = tk.LabelFrame(root, text="Signal preview", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        signal_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Using grid instead of pack

        self.canva = pd.PlotDisplay(signal_frame)

        def update_canvas():
            if self.signal:
                self.canva.plot_single(self.signal)
        
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

        ################################################################################################
        
        smooth_frame = tk.LabelFrame(control_frame, text="Moving Average", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        smooth_frame.pack(pady=5)
        
        window_size_label = tk.Label(smooth_frame, text="Window size:", font=("Arial", 14), bg="#f2f2f2")
        window_size_label.grid(row=0, column=0, padx=5, pady=5)
        
        window_size_entry = tk.Entry(smooth_frame, font=("Arial", 12))
        window_size_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def validate_smooth():
            try:
                window_size = int(window_size_entry.get())
                if window_size <= 0:
                    raise ValueError("Window size must be greater than 0")
                self.smooth_signal(window_size)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid window size")
                
        smooth_button = tk.Button(smooth_frame, text="Smooth Signal", command=validate_smooth, **button_style)
        smooth_button.grid(row=1, columnspan=2, pady=5)
        
        ################################################################################################

        sharpen_frame = tk.LabelFrame(control_frame, text="Sharpening", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        sharpen_frame.pack(pady=5)
        
        def validate_sharpen():
            self.sharpen_signal()
          
        sharpen_button = tk.Button(sharpen_frame, text="Sharpen Signal", command=validate_sharpen, **button_style)
        sharpen_button.grid(row=0, columnspan=2, pady=5)
                
        
        ################################################################################################


        fold_frame = tk.LabelFrame(control_frame, text="Folding", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        fold_frame.pack(pady=5)
        
        def validate_fold():
            self.fold_signal()
            
        fold_button = tk.Button(fold_frame, text="Fold Signal", command=validate_fold, **button_style)
        fold_button.grid(row=0, columnspan=2, pady=5)       
        
        
        ################################################################################################
        
        shift_frame = tk.LabelFrame(control_frame, text="Shift", font=("Arial", 14), bg='#F5F5F5', padx=5, pady=5)
        shift_frame.pack(pady=5)
        
        shift_label = tk.Label(shift_frame, text="Shift:", font=("Arial", 14), bg="#f2f2f2")
        shift_label.grid(row=0, column=0, padx=5, pady=5)
        
        shift_entry = tk.Entry(shift_frame, font=("Arial", 12))
        shift_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def validate_advance():
            try:
                shift = int(shift_entry.get())
                if shift <= 0:
                    raise ValueError("Shift must be greater than 0")
                self.shift_signal(shift)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid shift")
                
        advance_button = tk.Button(shift_frame, text="Advance Signal", command=validate_advance, **button_style)
        advance_button.grid(row=1, columnspan=2, pady=5)
        
        def validate_delay():
            try:
                shift = int(shift_entry.get())
                if shift <= 0:
                    raise ValueError("Shift must be greater than 0")
                self.shift_signal(-shift)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid shift")
                
        delay_button = tk.Button(shift_frame, text="Delay Signal", command=validate_delay, **button_style)
        delay_button.grid(row=2, columnspan=2, pady=5)
        
        
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

        ################################################################################################
        
        def close():
            self.root.quit()
            self.root.destroy()
            
        # Close the window when the user presses the X button on the window
        self.root.protocol("WM_DELETE_WINDOW", close)
        # Run the GUI
        self.root.mainloop()
        t2.MainWindow().run()

                
if __name__ == "__main__":
    td = TimeDomainView()
    td.run()