# Summary
This is my little tinkering project with the Gaggia Classic Pro to add a PID control system for the boiler control using Arduino and microcontrollers. The goal is to improve thermal stability over the stock boiler through constant switching of a solid state relay while being minimally invasive to stock hardware.

It currently runs on using a Teensy 4.0 600 MHz clock microcontroller (yes, this is slightly overpowered) with a C++ program flashed using the Arduino IDE. The components are all secured in a 3D printed enclosure mounted to the side of the machine, with wires running discretely through the back ventilation ports of the machine.

The Gaggia Classic Pro has many open-source PID mods and plenty of off-the-shelf kits, but I wanted to create my own take on the mod and learn as much as I can about Arduino, PID control, thermal inertia and 3D printing from doing it myself.

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
- /images: Showcases the installed project
  
- /src: All compiled/runnable files for control loop
  
- /test: Testing files to verify boiler switching functionality

# Project Showcase:

![GaggiaBerry2](https://github.com/user-attachments/assets/041621d6-5ff7-453e-87d3-0def705909a6)

![GaggiaBerry1](https://github.com/user-attachments/assets/5d1df92b-b439-4863-82a8-d794bf1eb619)
