![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)  ![Static Badge](https://img.shields.io/badge/Arduino%20IDE%202-blue?style=for-the-badge&logo=arduino&link=https%3A%2F%2Fwww.arduino.cc%2Fen%2Fsoftware) ![Obsidian](https://img.shields.io/badge/Obsidian-%23483699.svg?style=for-the-badge&logo=obsidian&logoColor=white)

```
// Logo place holder
```

<h1 align="center">Mixuino</h1>

<h3 align="center">An Arduino Mixer for windows built with Python</h3>

-----------

- Table of contents
	- Description
	- Built with
	- Getting started
		- Software
			- Required libraries
			- Python
		- Hardware
			- Required hardware
			- Circuit diagram
	- Usage
	- Roadmap!
	- Contributing?
	- Contact
	- Acknowledgement/Credit


---------
#### WARNING  ⚠️: VERY W.I.P!!

Mixuino is a windows audio mixer build with on a Arduino nano and controlled by a python program. It uses 4 slide potentiometers feeding analog input into an Arduino nano that sends the values through serial to a python scripts that handles volume management in the windows machine. You can also add an optional push button to mute/un-mute the speakers. 

This is my first Arduino projects and first *"big"* program so please bear with me :)

-----
## Built with:

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
- ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)

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
```

```console
pip install comtypes

pip install Pillow

pip install pycaw

pip install pyserial

pyp install pystray
```
##### Nothing needed for the Arduino

### Hardware 
#### Required hardware

- Arduino nano (you could use any Arduino tho)
- 4 (or more if you want to expand) slide potentiometers
- Optional push button for muting

##### Circuit diagram

![alt text](https://github.com/thepangel/Mixuino/blob/Development/Mixuino-Diagram.pdf)


---

## Usage

You can build the script into an exe or just run the python file.
To change the processes that slider 2-4 control you can edit the if statements in the code. I am currently working on a way to do this directly in the program dynamically without hard coding it.

The program automatically detects in what port the Arduino in connected and starts a serial connection. Thats it, if you have the circuit well built just move the sliders and the volume will begin to change :)

---
## Roadmap!


- [ ] Slider 3D Models for 3D printing!
- [ ] Select processes for sliders 2-4 in the systray
	- [ ] GUI? 

---
## Contributing?

- Feel free to open up any issues or ask for features in the issues tab!
- If you want to contribute directly make sure to fork the repo and submit a pull request for me to review.

---
## Contact

Feel free to contact me [@ThePangel_](https://twitter.com/thepangel_) on Twitter/X or DM me on discord @thepangel

----
## Acknowledgement/Credit

- Logo: [@shenziscraft](https://instagram.com/shenziscraft) on Instagram

---
