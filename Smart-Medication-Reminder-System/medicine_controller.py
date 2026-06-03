import paho.mqtt.client as mqtt
from datetime import datetime
import time
import csv
import requests
import os

BROKER = "localhost"
COMMAND_TOPIC = "medicine/command"
STATUS_TOPIC = "medicine/status"

TAKEN_URL = "https://maker.ifttt.com/trigger/medicine_taken/with/key/CyAkv9Z0Zx"
MISSED_URL = "https://maker.ifttt.com/trigger/medicine_missed/with/key/CyAkv9Z0"

LOG_FILE = "medicine_log.csv"
SCHEDULE_FILE = "schedule.csv"

latest_status = None

def setup_files():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Patient", "Dose", "Status"])

    if not os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Patient", "Time", "Dose"])
            writer.writerow(["Linda", "09:00", "Morning Dose"])

def load_schedule():
    schedule = []

    with open(SCHEDULE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) == 3:
                patient, time_value, dose = row
                schedule.append((time_value, patient, dose))

    schedule.sort()
    return schedule

def log_status(patient, dose, status):
    now = datetime.now()

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            patient,
            dose,
            status
        ])

    print(f"Logged: {patient} - {dose} - {status}")

def send_notification(status):
    try:
        if status == "taken":
            requests.post(TAKEN_URL)
            print("Taken notification sent")

        elif status in ["missed", "no_response"]:
            requests.post(MISSED_URL)
            print("Missed/no-response notification sent")

    except Exception as e:
        print("Notification error:", e)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(STATUS_TOPIC)

def on_message(client, userdata, msg):
    global latest_status
    latest_status = msg.payload.decode()
    print("Status received from Arduino:", latest_status)

def wait_until(schedule_time):
    print(f"Waiting for scheduled time: {schedule_time}")

    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            return
        time.sleep(1)

def send_backup_schedule(client, patient, dose, schedule_time):
    message = f"backup_schedule|{patient}|{dose}|{schedule_time}"
    client.publish(COMMAND_TOPIC, message)
    print("Backup schedule sent to Arduino:", message)

def run_dose(client, patient, dose):
    global latest_status
    latest_status = None

    print(f"Starting reminder for {patient} - {dose}")
    client.publish(COMMAND_TOPIC, f"take_medicine|{patient}|{dose}")

    start_time = time.time()
    timeout = 30

    while time.time() - start_time < timeout:
        if latest_status in ["taken", "missed"]:
            log_status(patient, dose, latest_status)
            send_notification(latest_status)
            return
        time.sleep(1)

    print("No response received from Arduino")
    log_status(patient, dose, "no_response")
    send_notification("no_response")

setup_files()
schedule = load_schedule()

print("Loaded schedule:")
for schedule_time, patient, dose in schedule:
    print(schedule_time, "-", patient, "-", dose)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

time.sleep(2)

for schedule_time, patient, dose in schedule:
    send_backup_schedule(client, patient, dose, schedule_time)
    wait_until(schedule_time)
    run_dose(client, patient, dose)

client.loop_stop()
client.disconnect()

print("All scheduled doses completed")
