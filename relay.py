import RPi.GPIO as GPIO
import time

# Use BCM numbering (GPIO numbers, not pin numbers)
RELAY_PIN = 17  # Pin 11 = GPIO17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

print("Toggling relay on GPIO17 (pin 11). Press Ctrl+C to stop.")

try:
    while True:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay ON
        print("Relay ON")
        time.sleep(2)

        GPIO.output(RELAY_PIN, GPIO.LOW)   # Relay OFF
        print("Relay OFF")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Make sure relay is off
    GPIO.cleanup()
