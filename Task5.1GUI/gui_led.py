import RPi.GPIO as GPIO
from tkinter import *

GPIO.setmode(GPIO.BCM)

# GPIO Pins
living = 17
bathroom = 27
closet = 22

GPIO.setup(living, GPIO.OUT)
GPIO.setup(bathroom, GPIO.OUT)
GPIO.setup(closet, GPIO.OUT)

# Function to update LEDs
def update_lights():
    # Living Room
    if living_var.get():
        GPIO.output(living, True)
    else:
        GPIO.output(living, False)

    # Bathroom
    if bathroom_var.get():
        GPIO.output(bathroom, True)
    else:
        GPIO.output(bathroom, False)

    # Closet
    if closet_var.get():
        GPIO.output(closet, True)
    else:
        GPIO.output(closet, False)

    # Update status text
    status = "Lights ON: "
    lights_on = []

    if living_var.get():
        lights_on.append("Living")
    if bathroom_var.get():
        lights_on.append("Bathroom")
    if closet_var.get():
        lights_on.append("Closet")

    if lights_on:
        status_label.config(text=status + ", ".join(lights_on))
    else:
        status_label.config(text="All lights OFF")

# Exit function
def exit_app():
    GPIO.cleanup()
    root.destroy()

# GUI Setup
root = Tk()
root.title("Linda's Room Light Control")
root.geometry("350x300")

# Variables for switches
living_var = BooleanVar()
bathroom_var = BooleanVar()
closet_var = BooleanVar()

Label(root, text="Toggle Room Lights", font=("Arial", 14, "bold")).pack(pady=10)

# Switch buttons (Checkbuttons)
Checkbutton(root, text="Living Room", variable=living_var,
            command=update_lights, font=("Arial", 12)).pack(anchor="w", padx=40)

Checkbutton(root, text="Bathroom", variable=bathroom_var,
            command=update_lights, font=("Arial", 12)).pack(anchor="w", padx=40)

Checkbutton(root, text="Closet", variable=closet_var,
            command=update_lights, font=("Arial", 12)).pack(anchor="w", padx=40)

# Status label
status_label = Label(root, text="All lights OFF", font=("Arial", 11), fg="blue")
status_label.pack(pady=15)

# Exit button
Button(root, text="Exit", command=exit_app,
       width=12, bg="red", fg="white", font=("Arial", 11)).pack(pady=10)

root.mainloop()
