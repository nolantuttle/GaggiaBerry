import time
import threading
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_max31855

# --- Thermocouple setup ---
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D8)  # CS pin 24 on Pi header
sensor = adafruit_max31855.MAX31855(spi, cs)

# --- Relay setup ---
RELAY_PIN = 17  # GPIO17 = pin 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # start OFF

# --- Shared temperature variable ---
current_temp_f = 0
lock = threading.Lock()  # to safely share data between threads

# --- Temperature reading thread ---
def read_temperature():
    global current_temp_f
    while True:
        temp_c = sensor.temperature
        temp_f = temp_c * 9 / 5 + 32 - 40
        with lock:
            current_temp_f = temp_f
        print(f"Temperature: {temp_f:.2f}°F")
        time.sleep(0.5)  # adjust frequency if desired

# --- Relay control thread ---
def control_relay():
    while True:
        with lock:
            temp = current_temp_f
        if temp < 200:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # turn ON
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # turn OFF
        time.sleep(2)  # check twice a second

# --- Start threads ---
try:
    temp_thread = threading.Thread(target=read_temperature, daemon=True)
    relay_thread = threading.Thread(target=control_relay, daemon=True)
    temp_thread.start()
    relay_thread.start()

    while True:
        time.sleep(1)  # main thread just waits

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
