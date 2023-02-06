import tkinter as tk # import the UI package to main 
import UI # import custom UI elements to main
import sys
import stage.motor_ini.core as stg
import IStage

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


def main () -> int:
    stages = list(stg.find_stages())
    active_motors = list()

    window = tk.Tk()
    window.title("Keck - XRay Imaging Sample Control")
    window.geometry("750x270")


    tk.Button(window, text="Add Motor", command=lambda: active_motors.append(add_motor_new_control(window, stages))).pack()
    window.mainloop()

    return 0        # Return good exit code

if __name__ == "__main__":
    sys.exit(main())
    print("Exit")