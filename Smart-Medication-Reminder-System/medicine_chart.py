import csv
import os
import matplotlib.pyplot as plt

CSV_FILE = "medicine_log.csv"

taken_count = 0
missed_count = 0
no_response_count = 0

if not os.path.exists(CSV_FILE):
    print("No medicine_log.csv file found.")
    exit()

with open(CSV_FILE, "r") as file:
    reader = csv.reader(file)
    next(reader, None)

    for row in reader:
        if len(row) == 5:
            status = row[4]

            if status == "taken":
                taken_count += 1
            elif status == "missed":
                missed_count += 1
            elif status == "no_response":
                no_response_count += 1

labels = ["Taken", "Missed", "No Response"]
values = [taken_count, missed_count, no_response_count]

plt.figure(figsize=(7, 5))
plt.bar(labels, values)
plt.title("Medication Adherence Summary")
plt.xlabel("Dose Status")
plt.ylabel("Number of Events")
plt.tight_layout()
plt.savefig("medicine_adherence_chart.png")
plt.show()

print("Chart saved as medicine_adherence_chart.png")
