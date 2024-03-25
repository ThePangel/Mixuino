![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)  ![Static Badge](https://img.shields.io/badge/Arduino%20IDE%202-blue?style=for-the-badge&logo=arduino&link=https%3A%2F%2Fwww.arduino.cc%2Fen%2Fsoftware) ![Obsidian](https://img.shields.io/badge/Obsidian-%23483699.svg?style=for-the-badge&logo=obsidian&logoColor=white)

<p align="center">
  <img src="logo.png" alt="logo" width="150" height="150"/>
</p>

<h1 align="center">Mixuino</h1>

<h3 align="center">An Arduino Mixer for windows built with Python</h3>


-----------

- Table of contents
	- Description
	- Built with
	- Usage
		- UI
		- Config file
	- Getting started
		- Software
			- Required libraries
			- Python
		- Hardware
			- Required hardware
			- Circuit diagram
	- Roadmap!
	- Contributing?
	- Contact
	- Acknowledgement/Credit


---------

Mixuino is a windows audio mixer build with on a Arduino nano and controlled by a python program. It uses 4 slide potentiometers feeding analog input into an Arduino nano that sends the values through serial to a python scripts that handles volume management in the windows machine. You can also add an optional push button to mute/un-mute the speakers. 

This is my first Arduino projects and first *"big"* program so please bear with me :)

-----
## Built with:

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
- ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)

---
## Usage 

### UI

![UI](UI.png)

Each option menu changes the process which each slider controls the volume of (1<sup>st</sup> slider is for master volume)

Hide to systray hides the window, the window can be revealed again from the systray icon option  ``Show`` 

There is also a checkbox than when checked changes the ``hideDefault`` value if you want the window to be hidden at startup

The options available refreshes and changes (if new programs are opened or others closed) when the mouse hovers any of the option menus

To close the application you can just close this window or close it with the ``Exit`` option in the systray icon

### Config file

To run the program you require [processes.yaml](processes.yaml) file with the structure : 
```yaml
hideDefault: false
slider1: ''
slider2: ''
slider3: ''

```
The values are the processes each slide changes and can be changed manually or through the UI

---
## Getting started

### Software

#### Required libraries:

##### Python
- Using pip

```python
comtypes==1.2.0 # To communicate with the ports

Pillow==10.1.0 # For opening the image for the systray icon

pycaw==20230407 # For audio handling

pyserial==3.5 # To read the serial data sent from the arduino

pystray==0.19.5 # To create and manage the systray icon

PyYAML==6.0.1 # To edit the Yaml config file

customtkinter==5.2.1 # To build the UI
```

```console
pip install comtypes

pip install Pillow

pip install pycaw

pip install pyserial

pip install pystray

pip install PyYAML

pip install customtkinter
```
##### Nothing needed for the Arduino

### Hardware 
#### Required hardware

- Arduino nano (you could use any Arduino tho)
- 4 (or more if you want to expand) slide potentiometers
- Optional push button for muting

##### Circuit diagram

![Cicuit diagram(pdf)](https://github.com/thepangel/Mixuino/blob/Development/MixuinoDiagram.pdf)
![Circuit Diagram](Diagram.png)


---

## Roadmap!


- [ ] Slider 3D Models for 3D printing!
- [x] GUI to select which slides control which process (30/12/2023)

---
## Contributing?

- Feel free to open up any issues or ask for features in the issues tab!
- If you want to contribute directly make sure to fork the repo and submit a pull request for me to review.

---
## Contact

Feel free to contact me [@ThePangel_](https://twitter.com/thepangel_) on Twitter/X or DM me on discord @thepangel

----
## Acknowledgement/Credit

- Logo: Inés D'Olha

---
