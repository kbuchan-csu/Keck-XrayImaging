import tkinter as tk # import the UI package to main 
import UI # import custom UI elements to main
import sys
import stage.motor_ini.core as stg
import IStage

import json

# motor_id: motor
motors = {}

motor_id = 0
def add_motor_new_control(window, stages):
    global motor_id

    # TODO better stage selection
    motor = IStage.stage(stages[motor_id], motor_id)
    motor_control = UI.motor_controls(motor)
    motor_control.drawTo(window)

    motor_id += 1

    return motor_control

def save (active_motors):
    data = {}
    for motor in active_motors:
        data[motor.stage.port] = motor.stage.save()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(window, stages, active_motors):

    data = None

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(data)

    for key, value in data.items():
        for stage in stages:
            if stage.ser_port == key:
                motor = IStage.stage(stage, motor_id, value['name'], value['positions'], value['limits'], value['step'])
                motor_control = UI.motor_controls(motor)
                motor_control.drawTo(window)

                active_motors.append(motor_control)

def main () -> int:
    stages = list(stg.find_stages())
    active_motors = list()

    window = tk.Tk()
    window.title("Keck - XRay Imaging Sample Control")
    window.geometry("750x270")


    tk.Button(window, text="Add Motor", command=lambda: active_motors.append(add_motor_new_control(window, stages))).pack()
    tk.Button(window, text="Save", command=lambda: save(active_motors)).pack()
    tk.Button(window, text="Load", command=lambda: load(window, stages, active_motors)).pack()
    window.mainloop()
    
    return 0        # Return good exit code

if __name__ == "__main__":
    sys.exit(main())
    print("Exit")