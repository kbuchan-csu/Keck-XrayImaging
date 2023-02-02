import tkinter as tk
import __main__

class motor_controls:
    def __init__ (self, stage, motor_id):
        self.stage = stage
        self.motor_id = motor_id

    def motor_position_update (self, text_area):
        text_area.config(text=f'{self.stage.pos:.5f}') # 5 decimal places after mm is 10 nm
        text_area.after(1, motor_update, text_area)

    def drawTo (self, parent):
        """
        -----------------------
        |     Stage Label     |
        -----------------------
        |    00.00000    | mm |
        -----------------------
        | ^ |   | /-\ |   | V |
        | ^ | ^ | |_| | V | V |
        -----------------------
        """
        motor_control = tk.Frame(parent)
        motor_control.pack()

        stage_label = tk.Label(motor_control, text=f'Motor {self.motor_id}')
        stage_label.grid(row=0, rowspan=1, column=0, columnspan=5)

        stage_position = tk.Label(motor_control, text="00.00000")
        stage_position.grid(row=1, rowspan=1, column=0, columnspan=3)
        # TODO Not the spot to put this, here for testing
        try:
            motor_position_update(stage_position)
        except:
            print("No more motors")

        units = tk.Label(motor_control, text="mm")
        units.grid(row=1, rowspan=1, column=3, columnspan=2)
        
        walk_up = tk.Button(motor_control, text="^^")
        walk_up.grid(row=2, rowspan=1, column=0)

        step_up = tk.Button(motor_control, text="^")
        step_up.grid(row=2, rowspan=1, column=1)

        home = tk.Button(motor_control, text="H")
        home.grid(row=2, rowspan=1, column=2)

        step_down = tk.Button(motor_control, text="V")
        step_down.grid(row=2, rowspan=1, column=3)

        walk_down = tk.Button(motor_control, text="VV")
        walk_down.grid(row=2, rowspan=1, column=4)