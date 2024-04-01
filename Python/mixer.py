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
from functools import partial


# Setup global variables
global root
global stopb
stopb = False
global defHide

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
        if session not in configfile['slider1']:
            configfile['slider1'].append(session)
        else:
            configfile['slider1'].remove(session)
        write_yaml(configfile)
        root.after(0, update1)
    
    # Assigns the process for the 3º slider (1º slider is for master volume) and writes to the YAML file
    def assign2(session):
        if session not in configfile['slider2']:
            configfile['slider2'].append(session)
        else:
            configfile['slider2'].remove(session)
        write_yaml(configfile)
        root.after(0, update2)
    
    # Assigns the process for the 4º slider (1º slider is for master volume) and writes to the YAML file
    def assign3(session):
        if session not in configfile['slider3']:
            configfile['slider3'].append(session)
        else:
            configfile['slider3'].remove(session)
        write_yaml(configfile)
        root.after(0, update3)
        
    # Closes UI and the audio thread
    def close():
        global stopb
        stopb = True
        root.after(100, root.destroy)  
    
    # Hides UI window
    def hide():
        root.withdraw()

    # Sets the hideDeefault value
    def defaultHide():
        if configfile['hideDefault'] == True:
            configfile['hideDefault'] = False
            write_yaml(configfile)
        else:
            configfile['hideDefault'] = True
            write_yaml(configfile)

    # Updates checkboxes in the frame
    def update1(event=None):
        for widget in frame1.winfo_children():
            widget.destroy()
        i = 0
        sessions = AudioUtilities.GetAllSessions()
        for element in configfile['slider1']:
            isSelect = customtkinter.BooleanVar()
            isSelect.set(True)
            frame1.checkbox = customtkinter.CTkCheckBox(frame1, text=element, command=partial(assign1, element), variable=isSelect)
            frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
            i += 1
        for session in sessions:
            if session.Process is not None:
                if session.Process.name() not in configfile['slider1']:
                    frame1.checkbox = customtkinter.CTkCheckBox(frame1, text=session.Process.name(), command=partial(assign1, session.Process.name()))
                    frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
                i += 1
    
    # Updates checkboxes in the frame
    def update2(event=None):
        for widget in frame2.winfo_children():
            widget.destroy()
        i = 0
        sessions = AudioUtilities.GetAllSessions()
        for element in configfile['slider2']:
            isSelect = customtkinter.BooleanVar()
            isSelect.set(True)
            frame1.checkbox = customtkinter.CTkCheckBox(frame2, text=element, command=partial(assign2, element), variable=isSelect)
            frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
            i += 1
        for session in sessions:
            if session.Process is not None:
                if session.Process.name() not in configfile['slider2']:
                    frame1.checkbox = customtkinter.CTkCheckBox(frame2, text=session.Process.name(), command=partial(assign2, session.Process.name()))
                    frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
                i += 1
    
    # Updates checkboxes in the frame
    def update3(event=None):
        for widget in frame3.winfo_children():
            widget.destroy()
        i = 0
        sessions = AudioUtilities.GetAllSessions()
        for element in configfile['slider3']:
            isSelect = customtkinter.BooleanVar()
            isSelect.set(True)
            frame1.checkbox = customtkinter.CTkCheckBox(frame3, text=element, command=partial(assign3, element), variable=isSelect)
            frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
            i += 1
        for session in sessions:
            if session.Process is not None:
                if session.Process.name() not in configfile['slider3']:
                    frame1.checkbox = customtkinter.CTkCheckBox(frame3, text=session.Process.name(), command=partial(assign3, session.Process.name()))
                    frame1.checkbox.grid(row=i, column=0, padx=20, pady=5)
                i += 1

    # Checks if program must check the chckbox by default
    def checkHide(event=None):
        
        # Checks if window is hidden by default
        if configfile['hideDefault'] == True:
            defHide.set(True)
        else:
            defHide.set(False)
    
    
    
    # Sets display mode to system setting (dark || light)
    customtkinter.set_appearance_mode("system")
    
    # Sets color theme to dark blue 
    customtkinter.set_default_color_theme("dark-blue")

    # Initiates customtkinter
    root = customtkinter.CTk()

    

    # (Set the windows size to 300x1000 (works fine with 1080p))
    root.geometry("300x1000") 

    # Sets window title
    root.title("Mixuino")
    
    # Sets window icon
    root.iconbitmap(resource_path("logo.ico"))

    # Creates defHide var to check if checkbox must be checked by default
    defHide = customtkinter.BooleanVar()    
    
    # Creates frame and sets padding
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 2", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates scrollable frame 
    frame1 = customtkinter.CTkScrollableFrame(frame)
    frame1.pack(padx=5, pady=5)

    # When the mouse hovers above the scrollable frame refresh the programs
    frame1.bind('<Enter>', update1)
    
    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 3", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates scrollable frame 
    frame2 = customtkinter.CTkScrollableFrame(frame)
    frame2.pack(padx=5, pady=5)

    # When the mouse hovers above the scrollable frame refresh the programs
    frame2.bind('<Enter>', update2)

    # Creates label (text) and sets padding
    label = customtkinter.CTkLabel(master=frame, text="Slider 4", font=("roboto", 24))
    label.pack(pady=12, padx=12)

    # Creates scrollable frame 
    frame3 = customtkinter.CTkScrollableFrame(frame)
    frame3.pack(padx=5, pady=5)

    # When the mouse hovers above the scrollable frane refresh the programs
    frame3.bind('<Enter>', update3)

    # Creates button that hides the window when clicked
    button = customtkinter.CTkButton(frame, text="Hide to systray", command=hide)
    button.pack(padx=10, pady=10)
    
    # Creates checkbox that sets if the window should be hidden on startup
    hideDefault = customtkinter.CTkCheckBox(frame, text="Hide to systray on startup", command=defaultHide, variable=defHide)
    hideDefault.pack(padx=10, pady=10)
    
    # When window is close shut the program
    root.protocol("WM_DELETE_WINDOW", close)

    # Update defHide while starting the program
    root.after(0, checkHide)
    
    # Updates the programs shown in the frames
    root.after(0, update1)
    root.after(0, update2)
    root.after(0, update3)
    
    
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

                # Checks if the window must be hidden on startup
                if configfile['hideDefault'] == True:
                    root.after(0, root.withdraw())
            
            # Sets variable to true since the loop has run
            runOnce = True

            # Tries to execute the main script if else it exits with the error
            try:
                
                # Initializes a serialData variable useds to check if values have changed
                serialData1 = ""
                
                # Infinite loop to constantly monitor and change the audio volume
                while True:
                    
                    # Checks if it has to stop the program
                    if stopb:
                        root.after(50, root.destroy)
                        icon.stop()
                        sys.exit()
                    
                    # Stores the received data of the Arduino into the variable
                    serialData = str(arduino.readline().decode())
                    
                    # Removes the prefixes and suffixes from the data and removes unwanted spaces
                    serialData = serialData.replace("b'", "").replace("\\n'", "").rstrip()
                    
                    # Compares if values have changed so there is no need to change every second
                    if serialData1 != serialData:
                    
                        # Equals variables for comparisong in the next loop itiration
                        serialData1 = serialData

                        # Checks if the serial data is not empty
                        if serialData:
                            
                            # Adds the slider values to the slider list
                            slider = []
                            slider.append(serialData[0:4])   # Slider[0]
                            slider.append(serialData[4:8])   # Slider[1]
                            slider.append(serialData[8:12])  # Slider[2]
                            slider.append(serialData[12:16]) # Slider[3]
                            # Assigns the data in float format into a variable
                            masterVolume = float(slider[0])

                            # Changes the master volume to the desired volume (Since it's scalar the volume is from 0.0 to 1.0)
                            volume.SetMasterVolumeLevelScalar(masterVolume, None)

                            # Loops for each slider
                            for i in range(1,4):
                                
                                # Checks if the process is the one you want
                                for session in sessions:
                                        
                                        # Initiates volume manipulation for processes
                                        processedVolume = session._ctl.QueryInterface(ISimpleAudioVolume)
                                        
                                        # Checks if the process is the one you want
                                        if session.Process and session.Process.name() in configfile[f'slider{i}']:
                                            
                                            # Assigns the data in float format into a variable
                                            masterVolume = float(slider[i])   
                                            
                                            # Changes the session volume to the desired volume (From 0.0 to 1.0)
                                            processedVolume.SetMasterVolume(masterVolume, None)

                            # If the value starts with the indicator e, mute the speakers 
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

# Joins threads
audioThread.join()
guiThread.join()



