import tkinter as tk
import stage.motor_ini.core as stg
import IStage

class motor_controls:
    def __init__ (self, stage: IStage.stage):
        self.stage = stage

    def motor_position_update (self, text_area):
        text_area.config(text=f'{self.stage.pos:.5f}') # 5 decimal places after mm is 10 nm
        text_area.after(1, self.motor_position_update, text_area)
    
    def update (self, parent):
        pass

    def drawTo (self, parent):
        """
        -----------------------
        |    Stage Label  | X |
        -----------------------
        |   00.00000  |  mm   |
        -----------------------
        | ^ |   | /-\ |   | V |
        | ^ | ^ | |_| | V | V |
        -----------------------
        """
        motor_control = tk.Frame(parent)
        motor_control.pack()

        stage_label = tk.Label(motor_control, text=self.stage.name)
        stage_label.grid(row=0, rowspan=1, column=0, columnspan=4)

        stage_remove = tk.Button(motor_control, text="X")
        stage_remove.grid(row=0, rowspan=1, column=4, columnspan=1)

        stage_position = tk.Label(motor_control, text="00.00000")
        stage_position.grid(row=1, rowspan=1, column=0, columnspan=3)
        
        self.motor_position_update(stage_position)

        units = tk.Label(motor_control, text="mm")
        units.grid(row=1, rowspan=1, column=3, columnspan=2)
        
        walk_up = tk.Button(motor_control, text="^^")
        walk_up.grid(row=2, rowspan=1, column=0)

        step_up = tk.Button(motor_control, text="^")
        step_up.grid(row=2, rowspan=1, column=1)

        home = tk.Button(motor_control, text="H", command=self.stage.home)
        home.grid(row=2, rowspan=1, column=2)

        step_down = tk.Button(motor_control, text="V")
        step_down.grid(row=2, rowspan=1, column=3)

        walk_down = tk.Button(motor_control, text="VV")
        walk_down.grid(row=2, rowspan=1, column=4)

if __name__ == '__main__':
    window = tk.Tk()
    window.title("UI Test Envirment")
    window.geometry("750x270")

    test = IStage.stage("NOSTAGE", -999)

    motor_control = motor_controls(test)
    motor_control.drawTo(window)

    window.mainloop()