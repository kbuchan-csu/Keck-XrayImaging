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

"""
    Thor labs 3 axis stage limits
        X axis upper limit: 22 mm
        Y axis upper limit: 22 mm
        Z axis upper limit: 24 mm
"""

def create_new_motor (stage, name=None, positions={}, limits={IStage.UPPER: 21}, step=0.000030):
    if stage is None:
        return IStage.stage_none(stage, name, positions, limits, step)
    elif platform == 'win32':
        return IStage.stage_windows(stage[1], name, positions, limits, step)
    elif platform == 'linux':
        return IStage.stage_linux(stage, name, positions, limits, step)

def add_motor_new_control(window, stages):
    global motor_id

    # TODO better stage selection
    if motor_id < len(stages):
        motor = create_new_motor(stages[motor_id])
    else:
        motor = create_new_motor(None)
    
    motor_control = UI.motor_controls(motor)
    motor_control.drawTo(window)

    motor_id += 1

    return motor_control

def save (active_motors):
    data = {}
    for motor in active_motors:
        data[motor.stage.serial_number] = motor.stage.save()

    f = asksaveasfile(mode= 'w', initialfile='data.json', defaultextension='.json', filetypes=[("All Files","*.*"), ('JSON Files', '*.json')])
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
    """
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        """

def load(window, stages, active_motors):

    data = None
    f = askopenfile(mode='r', initialfile='data.json', defaultextension='.json', filetypes=[("All Files","*.*"), ('JSON Files', '*.json')])
    data = json.load(f)
    f.close()
    
    print(data)

    for SN, value in data.items():
        for stage in stages:
            test = create_new_motor(stage)
            if test.serial_number == int(SN):
                motor = create_new_motor(stage, value['name'], value['positions'], value['limits'], value['step'])
                motor_control = UI.motor_controls(motor)
                motor_control.drawTo(window)

                active_motors.append(motor_control)

def main () -> int:
    stages = []

    if platform == 'win32':
        stages = apt.list_available_devices()
    elif platform == 'linux':
        stages = list(stg.find_stages())

    active_motors = list()

    window = tk.Tk()
    window.title("Keck - XRay Imaging Sample Control")
    window.geometry("750x270")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    fileMenu = tk.Menu(menubar)
    fileMenu.add_command(label="Save", command=lambda: save(active_motors))
    fileMenu.add_command(label="Load", command=lambda: load(window, stages, active_motors))
    menubar.add_cascade(label="File", menu=fileMenu)

    tk.Button(window, text="Add Motor", command=lambda: active_motors.append(add_motor_new_control(window, stages))).pack()
    window.mainloop()
    
    return 0        # Return good exit code

if __name__ == "__main__":
    sys.exit(main())
    print("Exit")