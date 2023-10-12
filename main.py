import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            points.append((float(x), float(y)))
    return points

def continuous(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    fig_continuous = Figure(figsize=(5, 4), dpi=100)
    plot_continuous = fig_continuous.add_subplot(111)
    plot_continuous.plot(x, y, 'b-')
    plot_continuous.set_xlabel('X')
    plot_continuous.set_ylabel('Y')
    plot_continuous.set_title('Continuous Signal')
    plot_continuous.grid(True)

    return fig_continuous

def discrete(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    fig_discrete = Figure(figsize=(5, 4), dpi=100)
    plot_discrete = fig_discrete.add_subplot(111)
    plot_discrete.stem(x, y, 'r')
    plot_discrete.set_xlabel('X')
    plot_discrete.set_ylabel('Y')
    plot_discrete.set_title('Discrete Signal')
    plot_discrete.grid(True)

    return fig_discrete

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        points = read(file_path)

        fig_continuous = continuous(points)
        fig_discrete = discrete(points)

        canvas_continuous = FigureCanvasTkAgg(fig_continuous, master=root)
        canvas_continuous.draw()
        canvas_continuous.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        canvas_discrete = FigureCanvasTkAgg(fig_discrete, master=root)
        canvas_discrete.draw()
        canvas_discrete.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root = tk.Tk()
root.title("Signal Drawing")

btn_choose_file = tk.Button(root, text="Choose File", command=choose_file)
btn_choose_file.pack(pady=10)

root.mainloop()