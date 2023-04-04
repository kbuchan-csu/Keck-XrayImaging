import tkinter as tk # import the UI package to main 
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

def create_new_motor (stage, name=None, positions=[], limits={}, step=0.000030):
    if platform == 'win32':
        return IStage.stage_windows(stage[1], name, positions, limits, step)
    elif platform == 'linux':
        return IStage.stage_linux(stage, name, positions, limits, step)

def add_motor_new_control(window, stages):
    global motor_id

    # TODO better stage selection
    motor = create_new_motor(stages[motor_id])
    
    motor_control = UI.motor_controls(motor)
    motor_control.drawTo(window)

    motor_id += 1

    return motor_control

def save (active_motors):
    data = {}
    for motor in active_motors:
        data[motor.stage.serial_number] = motor.stage.save()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(window, stages, active_motors):

    data = None

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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