import tkinter as tk # import the UI package to main 
from tkinter.filedialog import asksaveasfile, askopenfile
import UI # import custom UI elements to main
import sys
import IStage
import json

# PLATFORM SPECIFIC IMPORTS
platform = sys.platform
if platform == 'win32':
    import thorlabs_apt as apt          # windows thorlabs wrapper
    
elif platform == 'linux':
    import stage.motor_ini.core as stg  # linux thorlabs wrapper

motor_id = 0
motors = {}
active_motors = []

"""
    Thor labs 3 axis stage limits
        X axis upper limit: 22 mm
        Y axis upper limit: 22 mm
        Z axis upper limit: 24 mm
"""

def create_new_motor (stage, name=None, positions={}, limits={}, step=0.000030):
    if stage is None:
        return IStage.stage_none(stage, name, positions, limits, step)
    elif platform == 'win32':
        return IStage.stage_windows(stage[1], name, positions, limits, step)
    elif platform == 'linux':
        return IStage.stage_linux(stage, name, positions, limits, step)

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

    for SN, value in data.items():
        for sn, motor in motors.items():
            if int(sn) == int(SN):
                motor.load(value['name'], value['step'], value['positions'], value['limits'])
                break

    for motor in active_motors:
        motor.refresh_limits()

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
    
    if platform == 'win32':
        stages = apt.list_available_devices()
    elif platform == 'linux':
        stages = list(stg.find_stages())

    for stage in stages:
        motor = create_new_motor(stage)
        SN = motor.serial_number
        if SN not in motors:
            motors[SN] = motor
            active_motors.append(add_motor(window, SN))
    
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