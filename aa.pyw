import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Creamos un botón con una imagen y texto
image = tk.PhotoImage(file="comprobado.png")
button = ttk.Button(root, text="Mi botón", image=image, compound="top")
button.pack()

root.mainloop()

