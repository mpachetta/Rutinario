import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Routine Alarm")

# Define the routines
def morning_routine():
    messagebox.showinfo("Routine", "Starting Morning Routine")

def dress_routine():
    messagebox.showinfo("Routine", "Starting Dress Routine")

def hygiene_routine():
    messagebox.showinfo("Routine", "Starting Hygiene Routine")

def food_routine():
    messagebox.showinfo("Routine", "Starting Food Routine")

# Create buttons for each routine
morning_button = tk.Button(root, text="Morning Routine", command=morning_routine)
morning_button.pack()

dress_button = tk.Button(root, text="Dress Routine", command=dress_routine)
dress_button.pack()

hygiene_button = tk.Button(root, text="Hygiene Routine", command=hygiene_routine)
hygiene_button.pack()

food_button = tk.Button(root, text="Food Routine", command=food_routine)
food_button.pack()

# Start the main event loop
root.mainloop()
