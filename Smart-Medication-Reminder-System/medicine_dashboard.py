import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import csv
import os
import subprocess

LOG_FILE = "medicine_log.csv"
SCHEDULE_FILE = "schedule.csv"
ADMIN_PASSWORD = "admin123"

def setup_files():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Patient", "Dose", "Status"])

    if not os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Patient", "Time", "Dose"])

def check_admin():
    password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
    return password == ADMIN_PASSWORD

def add_schedule():
    if not check_admin():
        messagebox.showerror("Access Denied", "Only admin can change medication schedules.")
        return

    patient = patient_entry.get()
    time_value = time_entry.get()
    dose = dose_entry.get()

    if patient == "" or time_value == "" or dose == "":
        messagebox.showwarning("Missing Data", "Please enter patient name, time, and dose.")
        return

    with open(SCHEDULE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([patient, time_value, dose])

    patient_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    dose_entry.delete(0, tk.END)

    load_schedule()
    status_label.config(text="Schedule added successfully.")

def clear_schedule():
    if not check_admin():
        messagebox.showerror("Access Denied", "Only admin can clear schedules.")
        return

    with open(SCHEDULE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Patient", "Time", "Dose"])

    load_schedule()
    status_label.config(text="Schedule cleared.")

def load_schedule():
    for row in schedule_tree.get_children():
        schedule_tree.delete(row)

    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) == 3:
                    schedule_tree.insert("", "end", values=row)

def load_log():
    for row in log_tree.get_children():
        log_tree.delete(row)

    taken_count = 0
    missed_count = 0
    no_response_count = 0

    if not os.path.exists(LOG_FILE):
        status_label.config(text="No log file found yet.")
        return

    with open(LOG_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) == 5:
                log_tree.insert("", "end", values=row)
                status = row[4]

                if status == "taken":
                    taken_count += 1
                elif status == "missed":
                    missed_count += 1
                elif status == "no_response":
                    no_response_count += 1

    summary_label.config(
        text=f"Taken: {taken_count} | Missed: {missed_count} | No Response: {no_response_count}"
    )

    status_label.config(text="Log refreshed successfully.")

def start_reminder():
    status_label.config(text="Scheduled reminder started.")
    subprocess.Popen(["python3", "medicine_controller.py"])

def clear_log():
    if not check_admin():
        messagebox.showerror("Access Denied", "Only admin can clear logs.")
        return

    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Patient", "Dose", "Status"])

    load_log()
    status_label.config(text="Log cleared.")

setup_files()

root = tk.Tk()
root.title("Smart Medication Reminder Dashboard")
root.geometry("1000x700")

title_label = tk.Label(root, text="Smart Medication Reminder Dashboard", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

input_frame = tk.LabelFrame(root, text="Admin Schedule Setup", font=("Arial", 12, "bold"))
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
patient_entry = tk.Entry(input_frame, width=15)
patient_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Time (HH:MM):").grid(row=0, column=2, padx=5, pady=5)
time_entry = tk.Entry(input_frame, width=12)
time_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Dose:").grid(row=0, column=4, padx=5, pady=5)
dose_entry = tk.Entry(input_frame, width=20)
dose_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Button(input_frame, text="Add Schedule", command=add_schedule, bg="lightgreen").grid(row=0, column=6, padx=5)
tk.Button(input_frame, text="Clear Schedule", command=clear_schedule, bg="orange").grid(row=0, column=7, padx=5)

schedule_label = tk.Label(root, text="Medication Schedule", font=("Arial", 13, "bold"))
schedule_label.pack()

schedule_columns = ("Patient", "Time", "Dose")
schedule_tree = ttk.Treeview(root, columns=schedule_columns, show="headings", height=6)

for col in schedule_columns:
    schedule_tree.heading(col, text=col)
    schedule_tree.column(col, width=250, anchor="center")

schedule_tree.pack(pady=5)

summary_label = tk.Label(root, text="Taken: 0 | Missed: 0 | No Response: 0", font=("Arial", 12), fg="blue")
summary_label.pack(pady=5)

log_label = tk.Label(root, text="Medication Log", font=("Arial", 13, "bold"))
log_label.pack()

log_columns = ("Date", "Time", "Patient", "Dose", "Status")
log_tree = ttk.Treeview(root, columns=log_columns, show="headings", height=10)

for col in log_columns:
    log_tree.heading(col, text=col)
    log_tree.column(col, width=180, anchor="center")

log_tree.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Refresh Log", command=load_log, width=15, bg="lightblue").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Start Schedule", command=start_reminder, width=15, bg="lightgreen").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear Log", command=clear_log, width=15, bg="orange").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Exit", command=root.destroy, width=15, bg="red", fg="white").grid(row=0, column=3, padx=5)

status_label = tk.Label(root, text="Dashboard ready.", font=("Arial", 11), fg="green")
status_label.pack(pady=10)

load_schedule()
load_log()

root.mainloop()
