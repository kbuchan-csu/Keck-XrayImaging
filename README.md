# Keck-XrayImaging
Real Space XRay Imaging

# Install
## Windows
Download all files from github repository then run
```
pip install -r requierments.txt
```
Follow these additional [install instructions](https://github.com/qpit/thorlabs_apt) (Only the Window/System32 directory seems to work)

The program should now run

## Linux
Download all files from github repository then run
```
pip install -r requierments.txt
```
Go [here](https://github.com/kzhao1228/pystage_apt/tree/master)
You will need to download the /stage/motor_ctrl/MG17APTServer.ini file as for some reason pip does not download it.
You will need to find the install location of the pystage_apt module and the place the afomentioned file in <location>/stage/motor_ctrl/

You will then need to go into /stage/motor_ini/core.py
and in the 
```
        try:
            #FIXME: this avoids an error related to https://github.com/walac/pyusb/issues/139
            #FIXME: this could maybe be solved in a better way?
            dev._langids = (1033, )
            # KDC101 3-port is recognized as FTDI in newer kernels
            if not (dev.manufacturer == 'Thorlabs' or dev.manufacturer == 'FTDI'):
                ### raise Exception('No manufacturer found')
                continue ### until the device is found
        except usb.core.USBError:
            print("No stage controller found: make sure your device is connected")
            break
```
change the "break" to a "continue", this fixes an issue where the scanning of stages stops when it finds any usb item that isn't stage, this includes the camera built into most laptops

After these changes are made the program should run without issues.

# How to use
