import time
import threading
import math
import sys
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_max31855
import tkinter as tk
from tkinter import ttk

# --- Thermocouple setup ---
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D8)  # CS pin 24 on Pi header
sensor = adafruit_max31855.MAX31855(spi, cs)

# --- Relay setup ---
RELAY_PIN = 17  # GPIO17 = pin 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # start OFF

def run_gui():
    screen = tk.Tk()
    screen.title("Nolan's PID Control")
    # Get screen width and height
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()

    screen.geometry(f"{screen_width}x{screen_height}+0+0")

    mainLabel = tk.Label(screen, text="Gaggia Classic Pro", font=("Times New Roman", 36))
    mainLabel.pack()

    # Temperature display label
    temp_label = tk.Label(screen, text="Temperature: --°F", font=("Arial", 24))
    temp_label.pack(pady=10)

    # Relay status label
    relay_label = tk.Label(screen, text="Relay: OFF", font=("Arial", 20), fg="red")
    relay_label.pack(pady=5)

    # Function to update labels periodically
    def update_labels():
        # Update temperature
        with lock:
            temp = current_temp_f
            relay_state = GPIO.input(RELAY_PIN)  # HIGH = ON, LOW = OFF

        if temp is not None:
            temp_label.config(text=f"Temperature: {temp:.2f}°F")

        # Update relay status
        if relay_state:
            relay_label.config(text="Relay: ON", fg="green")
        else:
            relay_label.config(text="Relay: OFF", fg="red")

        screen.after(500, update_labels)  # schedule next update in 500ms

    # Start periodic updates
    update_labels()
    
    screen.mainloop()

# --- Shared temperature variable ---
current_temp_f = None
lock = threading.Lock()

# --- Temperature reading thread ---
def read_temperature():
    global current_temp_f
    while True:
        try:
            temp_c = sensor.temperature
            if temp_c is None or math.isnan(temp_c):
                raise ValueError("Thermocouple disconnected or invalid reading")
            temp_f = temp_c * 9 / 5 + 32 - 37  # with offset
            with lock:
                current_temp_f = temp_f
            print(f"Temperature: {temp_f:.2f}°F")
        except (OSError, ValueError) as e:
            print(f"[!] Fatal sensor error: {e}")
            sys.exit(1)   # Kill program immediately, relay turns off in finally
        time.sleep(0.1)

# --- Relay control thread ---
def control_relay():
    while True:
        with lock:
            temp = current_temp_f
        # Relay stays off until valid temp arrives
        if temp is not None and temp < 195:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(0.1)

# --- Start threads ---
try:
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    temp_thread = threading.Thread(target=read_temperature, daemon=True)
    relay_thread = threading.Thread(target=control_relay, daemon=True)
    temp_thread.start()
    relay_thread.start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
