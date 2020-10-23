# TA-IF
Interface for reading data from Technische Alternative's controllers with a Raspberry Pi

Tested with following controllers:
* HZR65
* UVR64

## Installation
This Python script depends on Python3 the pigpio library which can be installed on Raspberry Pi OS using this command:  

    apt install python3 python3-pigpio
    
Eventually you have to start the pigpio service:
    
    systemctl start pigpio
    
    
To autostart the service at boot enter

    systemctl enable pigpio


## Description
taif.py contains an example implementation at the end of the file, which simply returns all datasets returned within 10 seconds
