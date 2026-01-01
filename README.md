This is my little tinkering project with the Gaggia Classic Pro to add a PID control system for the boiler control using Arduino and microcontrollers. The goal is to improve thermal stability over the stock boiler through constant switching of a solid state relay while being minimally invasive to stock hardware.

It currently runs on a Raspberry Pi Zero 2 WH for easy revisions and simplicity, next release in v2.0 will feature an ESP-type microcontroller with a fast control loop and precise PID control through a PID Arduino library. 

The system is housed in a custom 3D-printed enclosure that friction-fits onto the stock water tank lid, requiring zero screws or drilling on the original machine. The enclosure features a filleted space for a 16x2 LCD display that communicates over I2C to display relay state and boiler temperature.

Current Features (v1.0)
- Software-controlled boiler temperature regulation

- Raspberry Pi Zero 2 WH–based controller for rapid development

- Open source 3D-printed enclosure with friction fit on OEM tank lid

- Non-destructive, reversible installation

- Modular design to support future controller swaps

Repository Contents:
- /images: Showcases the installed project
  
- /src: All compiled/runnable files for control loop
  
- /test: Testing files to verify boiler switching functionality

Project Showcase:

![GaggiaBerry2](https://github.com/user-attachments/assets/041621d6-5ff7-453e-87d3-0def705909a6)

![GaggiaBerry1](https://github.com/user-attachments/assets/5d1df92b-b439-4863-82a8-d794bf1eb619)
