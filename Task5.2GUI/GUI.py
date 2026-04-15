import RPi.GPIO as GPIO
from tkinter import *

# -----------------------------
# GPIO setup
# -----------------------------
GPIO.setmode(GPIO.BCM)

living = 18      # PWM pin for living room
bathroom = 27    # normal GPIO
closet = 22      # normal GPIO

GPIO.setup(living, GPIO.OUT)
GPIO.setup(bathroom, GPIO.OUT)
GPIO.setup(closet, GPIO.OUT)

# PWM setup for living room LED
pwm = GPIO.PWM(living, 1000)   # 1000 Hz frequency
pwm.start(0)                   # start with 0% brightness

# -----------------------------
# Functions
# -----------------------------
def update_lights():
    choice = room.get()

    # Turn everything off first
    pwm.ChangeDutyCycle(0)
    GPIO.output(bathroom, False)
    GPIO.output(closet, False)

    if choice == 1:
        # Living room uses slider brightness
        duty = slider.get()
        pwm.ChangeDutyCycle(duty)
        status_label.config(text=f"Living Room brightness: {duty}%")

    elif choice == 2:
        GPIO.output(bathroom, True)
        status_label.config(text="Bathroom light is ON")

    elif choice == 3:
        GPIO.output(closet, True)
        status_label.config(text="Closet light is ON")

    else:
        status_label.config(text="No room selected")


def update_brightness(val):
    # Slider only affects living room
    if room.get() == 1:
        duty = int(val)
        pwm.ChangeDutyCycle(duty)
        status_label.config(text=f"Living Room brightness: {duty}%")
    else:
        status_label.config(text="Select Living Room to adjust brightness")


def exit_app():
    pwm.stop()
    GPIO.cleanup()
    root.destroy()

# -----------------------------
# GUI setup
# -----------------------------
root = Tk()
root.title("Room Light Control with Living Room Intensity")
root.geometry("420x320")

room = IntVar()
room.set(0)

title_label = Label(root, text="Select a Room", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

Radiobutton(
    root,
    text="Living Room",
    variable=room,
    value=1,
    command=update_lights,
    font=("Arial", 12)
).pack(anchor="w", padx=40)

Radiobutton(
    root,
    text="Bathroom",
    variable=room,
    value=2,
    command=update_lights,
    font=("Arial", 12)
).pack(anchor="w", padx=40)

Radiobutton(
    root,
    text="Closet",
    variable=room,
    value=3,
    command=update_lights,
    font=("Arial", 12)
).pack(anchor="w", padx=40)

brightness_label = Label(root, text="Living Room Brightness", font=("Arial", 12))
brightness_label.pack(pady=10)

slider = Scale(
    root,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=update_brightness,
    length=260
)
slider.pack()

status_label = Label(root, text="No room selected", font=("Arial", 11), fg="blue")
status_label.pack(pady=15)

exit_button = Button(
    root,
    text="Exit",
    command=exit_app,
    width=12,
    bg="red",
    fg="white",
    font=("Arial", 11)
)
exit_button.pack(pady=10)

root.mainloop()
