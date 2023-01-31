import tkinter as tk # import the UI package to main 
import UI # import custom UI elements to main
import sys
import stage.motor_ini.core as stg


def motor_update (text_area, stage):
    
    text_area.config(text=stage.pos)

    text_area.after(1, motor_update, text_area, stage)

def motor_control_frame (parent, stage: int):
    motor_control = tk.Frame(parent)
    position = tk.Label(motor_control, text="")
    position.pack()
    motor_update(position, stage)
    return motor_control

motor_id = 0
def add_motor_new_control(window, stages):
    global motor_id
    motor_control_frame(window, stages[motor_id]).pack()
    motor_id += 1


def main () -> int:
    stages = list(stg.find_stages())

    window = tk.Tk()
    window.title("Keck - XRay Imaging Sample Control")
    window.geometry("750x270")

    tk.Button(window, text="Add Motor", command=lambda: add_motor_new_control(window, stages)).pack()
    window.mainloop()

    return 0        # Return good exit code

if __name__ == "__main__":
    sys.exit(main())