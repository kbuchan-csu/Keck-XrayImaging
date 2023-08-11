import tkinter as tk # import the UI package to main 
from tkinter.filedialog import asksaveasfile, askopenfile
import UI # import custom UI elements to main
import sys
import IStage
import json
import re
    
from thorlabs_apt_device import KDC101
from thorlabs_apt_device.devices import aptdevice

import serial as ser
import serial.tools as serial
from optosigma import GSC01

THORLABS = 'thorlabs'
OPTOSIGMA = 'optosigma'

motor_id = 0
motors = {}
active_motors = []

"""
    Thor labs 3 axis stage limits
        X axis upper limit: 22 mm
        Y axis upper limit: 22 mm
        Z axis upper limit: 24 mm
"""

def create_new_motor (manufacturere, identifier, name=None, positions={}, limits={}, step=0.000030):
    if manufacturere == THORLABS:
        return IStage.stage_thorlabs(KDC101(identifier), identifier, name, positions, limits, step)
    elif manufacturere == OPTOSIGMA:
        return IStage.stage_optosigma(GSC01(identifier), identifier, name, positions, limits, step)

def save ():
    global motors
    data = {}
    for SN, motor in motors.items():
        data[SN] = motor.save()

    f = asksaveasfile(mode= 'w', initialfile='data.json', defaultextension='.json', filetypes=[("All Files","*.*"), ('JSON Files', '*.json')])
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

def load(window):
    global motors, active_motors

    data = None
    f = askopenfile(mode='r', initialfile='data.json', defaultextension='.json', filetypes=[("All Files","*.*"), ('JSON Files', '*.json')])
    data = json.load(f)
    f.close()
    
    print(data)

    for SN, settings in data.items():
        for sn, motor in motors.items():
            if sn == SN:
                motor.load(settings['name'], settings['step'], settings['positions'], settings['limits'])
                motor.refresh_positions()
                motor.refresh_limits()
                break
        

def add_motor (window, SN):
    global motors
    motor_control = UI.motor_controls(motors[SN])
    motor_control.drawTo(window)
    return motor_control

def refresh_motors(window):
    global motors, active_motors
    
    for motor in active_motors:
        motor.pack_forget()

    active_motors = []

    
    # Find thorlabs devices
    apt_devices = aptdevice.list_devices()
    print(apt_devices)
    devices = re.findall("(?<=device=)[A-Za-z0-9]*(?=, manufacturer=Thorlabs)", apt_devices)
    for device in devices:
        if device not in motors:
            motor = create_new_motor(THORLABS, device)
            motors[device] = motor
            active_motors.append(add_motor(window, device))
    
    """
    # Find optosigma devices
    #optosigma_devices = serial.grep("optosigma")
    devices = re.findall("(?<=device=)[A-Za-z0-9]*(?=, manufacturer=Prolific)", apt_devices)
    for device in devices:
        if device not in motors:
            motor = create_new_motor(OPTOSIGMA, device)
            motors[device] = motor
            active_motors.append(add_motor(window, device))
    """
    
    for motor in active_motors:
        motor.refresh_limits()

def main () -> int:
    window = tk.Tk()
    window.title("Keck - XRay Imaging Sample Control")
    window.geometry("750x270")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    fileMenu = tk.Menu(menubar)
    fileMenu.add_command(label="Save", command=lambda: save())
    fileMenu.add_command(label="Load", command=lambda: load(window))
    menubar.add_cascade(label="File", menu=fileMenu)

    refresh_motors(window)
    window.mainloop()
    
    return 0        # Return good exit code

if __name__ == "__main__":
    sys.exit(main())
    print("Exit")