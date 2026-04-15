import RPi.GPIO as GPIO
from tkinter import *

GPIO.setmode(GPIO.BCM)

living = 17
bathroom = 27
closet = 22

GPIO.setup(living, GPIO.OUT)
GPIO.setup(bathroom, GPIO.OUT)
GPIO.setup(closet, GPIO.OUT)

def select_room():
    choice = room.get()

    GPIO.output(living, False)
    GPIO.output(bathroom, False)
    GPIO.output(closet, False)

    if choice == 1:
        GPIO.output(living, True)
        status_label.config(text="Living Room light is ON")
    elif choice == 2:
        GPIO.output(bathroom, True)
        status_label.config(text="Bathroom light is ON")
    elif choice == 3:
        GPIO.output(closet, True)
        status_label.config(text="Closet light is ON")

def exit_app():
    GPIO.cleanup()
    root.destroy()

root = Tk()
root.title("Linda's Room Light Control")
root.geometry("320x250")

room = IntVar()

Label(root, text="Select a Room Light", font=("Arial", 14, "bold")).pack(pady=10)

Radiobutton(root, text="Living Room", variable=room, value=1, command=select_room, font=("Arial", 12)).pack(anchor="w", padx=40)
Radiobutton(root, text="Bathroom", variable=room, value=2, command=select_room, font=("Arial", 12)).pack(anchor="w", padx=40)
Radiobutton(root, text="Closet", variable=room, value=3, command=select_room, font=("Arial", 12)).pack(anchor="w", padx=40)

status_label = Label(root, text="No room selected", font=("Arial", 11), fg="blue")
status_label.pack(pady=15)

Button(root, text="Exit", command=exit_app, width=12, bg="red", fg="white", font=("Arial", 11)).pack(pady=10)

root.mainloop()
