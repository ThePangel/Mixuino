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
import functools

isAssigned = False
portNum = 0


def portAssign():
    global isAssigned
    while isAssigned == False:
        global portNum
        
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
                

                for portNum in range(0, 9):
                    
                    if ("CH340") in p[1] and (f"COM{portNum}") in p[1]:
                        
                        isAssigned = True
                        return True
        time.sleep(5)


portAssign()
    
arduino = serial.Serial(port=f'COM{portNum}', baudrate=57600, timeout=.1) 

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

sessions = AudioUtilities.GetAllSessions()

stopb = False

def stop():
    global stopb
    stopb = True
    #print(stopb)
    icon.stop()
    

def slideAdress(icon, name):
    
    print(f"The process is {name}")
    def test(name):
         print(name)
    return test


def slider2(name):
     print(name)
def slider3(name):
     print(name)
    
def slider4(name):
     print(name)
    
def test():
    print("yes")    
    
icon = "E:\Code\ArduinoMixer\dist\LOGO.png"
image=Image.open(icon)   

  
global sessionsl
sessionsl = [] 
global sessionl
sessionl = [] 
funcvalue = [slider2, slider3, slider4 ]

#print(funcvalue[2])

for i in range(2, 5):
    n = 0
    for session in sessions:
        #x = lambda name = str(session.Process.name()), func = funcvalue[n]: slideAdress(name, func)
        #print(session.Process.name())
        sessionl.append(item(session.Process.name(), slideAdress(icon, session.Process.name())))
        lambda name=session.Process.name(): print(f"Lambda Called: {name}"); 
    #x()
    sessionsl.append(sessionl)
    sessionl = []
    n = n + 1


 

menu1 = (
    item("Slider2", Menu(*sessionsl[0]),),
    item("Slider3", Menu(*sessionsl[1]),),
    item("Slider4", Menu(*sessionsl[2]),),
    item("Exit", stop),
    )

icon = pystray.Icon(name="name", icon=image, title="Mixer", menu=menu1)

icon.run_detached()

try:
    while True:
        
        
        serialData = str(arduino.readline())
        #print(serialData)
       
        if stopb == True:
            #print(stopb)
            sys.exit()
            
              
      
        # Use parentheses to call the split method
        serialData = serialData.replace("b'", "").replace("\\n'", "").rstrip()
        
        #print(serialData)
        if serialData != "" and serialData[0] == "a":
            
            
            serialData = serialData.replace("a", "")
            masterVolume = float(serialData)
            #print(serialData)
            volume.SetMasterVolumeLevelScalar(masterVolume, None)   
        
        if serialData != "" and serialData[0] == "b":
            
            for session in sessions:
                volume1 = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == "brave.exe":
                
                    
                    serialData = serialData.replace("b", "")
                    masterVolume = float(serialData)
                    #print(serialData)   
                    volume1.SetMasterVolume(masterVolume, None)
        
        if serialData != "" and serialData[0] == "c":
            
            for session in sessions:
                volume2 = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == "Discord.exe":
                        
                        
                    serialData = serialData.replace("c", "")
                    masterVolume1 = float(serialData)
                    #print(serialData)   
                    volume2.SetMasterVolume(masterVolume1, None)
        
        if serialData != "" and serialData[0] == "d":
            
            for session in sessions:
                volume2 = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == "Discord.exe":
                        
                        
                    serialData = serialData.replace("d", "")
                    masterVolume = float(serialData)
                    #print(serialData)   
                    volume2.SetMasterVolume(masterVolume, None)
            
            
        
        if serialData != "" and serialData[0] == "e":
            
            serialData = serialData.replace("e", "")
            volume.SetMute(int(serialData), None)


       
except Exception as e:  # Catch specific exception for better error handling
    print(f"Error: {e}")

    
