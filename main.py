import os
import platform
import threading
import customtkinter as ctk
import shared_state
from PIL import Image, ImageTk
from register import register_face
from attendance import start_attendance
from datetime import datetime
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ===== App Settings =====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Attendance System")
app.geometry("1200x700")
app.resizable(True, True)
app.minsize(1100, 700)

def get_registered_students():
    dataset_path = "dataset"

    if not os.path.exists(dataset_path):
        return 0

    return len([
        folder for folder in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, folder))
    ])


def get_today_attendance():

    attendance_file = "attendance.csv"

    if not os.path.exists(attendance_file):
        return 0

    today = datetime.now().strftime("%Y-%m-%d")
    present = set()

    try:
        with open(attendance_file, "r", encoding="utf-8") as f:

            lines = f.readlines()

            # Skip header
            for line in lines[1:]:

                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) < 2:
                    continue

                name = parts[0]
                timestamp = parts[1]

                if timestamp.startswith(today):
                    present.add(name)

    except Exception as e:
        print("Attendance read error:", e)
        return 0

    return len(present)

current_theme = "dark"

def handle_register():

    popup = ctk.CTkToplevel(app)
    popup.transient(app)
    popup.title("Register Student")
    popup.geometry("400x220")
    popup.resizable(False, False)

    popup.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - (400 // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (220 // 2)
    popup.geometry(f"400x220+{x}+{y}")

    popup.grab_set()

    title = ctk.CTkLabel(
        popup,
        text="Register New Student",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=(25, 15))

    subtitle = ctk.CTkLabel(
    popup,
    text="Capture face data for recognition",
    font=("Segoe UI", 12),
    text_color="gray"
)
    subtitle.pack()

    entry = ctk.CTkEntry(
        popup,
        placeholder_text="Enter Student Name",
        width=280,
        height=40,
        corner_radius=10,
        font=("Segoe UI", 14)
    )
    entry.pack(pady=10)

    def submit_registration():
        name = entry.get().strip()

        if name == "":
            status.configure(text="⚠️ Enter valid name")
            return

        popup.destroy()

        status.configure(text="🟡 Registering student...")
        app.update()

        register_face(name)

        status.configure(text=f"✅ {name} registered successfully")

    submit_btn = ctk.CTkButton(
        popup,
        text="Register",
        command=submit_registration,
        width=180,
        height=40,
        corner_radius=10,
        font=("Segoe UI", 14, "bold")
    )
    submit_btn.pack(pady=20)

def handle_attendance():
    shared_state.attendance_running = True

    status.configure(text="🟡 Loading encodings and camera...")
    app.update()

    threading.Thread(
        target=start_attendance,
        args=(camera_label,),
        daemon=True
    ).start()

    status.configure(text="🟢 Attendance Running")

def stop_attendance():

    shared_state.attendance_running = False

    status.configure(text="🔴 Attendance Stopped")

def view_attendance():
    file_path = "attendance.csv"

    if not os.path.exists(file_path):
        status.configure(text="No attendance file found")
        return

    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {file_path}")
        else:  # Linux
            os.system(f"xdg-open {file_path}")

        status.configure(text="Opened attendance file")
    except:
        status.configure(text="Error opening file")

# ===== Main Layout =====

# Sidebar
sidebar = ctk.CTkFrame(
    app,
    width=260,
    corner_radius=0,
    fg_color="#1A1A1A"
)
sidebar.pack(side="left", fill="y")

# Main Content
main_area = ctk.CTkFrame(
    app,
    fg_color="#121212",
    corner_radius=0
)
main_area.pack(side="right", fill="both", expand=True)

# ===== Sidebar Content =====
icon = ctk.CTkLabel(
    sidebar,
    text="🎓",
    font=("Segoe UI Emoji", 40)
)
icon.pack(pady=(30, 10))

logo = ctk.CTkLabel(
    sidebar,
    text="Smart Attendance",
    font=("Segoe UI", 22, "bold")
)
logo.pack(pady=(40, 30), padx=20)

nav_label = ctk.CTkLabel(
    sidebar,
    text="Navigation",
    font=("Segoe UI", 14),
    text_color="gray"
)
nav_label.pack(pady=(0, 20))

stats_title = ctk.CTkLabel(
    sidebar,
    text="Dashboard Stats",
    font=("Segoe UI", 16, "bold")
)
stats_title.pack(pady=(30, 15))

students_label = ctk.CTkLabel(
    sidebar,
    text=f"👥 Registered: {get_registered_students()}",
    font=("Segoe UI", 13)
)
students_label.pack(pady=5)

attendance_label = ctk.CTkLabel(
    sidebar,
    text= "✅ Present Today: 0",
    font=("Segoe UI", 13)
)
attendance_label.pack(pady=5)

time_label = ctk.CTkLabel(
    sidebar,
    text="",
    font=("Segoe UI", 13)
)
time_label.pack(pady=(40, 5))

date_label = ctk.CTkLabel(
    sidebar,
    text="",
    font=("Segoe UI", 13),
    text_color="gray"
)
date_label.pack()


def update_time():
    now = datetime.now()

    current_time = now.strftime("Time: %I:%M:%S %p")
    current_date = now.strftime("Date: %d %B %Y")

    time_label.configure(text=current_time)
    date_label.configure(text=current_date)

    app.after(1000, update_time)

def update_stats():

    students_label.configure(
        text=f"👥 Registered: {get_registered_students()}"
    )

    attendance_label.configure(
        text=f"✅ Present Today: {get_today_attendance()}"
    )

    app.after(3000, update_stats)

update_time()
update_stats()

# ===== Main Header =====

header = ctk.CTkLabel(
    main_area,
    text="Face Recognition Attendance System",
    font=("Segoe UI", 28, "bold")
)
header.pack(pady=(25, 8))

subheader = ctk.CTkLabel(
    main_area,
    text="Automated • Secure • Efficient",
    font=("Segoe UI", 14),
    text_color="gray"
)
subheader.pack(pady=(0, 20))

# ===== Main Content Container =====

content_frame = ctk.CTkFrame(
    main_area,
    fg_color="#1E1E1E",
    corner_radius=20
)

content_frame.pack(
    padx=40,
    pady=20,
    fill="both",
    expand=True
)
# ===== Left Controls Panel =====

controls_panel = ctk.CTkFrame(
    content_frame,
    width=320,
    corner_radius=15
)

controls_panel.pack(
    side="left",
    fill="y",
    padx=20,
    pady=20
)

controls_panel.pack_propagate(False)

# ===== Right Camera Panel =====

camera_panel = ctk.CTkFrame(
    content_frame,
    corner_radius=15
)

camera_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(0, 20),
    pady=20
)

camera_label = ctk.CTkLabel(
    camera_panel,
    text="Camera Preview"
)

camera_label.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ===== Status =====
divider = ctk.CTkFrame(
    controls_panel,
    height=2,
    fg_color="#2A2A2A"
)
divider.pack(fill="x", padx=60, pady=(10, 15))

status = ctk.CTkLabel(
    controls_panel,
    text="🟢 System Ready",
    font=("Segoe UI", 14),
    text_color="#00C853"
)
status.pack(pady=(15, 20))
# ===== Button Style =====
btn_style = {
    "width": 260,
    "height": 50,
    "corner_radius": 12,
    "font": ("Segoe UI", 15, "bold"),
    "fg_color": "#2563EB",
    "hover_color": "#1D4ED8"
}

# ===== Buttons =====
register_btn = ctk.CTkButton(
    controls_panel,
    text="👤 Register Student",
    command= handle_register,
    **btn_style
)
register_btn.pack(pady=10)

attendance_btn = ctk.CTkButton(
    controls_panel,
    text="📷 Start Attendance",
    command= handle_attendance,
    **btn_style
)
attendance_btn.pack(pady=10)

stop_btn = ctk.CTkButton(
    controls_panel,
    text="⏹ Stop Attendance",
    command=stop_attendance,
    width=260,
    height=50,
    corner_radius=12,
    font=("Segoe UI", 15, "bold"),
    fg_color="#F59E0B",
    hover_color="#D97706"
)

stop_btn.pack(pady=10)

view_btn = ctk.CTkButton(
    controls_panel,
    text="📊 View Attendance",
    command= view_attendance,
    **btn_style
)
view_btn.pack(pady=10)

exit_btn = ctk.CTkButton(
    controls_panel,
    text="❌ Exit",
    command=app.destroy,
    width=260,
    height=50,
    corner_radius=12,
    font=("Segoe UI", 15, "bold"),
    fg_color="#DC2626",
    hover_color="#B91C1C"
)
exit_btn.pack(pady=20)

# ===== Run App =====
app.mainloop()