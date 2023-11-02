import tkinter as tk
from tkinter import filedialog
import signal_io as sio
import Arithmatic_operations as op
import main as t2
class SingleSignalOperations:
    
    def __init__(self):
        self.signal = None
        self.root = None
    
    def load_signal(self):
        # Load signal from file
        try:
            self.signal = sio.read_signal_file()
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid file")

    def validate_input(self):
        if not self.signal:
            tk.messagebox.showerror("Error", "Please load a signal first")
            return False
        else:
            return True

    def shift_signal(self, shift_value: float):
        # Shift signal
        if self.validate_input():
            new_points = op.shift(self.signal.points, shift_value)
            op.draw(new_points)                   
      
    def normalize_signal(self, normalize_range: str):
        # Normalize signal
        new_points = None
        if normalize_range == "zero":
            new_points = op.normalizeZeroToOne(self.signal.points)
        elif normalize_range == "one":
            new_points = op.normalizeMinusOneToOne(self.signal.points)            
        op.draw(new_points)
                     
    def accumulate_signal(self):
        # Accumulate signal
        if self.validate_input():
            new_points = op.accumulate(self.signal.points)
            op.draw(new_points)

    def run(self):
        # Create GUI window
        root = tk.Tk()
        root.title("Signal Processor")
        root.geometry("800x800")
        root.configure(bg="#f2f2f2")

        # Create buttons
        button_style = {"font": ("Arial", 14), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "bd": 0}
        
        load_frame = tk.LabelFrame(root, text="Signal load", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
        load_frame.pack(pady=20)
        load_button = tk.Button(load_frame, text="Load Signal", command=self.load_signal, **button_style)
       
        shift_frame = tk.LabelFrame(root, text="Signal Shift", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
        shift_frame.pack(pady=20)
        
        shift_label = tk.Label(shift_frame, text="Shift Value:", font=("Arial", 14), bg="#f2f2f2")
        shift_label.pack(side="left") 
        
        shift_entry = tk.Entry(shift_frame, font=("Arial", 12))
        shift_entry.pack()
        
        def validate_shift():
            try:
                shift = float(shift_entry.get())
                self.shift_signal(shift)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid shift value")
                return False
            return True
                
        shift_button = tk.Button(shift_frame, text="Shift Signal", command=validate_shift, **button_style)
        
        ########################################################################

        normalize_frame = tk.LabelFrame(root, text="Signal Normalization", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
        normalize_frame.pack(pady=20)
        
        normalize_label = tk.Label(normalize_frame, text="Normalize range:", font=("Arial", 14), bg="#f2f2f2")
        normalize_label.pack(side="left") 
        
        normalize_var = tk.StringVar(value="zero")
        normalize_zero_radio = tk.Radiobutton(normalize_frame, text="Zero To One [0 : 1]", variable=normalize_var, value="zero", font=("Arial", 12), bg="#f2f2f2")
        normalize_one_radio = tk.Radiobutton(normalize_frame, text="-VE one to +VE one [-1 : 1] ", variable=normalize_var, value="one", font=("Arial", 12), bg="#f2f2f2")
        normalize_zero_radio.pack(side="left")
        normalize_one_radio.pack(side="left")
        
        def validate_normalize():
            self.normalize_signal(normalize_var.get())
        
        normalize_button = tk.Button(normalize_frame, text="Normalize Signal", command=validate_normalize, **button_style)
        
        ################################################################################################
        
        accumulate_frame = tk.LabelFrame(root, text="Signal Accumulation", font=("Arial", 14), bg='#F5F5F5', padx=20, pady=20)
        accumulate_frame.pack(pady=20)
        accumulate_button = tk.Button(accumulate_frame, text="Accumulate Signal", command=self.accumulate_signal, **button_style)

        # Add buttons to window
        load_button.pack(pady=10)
        shift_button.pack(pady=10)
        normalize_button.pack(pady=10)
        accumulate_button.pack(pady=10)

        # Start GUI loop
        root.mainloop()
        t2.MainWindow().run()

if __name__ == "__main__":
    processor = SingleSignalOperations()
    processor.run()