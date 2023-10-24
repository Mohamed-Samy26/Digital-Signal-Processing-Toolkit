import tkinter as tk
from tkinter import ttk
import generate_signal as gs
import signal_io as sio
import Arithmatic_operations as op
from typing import List

class MultiSignalOperations:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Signal Operations")
        self.window.geometry("400x600")
        self.sig1 = []
        self.sig2 = []
        self.file1_label = tk.Label(self.window, text="Select File 1:")
        self.file1_label.pack(pady=10)
        self.file1_button = ttk.Button(self.window, text="Browse", command=self.select_file1)
        self.file1_button.pack()
        self.file2_label = tk.Label(self.window, text="Select File 2:")
        self.file2_label.pack(pady=10)
        self.file2_button = ttk.Button(self.window, text="Browse", command=self.select_file2)
        self.file2_button.pack()
        self.add_button = ttk.Button(self.window, text="Addition", command=self.perform_addition)
        self.add_button.pack(pady=10)
        self.sub_button = ttk.Button(self.window, text="Subtraction", command=self.perform_subtraction)
        self.sub_button.pack(pady=10)
        self.constant_label = tk.Label(self.window, text="Constant:")
        self.constant_label.pack(pady=10)
        self.entry_constant = tk.Entry(self.window)
        self.entry_constant.pack(pady=5)
        self.mul_button = ttk.Button(self.window, text="Multiplication", command=self.perform_multiplication)
        self.mul_button.pack(pady=10)
        self.sq_button = ttk.Button(self.window, text="Squaring", command=self.perform_squaring)
        self.sq_button.pack(pady=10)
        self.result_label = tk.Label(self.window, text="Result:")
        self.result_label.pack(pady=10)
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 10), padding=10)
        self.window.mainloop()

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