import RPi.GPIO as GPIO

RELAY_PIN = 17  # GPIO17 = pin 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # Start OFF

print("Press Enter to toggle the relay. Ctrl+C to quit.")

try:
    while True:
        input("Press Enter to toggle relay...")
        # Read current state and flip it
        current = GPIO.input(RELAY_PIN)
        GPIO.output(RELAY_PIN, not current)
        print("Relay ON" if not current else "Relay OFF")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
