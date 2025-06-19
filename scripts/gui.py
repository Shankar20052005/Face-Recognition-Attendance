import customtkinter as ctk
import subprocess
import os
import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLLECT_SCRIPT = "collect_dataset.py"
TRAIN_SCRIPT = "train_encodings.py"
SECURE_SCRIPT = "mark_attendance.py"
ATTENDANCE_FOLDER = "../attendance"

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("👁️ Secure Facial Attendance System")
        self.geometry("600x500")

        self.name_label = ctk.CTkLabel(self, text="Enter Name for Dataset Capture:", font=("Arial", 16))
        self.name_label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self, width=300, placeholder_text="e.g., Shankar")
        self.name_entry.pack(pady=5)

        self.capture_btn = ctk.CTkButton(self, text="📸 Capture Dataset", command=self.capture_dataset)
        self.capture_btn.pack(pady=10)

        self.train_btn = ctk.CTkButton(self, text="🧠 Train Encodings", command=self.train_encodings)
        self.train_btn.pack(pady=10)

        self.attend_btn = ctk.CTkButton(self, text="✅ Start Secure Attendance", command=self.start_attendance)
        self.attend_btn.pack(pady=10)

        self.view_log_btn = ctk.CTkButton(self, text="📂 Open Attendance Folder", command=self.open_logs)
        self.view_log_btn.pack(pady=10)

        self.log_box = ctk.CTkTextbox(self, height=120, width=500)
        self.log_box.pack(pady=15)
        self.log("System Ready. Awaiting input...")

    def log(self, message):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def capture_dataset(self):
        name = self.name_entry.get().strip()
        if not name:
            self.log("⚠️ Please enter a name before capturing.")
            return
        self.log(f"Starting image capture for: {name}")
        try:
            subprocess.run(["python", COLLECT_SCRIPT, name], check=True)
            self.log("✅ Dataset collection complete.")
        except subprocess.CalledProcessError:
            self.log("❌ Error during image collection.")

    def train_encodings(self):
        self.log("Training encodings...")
        try:
            subprocess.run(["python", TRAIN_SCRIPT], check=True)
            self.log("✅ Training complete.")
        except subprocess.CalledProcessError:
            self.log("❌ Training failed.")

    def start_attendance(self):
        self.log("Launching secure attendance system...")
        try:
            subprocess.run(["python", SECURE_SCRIPT])
            self.log("✅ Attendance session finished.")
        except subprocess.CalledProcessError:
            self.log("❌ Error in attendance script.")

    def open_logs(self):
        self.log("Opening attendance folder...")
        attendance_path = os.path.abspath(ATTENDANCE_FOLDER)
        try:
            os.startfile(attendance_path)
        except:
            self.log("❌ Cannot open folder. Try manually navigating.")

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()