import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Define script paths
COLLECT_SCRIPT = "collect_dataset.py"
TRAIN_SCRIPT = "train_encodings.py"
SECURE_SCRIPT = "secure_attendance.py"

# Function to collect dataset
def collect_dataset():
    try:
        subprocess.run(["python", COLLECT_SCRIPT], check=True)
        messagebox.showinfo("Success", "Dataset collected successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to collect dataset.")

# Function to train encodings
def train_encodings():
    try:
        subprocess.run(["python", TRAIN_SCRIPT], check=True)
        messagebox.showinfo("Success", "Encodings trained successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Training failed.")

# Function to run secure attendance
def start_attendance():
    try:
        subprocess.run(["python", SECURE_SCRIPT])
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Attendance marking failed.")

# Create GUI
root = tk.Tk()
root.title("Facial Recognition Attendance System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Secure Face Attendance", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Button(root, text="📸 Capture Dataset", width=25, height=2, bg="#cce5ff", command=collect_dataset).pack(pady=5)
tk.Button(root, text="🧠 Train Encodings", width=25, height=2, bg="#d4edda", command=train_encodings).pack(pady=5)
tk.Button(root, text="✅ Start Attendance", width=25, height=2, bg="#fff3cd", command=start_attendance).pack(pady=5)

tk.Label(root, text="By K.S. Shankar", font=("Arial", 10), bg="#f0f0f0").pack(side="bottom", pady=10)

root.mainloop()
