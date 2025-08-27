import time
import board
import digitalio
import adafruit_max31855

# SPI setup
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D8)  # CS pin 24 on Pi header
sensor = adafruit_max31855.MAX31855(spi, cs)

def c_to_f(celsius):
    return celsius * 9 / 5 + 32

try:
    while True:
        temp_c = sensor.temperature
        temp_f = c_to_f(temp_c)
        print(f"Temperature: {temp_f:.2f}°F")
        time.sleep(1)  # read every second
except KeyboardInterrupt:
    print("Exiting...")
