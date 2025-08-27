This is my project for adding PID-style control to a Gaggia Classic Pro espresso machine using a Raspberry Pi Zero 2 WH. The Pi runs a Python script that reads boiler temperature from a K-type thermocouple (via a MAX31855 module) and switches the heating element through a solid-state relay.

The setup replaces the stock brew thermostat but keeps the safety cutoff thermostat in place. The Pi reads temperature in real time, applies an offset (since the probe is mounted externally on the boiler), and toggles the relay to keep the machine at a stable target range.

The software is written in Python and runs as a systemd service. It uses threads for:

- Continuous thermocouple temperature readings

- Relay control logic (simple threshold switching for now)

- A small Tkinter GUI that shows the current temperature and status on an HDMI-connected display

The goal is to eventually make a lightweight, customizable controller for the Gaggia without relying on commercial PID kits.
