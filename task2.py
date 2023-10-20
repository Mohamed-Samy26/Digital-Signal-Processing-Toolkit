import tkinter as tk
from tkinter import ttk
import generate_signal as gs
import signal_io as sio
import Arithmatic_operations as op
from typing import List

# Create the main window
window = tk.Tk()
window.title("Signal Operations")
window.geometry("400x600")

# Create variables to store file paths
sig1 = []
sig2 = []

# Function to select file 1
def select_file1():
    global sig1  # Declare sig1 as a global variable
    sig1 = sio.choose_file()

# Function to select file 2
def select_file2():
    global sig2  # Declare sig2 as a global variable
    sig2 = sio.choose_file()

# Function to perform addition
def perform_addition():
    if sig1 and sig2:
        try:
            result = op.addition(sig1, sig2)
            result_label.config(text=f"Result: {result}")
        except ValueError:
            result_label.config(text="Error: Invalid signal values")
    else:
        result_label.config(text="Error: Please select two files")

# Function to perform subtraction
def perform_subtraction():
    if sig1 and sig2:
        try:
            result = op.subtraction(sig1, sig2)
            result_label.config(text=f"Result: {result}")
        except ValueError:
            result_label.config(text="Error: Invalid signal values")
    else:
        result_label.config(text="Error: Please select two files")

# Function to perform multiplication
def perform_multiplication():
    if sig1:
        try:
            constant = float(entry_constant.get())
            result = op.multiplication(sig1, constant)
            result_label.config(text=f"Result: {result}")
        except ValueError:
            result_label.config(text="Error: Invalid constant value")
    else:
        result_label.config(text="Error: Please select a file")

# Function to perform squaring
def perform_squaring():
    if sig1 and sig2:
        try:
            result = op.square(sig1, sig2)
            result_label.config(text=f"Result: {result}")
        except ValueError:
            result_label.config(text="Error: Invalid signal values")
    else:
        result_label.config(text="Error: Please select two files")

# Create buttons and labels
file1_label = tk.Label(window, text="Select File 1:")
file1_label.pack(pady=10)

file1_button = ttk.Button(window, text="Browse", command=select_file1)
file1_button.pack()

file2_label = tk.Label(window, text="Select File 2:")
file2_label.pack(pady=10)

file2_button = ttk.Button(window, text="Browse", command=select_file2)
file2_button.pack()

add_button = ttk.Button(window, text="Addition", command=perform_addition)
add_button.pack(pady=10)

sub_button = ttk.Button(window, text="Subtraction", command=perform_subtraction)
sub_button.pack(pady=10)

constant_label = tk.Label(window, text="Constant:")
constant_label.pack(pady=10)

entry_constant = tk.Entry(window)
entry_constant.pack(pady=5)

mul_button = ttk.Button(window, text="Multiplication", command=perform_multiplication)
mul_button.pack(pady=10)

sq_button = ttk.Button(window, text="Squaring", command=perform_squaring)
sq_button.pack(pady=10)

result_label = tk.Label(window, text="Result:")
result_label.pack(pady=10)

# Configure button styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10)

# Start the main loop
window.mainloop()
