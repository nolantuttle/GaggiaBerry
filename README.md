# Summary
This is my little tinkering project with the Gaggia Classic Pro to add a PID control system for the boiler control using Arduino and microcontrollers. The goal is to improve thermal stability over the stock boiler through constant switching of a solid state relay while being minimally invasive to stock hardware.

It currently runs on using a Teensy 4.0 600 MHz clock microcontroller (yes, this is slightly overpowered) with a C++ program flashed using the Arduino IDE. The components are all secured in a 3D printed enclosure mounted to the side of the machine, with wires running discretely through the back ventilation ports of the machine.

The Gaggia Classic Pro has many open-source PID mods and plenty of off-the-shelf kits, but I wanted to create my own take on the mod and learn as much as I can about Arduino, PID control, thermal inertia and 3D printing from doing it myself.

# Electrical Schematic
<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/6106e972-beaf-4b9a-ba1f-e3d61d97681c" />


# Current Release Features (v2.0)

- Adaptive PID boiler temperature controller

- Small form-factor 3D printed enclosure

- AC/DC buck converter runs microcontroller on Gaggia power circuit

- Push buttons for brew/steam mode control and boiler setpoint control

- 600 MHz Teensy 4.0 microcontroller w/ 128x64 OLED display

- Migrated from Python to C++/Arduino

# Deprecated Features (v1.0)
- Software-controlled boiler temperature regulation

- Raspberry Pi Zero 2 WH–based controller for rapid development

- Open source 3D-printed enclosure with friction fit on OEM tank lid

- Non-destructive, reversible installation

- Modular design to support future controller swaps


# Repository Contents:

    /images: Showcases the installed project
    
    /Arduino: All Arduino C++ files


# Project Showcase:
![Gaggietto](https://github.com/user-attachments/assets/e1b368ad-69ce-4f7b-a92a-b4f54d063287)

