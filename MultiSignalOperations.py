import tkinter as tk
import signal_io as sio
import Arithmatic_operations as op
import main as t2
class MultiSignalOperations:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Signal Operations")
        self.window.geometry("400x600")
        self.sig1 = []
        self.sig2 = []

        self.file1_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.file1_frame.pack(pady=10)
        self.file1_label = tk.Label(self.file1_frame, text="Select File 1:")
        self.file1_label.pack(side=tk.LEFT)
        self.file1_button = tk.Button(self.file1_frame, text="Browse", command=self.select_file1, font=("Arial", 14),
                                      bg="#4CAF50", fg="white", padx=10, pady=5, bd=0, width=10)
        self.file1_button.pack(side=tk.LEFT)

        self.file2_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.file2_frame.pack(pady=10)
        self.file2_label = tk.Label(self.file2_frame, text="Select File 2:")
        self.file2_label.pack(side=tk.LEFT)
        self.file2_button = tk.Button(self.file2_frame, text="Browse", command=self.select_file2, font=("Arial", 14),
                                      bg="#4CAF50", fg="white", padx=10, pady=5, bd=0, width=10)
        self.file2_button.pack(side=tk.LEFT)

        self.add_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.add_frame.pack(pady=10)
        self.add_button = tk.Button(self.add_frame, text="Addition", command=self.perform_addition, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0,width=10)
        self.add_button.pack()

        self.sub_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.sub_frame.pack(pady=10)
        self.sub_button = tk.Button(self.sub_frame, text="Subtraction", command=self.perform_subtraction, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0,width=10)
        self.sub_button.pack()

        self.mul_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.mul_frame.pack(pady=10)
        self.constant_label = tk.Label(self.mul_frame, text="Constant:")
        self.constant_label.pack(pady=10)
        self.entry_constant = tk.Entry(self.mul_frame)
        self.entry_constant.pack(pady=5)
        self.mul_button = tk.Button(self.mul_frame, text="Multiplication", command=self.perform_multiplication, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0,width=10)
        self.mul_button.pack()

        self.sq_frame = tk.Frame(self.window, bd=1, relief=tk.SOLID)
        self.sq_frame.pack(pady=10)
        self.sq_button = tk.Button(self.sq_frame, text="Squaring", command=self.perform_squaring, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0,width=10)
        self.sq_button.pack()

        self.result_label = tk.Label(self.window, text="Result:")
        self.result_label.pack(pady=10)

        self.window.mainloop()

        t2.MainWindow().run()

    def select_file1(self):
        try:
            self.sig1 = sio.read_signal_file().points
        except Exception as e:
            self.result_label.config(text="Error: Invalid file")

    def select_file2(self):
        try:
            self.sig2 = sio.read_signal_file().points
        except Exception as e:
            self.result_label.config(text="Error: Invalid file")

    def perform_addition(self):
        if self.sig1 and self.sig2:
            try:
                result = op.addition(self.sig1, self.sig2)
                self.result_label.config(text=f"Result: {result}")
            except ValueError:
                self.result_label.config(text="Error: Invalid signal values")
        else:
            self.result_label.config(text="Error: Please select two files")

    def perform_subtraction(self):
        if self.sig1 and self.sig2:
            try:
                result = op.subtraction(self.sig1, self.sig2)
                self.result_label.config(text=f"Result: {result}")
            except ValueError:
                self.result_label.config(text="Error: Invalid signal values")
        else:
            self.result_label.config(text="Error: Please select two files")

    def perform_multiplication(self):
        if self.sig1:
            try:
                constant = float(self.entry_constant.get())
                result = op.multiplication(self.sig1, constant)
                self.result_label.config(text=f"Result: {result}")
            except ValueError:
                self.result_label.config(text="Error: Invalid constant value")
        else:
            self.result_label.config(text="Error: Please select a file")

    def perform_squaring(self):
        if self.sig1 and self.sig2:
            try:
                result = op.square(self.sig1, self.sig2)
                self.result_label.config(text=f"Result: {result}")
            except ValueError:
                self.result_label.config(text="Error: Invalid signal values")
        else:
            self.result_label.config(text="Error: Please select two files")

if __name__ == "__main__":
    MultiSignalOperations()
