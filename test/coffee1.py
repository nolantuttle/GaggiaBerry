import time
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_max31855

# --- Thermocouple setup ---
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D8)  # CS pin 24 on Pi header
sensor = adafruit_max31855.MAX31855(spi, cs)

def c_to_f(celsius):
    return celsius * 9 / 5 + 32

# --- Relay setup ---
RELAY_PIN = 17  # GPIO17 = pin 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # start OFF

# --- Main loop ---
print("Press Enter to toggle relay. Ctrl+C to exit.")

try:
    while True:
        # Read and print temperature
        temp_c = sensor.temperature
        temp_f = c_to_f(temp_c)
        print(f"Temperature: {temp_f:.2f}°F")

        # Non-blocking Enter press check
        input_ready = input("Press Enter to toggle relay (or just wait to see temps): ")
        if input_ready == "":
            current = GPIO.input(RELAY_PIN)
            GPIO.output(RELAY_PIN, not current)
            print("Relay ON" if not current else "Relay OFF")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
