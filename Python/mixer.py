# Import of all required dependencies
from comtypes import CLSCTX_ALL
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
import serial
import pystray
from pystray import Menu, MenuItem as item
from PIL import Image
import sys
import serial.tools.list_ports
import time
import threading 
import customtkinter
import yaml
import os


# Setup global variables
global root
global stopb
stopb = False

# Write to the config file
def write_yaml(data):
   
    # Gets the binaries path
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # Construct the path to the YAML file in the script's directory
    yaml_path = os.path.join(script_dir, "processes.yaml")
    
    
    # Opens file
    with open(yaml_path, 'w') as file:
        
        # Writes to the file 
        yaml.dump(data, file)

# Read config file
def read_yaml():
    
    # Gets the binaries path
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # Construct the path to the YAML file in the script's directory
    yaml_path = os.path.join(script_dir, "processes.yaml")
    
    # Opens file
    with open(yaml_path, 'r') as file:
        
        # Loads file into variable
        global configfile
        configfile = yaml.safe_load(file)

# Sets path for when you use pyinstaller adding addiotional files (logo.png && logo.ico)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Reads file
read_yaml()

# GUI thread
def guiManipulator():
    
    # Set global variables
    global slide1
    global root

    # Initiates com library in current thread 
    comtypes.CoInitialize()

    # Assigns the process for the 2º slider (1º slider is for master volume) and writes to the YAML file
    def assign1(session):
        configfile['slider1'] = session
        write_yaml(configfile)
    
    # Assigns the process for the 3º slider (1º slider is for master volume) and writes to the YAML file
    def assign2(session):
        configfile['slider2'] = session
        write_yaml(configfile)
    
    # Assigns the process for the 4º slider (1º slider is for master volume) and writes to the YAML file
    def assign3(session):
        configfile['slider3'] = session
        write_yaml(configfile)
        
    # Closes UI and the audio thread
    def close():
        global stopb
        stopb = True
        root.after(100, root.destroy)  
    
    # Hides UI window
    def hide():
        root.withdraw()
    
    # Creates empty sessionList
    sessionList = []

    # Appends all current processes to sessionList and changes the values of the option menus
    def listUpdate(event=None):
        
        # Empties the list
        sessionList = []

        # Gets current processes
        sessions = AudioUtilities.GetAllSessions()
        
        # Appends all current processes to sessionList 
        for session in sessions:
            if session.Process is not None:
                
                # Appends the process name
                sessionList.append(session.Process.name())
        
        # Changes the dropdown value to the new list of processes 
        dropdown_menu1.configure(values=sessionList)
        dropdown_menu2.configure(values=sessionList)
        dropdown_menu3.configure(values=sessionList)
        
    
    # Sets display mode to system setting (dark || light)
    customtkinter.set_appearance_mode("system")
    
    # Sets color theme to dark blue 
    customtkinter.set_default_color_theme("dark-blue")

    # Initiates customtkinter
    root = customtkinter.CTk()

    # (Set the windows size to 300x400 (works fine with 1080p))
    root.geometry("300x400") 

    # Sets window title
    root.title("Mixuino")
    
    # Sets windopw icon
    root.iconbitmap(resource_path("logo.ico"))
    
    # Creates frame and sets padding
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 2", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates an optionmenu with the options being the values of sessionlist
    dropdown_menu1 = customtkinter.CTkOptionMenu(frame, values=sessionList, command=assign1)
    dropdown_menu1.pack(padx=10, pady=10)
    
    # Sets the displaying option as the option in the YAML file with key 'slider1'
    dropdown_menu1.set(configfile['slider1'])

    # When the mouse hovers above the option menu refresh the sessionlist
    dropdown_menu1.bind('<Enter>', listUpdate)

    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 3", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates an optionmenu with the options being the values of sessionlist
    dropdown_menu2 = customtkinter.CTkOptionMenu(frame, values=sessionList, command=assign2)
    dropdown_menu2.pack(padx=10, pady=10)
    
    # Sets the displaying option as the option in the YAML file with key 'slider2'
    dropdown_menu2.set(configfile['slider2'])

    # When the mouse hovers above the option menu refresh the sessionlist
    dropdown_menu2.bind('<Enter>', listUpdate)

    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 4", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates an optionmenu with the options being the values of sessionlist
    dropdown_menu3 = customtkinter.CTkOptionMenu(frame, values=sessionList, command=assign3)
    dropdown_menu3.pack(padx=10, pady=10)
    
    # Sets the displaying option as the option in the YAML file with key 'slider3'
    dropdown_menu3.set(configfile['slider3'])

    # When the mouse hovers above the option menu refresh the sessionlist
    dropdown_menu3.bind('<Enter>', listUpdate)
    
    # Creates button that hides the window when clicked
    button = customtkinter.CTkButton(frame, text="Hide to systray", command=hide)
    button.pack(padx=10, pady=10)
    
    # When window is close shut the program
    root.protocol("WM_DELETE_WINDOW", close)

    # Update the list for the first time while starting the program
    root.after(50, listUpdate)

    # Initiates the UI and the mainloop
    root.mainloop()    

# Audio manipulator thread
def audioManipulator():
        
        # Initializes de runOnce variable, used so even if the board disconnects, you dont create another systray icon
        runOnce = False
        
        while True:
            
            
            # Initiates com library in current thread 
            comtypes.CoInitialize()
            
            # Sets up global UI variable root to be able to close the window 
            global root

            # Initiates Variable used to check if the port is already assigned
            isAssigned = False

            # Initiates variable containing the COM port number
            portNum = 0

            # Function that assigns the COM port number where the Arduino Nano is connected
            def portAssign():
                
                # Makes the isAssigned variable globally accessible
                nonlocal isAssigned
                
                # Checks if the port is assigned
                while not isAssigned:
                    
                    # Makes the variable containing the COM port number globally accessible
                    nonlocal portNum
                    
                    # Makes a list of all COM ports and what's connected to them
                    ports = list(serial.tools.list_ports.comports())
                    
                    # Loops through all the ports
                    for p in ports:
                        
                        # Loops through all the possible COM ports that the Arduino Nano could be connected to
                        for portNum in range(0, 9):
                        
                            # Check if the device connected is the Arduino Nano
                            if "CH340" in p[1] and f"COM{portNum}" in p[1]:
                                
                                # Makes isAssigned true 
                                isAssigned = True
                                
                                # Returns the Function
                                return 
                    
                    # Delay for letting the function read the ports and not have them still open
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
            
            # Functions that stop the systray icon and set stopb to true so the loop exits the program 
            def stop():
                global stopb
                stopb = True
                
                icon.stop()

            def show():
                root.after(0, root.deiconify())

            # Checks if loop has been run so it doesn't create a new systray icon
            if runOnce == False:
                # Initiates systray menu with option "Exit" which calls the stop func
                menu1 = (item("Show", show), item("Exit", stop),)

                # File for the icon image (image or .ico)
                file = resource_path("logo.png")

                # Creates the systray icon object
                icon = pystray.Icon(name="name", icon=Image.open(file), title="Mixer", menu=menu1)

                # Initializes the systray icon in parallel so the script keeps running
                icon.run_detached()
            
            # Sets variable to true since the loop has run
            runOnce = True

            # Tries to execute the main script if else it exits with the error
            try:
                
                # Infinite loop to constantly monitor and change the audio volume
                while True:
                    
                    
                    
                    # Checks if it has to stop the program
                    if stopb:
                        root.after(50, root.destroy)
                        icon.stop()
                        sys.exit()
                    
                    
                    # Stores the received data of the Arduino into the variable
                    serialData = str(arduino.readline())
                    
                    # Removes the prefixes and suffixes from the data and removes unwanted spaces
                    serialData = serialData.replace("b'", "").replace("\\n'", "").rstrip()
                    
                    # Checks if the serial data is not empty
                    if serialData:
                        
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
                                
                                # Checks if the process is the one you want
                                if session.Process and session.Process.name() == configfile['slider1']:
                                    
                                    session.Process.name()
                                    # Removes slider indicator so we are left with the numerical value
                                    serialData = serialData.replace("b", "")
                                    
                                    # Assigns the data in float format into a variable
                                    masterVolume = float(serialData)   
                                    
                                    # Changes the session volume to the desired volume (From 0.0 to 1.0)
                                    volume1.SetMasterVolume(masterVolume, None)
                    
                        # If the value starts with the indicator c, change the volume of any process you would like 
                        if serialData.startswith("c"):
                        
                            # Loops through all the sessions currently running
                            for session in sessions:
                            
                                # Initiates volume manipulation for processes  
                                volume2 = session._ctl.QueryInterface(ISimpleAudioVolume)
                                
                                # Checks if the process is the one you want
                                if session.Process and session.Process.name() == configfile['slider2']:
                                    
                                    # Removes slider indicator so we are left with the numerical value
                                    serialData = serialData.replace("c", "")
                                    
                                    # Assigns the data in float format into a variable
                                    masterVolume1 = float(serialData)
                                
                                    # Changes the session volume to the desired volume (From 0.0 to 1.0)
                                    volume2.SetMasterVolume(masterVolume1, None)
                    
                        # If the value starts with the indicator d, change the volume of any process you would like 
                        if serialData.startswith("d"):
                        
                            # Loops through all the sessions currently running
                            for session in sessions:
                                
                                # Initiates volume manipulation for processes  
                                volume3 = session._ctl.QueryInterface(ISimpleAudioVolume)
                                
                                # Checks if the process is the one you want
                                if session.Process and session.Process.name() == configfile['slider3']:
                                
                                    # Removes slider indicator so we are left with the numerical value
                                    serialData = serialData.replace("d", "")
                                    
                                    # Assigns the data in float format into a variable
                                    masterVolume = float(serialData)
                                
                                    # Changes the session volume to the desired volume (From 0.0 to 1.0)
                                    volume3.SetMasterVolume(masterVolume, None)
                        
                        # If the value starts with the indicator c, mute the speakers 
                        if serialData.startswith("e"):
                        
                            # Removes slider indicator so we are left with the numerical value
                            serialData = serialData.replace("e", "")
                        
                            # Mutes the speakers (1 muted, 0 un-muted)
                            volume.SetMute(int(serialData), None)

            
            # Prints exception error      
            except Exception as e: 
                print(f"Error: {e}")
                arduino.close()


# Creates the GUI thread
guiThread = threading.Thread(target=guiManipulator)

# Create the Audio thread
audioThread = threading.Thread(target=audioManipulator)

# Starts threads
audioThread.start()
guiThread.start()


