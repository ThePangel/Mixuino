# Import of all required dependencies
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
import serial
import pystray
from pystray import Menu, MenuItem as item
from PIL import Image
import sys
import serial.tools.list_ports
import time

# Initiats Variable used to check if the port is alrady assigned
isAssigned = False

# Initiates variable containing the COM port number
portNum = 0

# Function that asigns the COM port number where the Arduino Nano is connected
def portAssign():
    
    # Makes the isAssigned variable globally accessible
    global isAssigned
    
    # Checks if the port is assigned
    while isAssigned == False:
        
        #Makes the variable containing the COM port number global accessible
        global portNum
        
        # Makes a list of al COM ports and whats connected to them
        ports = list(serial.tools.list_ports.comports())
        
        
        
        # Loops through all the ports
        for p in ports:
                
                # Loops through all the possible COM ports that the Arduino Nano could be connected to
                for portNum in range(0, 9):
                    
                    # Check if the device connected is the arduino Nano
                    if ("CH340") in p[1] and (f"COM{portNum}") in p[1]:
                        
                        # Makes isAssigned true 
                        isAssigned = True
                        
                        # Returns the Function
                        return 
        
        # Delay for let the function read the ports and not have them still open
        time.sleep(5)

# Calls the portAssign function
portAssign()
    
# Makes a variable containing the connection to the Arduino Nano
arduino = serial.Serial(port=f'COM{portNum}', baudrate=57600, timeout=.1) 

# Gets speaker for audio manipulation
devices = AudioUtilities.GetSpeakers()

# Initiates audio interface
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Initiates volume manipulation
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Gets running Sessions
sessions = AudioUtilities.GetAllSessions()

# Sets variable Stopb used to stop the program
stopb = False

# Funtions that stops the systray icon and sets stopb to true so the loop exits the program 
def stop():
    global stopb
    stopb = True
    icon.stop()
    
# Initiates systray menu with option "Exit" which calls the stop func
menu1 = (item("Exit", stop),)

# File for the icon image (image or .ico)
file = "logo.png"

# Creates the systray icon object
icon = pystray.Icon(name="name", icon=Image.open(file), title="Mixer", menu=menu1)

# Initializes the systray icon in parallel so the script keeps running
icon.run_detached()

# Tries to execute main script if else it exits with the error
try:
    
    # Infinite loop to constantly monitor and change the audio volume
    while True:
        
        # Checks if it has to stop the program
        if stopb == True:
            sys.exit()
        
        # Stores the recieved data of the arduino into the variable
        serialData = str(arduino.readline())
        
        # Removes the prefixes and suffixes from the data and removes unwanted spaces
        serialData = serialData.replace("b'", "").replace("\\n'", "").rstrip()
        
        # Checks if the serial data is not empty
        if serialData != "":
        
            # If the value starts with the indicator a, change master volume
            if serialData.startswith("a"):
                
                # Removes slider indicator so we are left with the numerical value
                serialData = serialData.replace("a", "")
                
                # Assigns the data in float format into a variable
                masterVolume = float(serialData)
                
                # Changes the master volume to the desired volume (Since it's scalar the volume is from 0.0 to 1.0)
                volume.SetMasterVolumeLevelScalar(masterVolume, None)   
            
            # If the value starts with the indicator b, change the volume of any process you would like 
            if serialData.startswith("b"):
                
                # Loops through all the sessions currently running
                for session in sessions:
                    
                    # Initiates volume manipulation for processes
                    volume1 = session._ctl.QueryInterface(ISimpleAudioVolume)
                    
                    # Checks if process is the one you want
                    if session.Process and session.Process.name() == "brave.exe":
                    
                        # Removes slider indicator so we are left with the numerical value
                        serialData = serialData.replace("b", "")
                        
                        # Assigns the data in float format into a variable
                        masterVolume = float(serialData)   
                        
                        # Changes the sessin volume to the desired volume (From 0.0 to 1.0)
                        volume1.SetMasterVolume(masterVolume, None)
            
            
            # If the value starts with the indicator c, change the volume of any process you would like 
            if serialData.startswith("c"):
                
                # Loops through all the sessions currently running
                for session in sessions:
                    
                    # Initiates volume manipulation for processes  
                    volume2 = session._ctl.QueryInterface(ISimpleAudioVolume)
                    
                    # Checks if process is the one you want
                    if session.Process and session.Process.name() == "prcessB.exe":
                            
                        # Removes slider indicatr so we are left with the numerical value
                        serialData = serialData.replace("c", "")
                        
                        # Assigns the data in float format into a variable
                        masterVolume1 = float(serialData)
                        
                        # Changes the sessin volume to the desired volume (From 0.0 to 1.0)
                        volume2.SetMasterVolume(masterVolume1, None)
            
            
            # If the value starts with the indicator d, change the volume of any process you would like 
            if serialData.startswith("d"):
                
                # Loops through all the sessions currently running
                for session in sessions:
                    
                    # Initiates volume manipulation for processes  
                    volume3 = session._ctl.QueryInterface(ISimpleAudioVolume)
                    
                    # Checks if process is the one you want
                    if session.Process and session.Process.name() == "processC.exe":
                            
                        # Removes slider indicatr so we are left with the numerical value
                        serialData = serialData.replace("d", "")
                        
                        # Assigns the data in float format into a variable
                        masterVolume = float(serialData)
                        
                        # Changes the sessin volume to the desired volume (From 0.0 to 1.0)
                        volume3.SetMasterVolume(masterVolume, None)
                
            
            # If the value starts with the indicator c, mute the speakers 
            if serialData.startswith("e"):
                
                # Removes slider indicatr so we are left with the numerical value
                serialData = serialData.replace("e", "")
                
                # Mutes the speakers (1 muted, 0 un-muted)
                volume.SetMute(int(serialData), None)


# Prints exception error      
except Exception as e: 
    print(f"Error: {e}")

    
