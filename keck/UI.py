import tkinter as tk
from tkinter import *
import stage.motor_ini.core as stg
import IStage

class motor_controls:
    def __init__ (self, stage: IStage.stage):
        self.stage = stage

    def motor_position_update (self, text_area):
        text_area.config(text=f'{self.stage.pos:.5f}') # 5 decimal places after mm is 10 nm
        text_area.after(1, self.motor_position_update, text_area)

    def edit_title (self, parent, label):
        """
        ----------------
        | Change Title |
        ----------------
        """
        edit_window = Toplevel(parent) # Child window 
        edit_window.geometry("200x200")  # Size of the window 
        edit_window.title("tmp")

        edit_window.bind('<Key>', lambda event: self.edit_close(event, edit_window))

        edit_window.wm_attributes('-type', 'splash')
        
        edit_window.focus_force()
        edit_window.lift()

        edit_box = tk.Entry(edit_window)
        edit_box.bind('<Key>', lambda event: self.update_title(edit_box, label))
        edit_box.insert(0, self.stage.name)
        edit_box.pack()

        edit_window.mainloop()

    def edit_close (self, event, window):
        if event.keycode == 36:
            window.destroy()

    def update_title (self, edit, label):
        self.stage.name = edit.get()
        label.config(text = self.stage.name)

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

        stage_label.bind('<ButtonPress-1>', lambda event: self.edit_title(motor_control, stage_label))

        stage_remove = tk.Button(motor_control, text="X")
        stage_remove.grid(row=0, rowspan=1, column=4, columnspan=1)

        stage_position = tk.Label(motor_control, text="00.00000")
        stage_position.grid(row=1, rowspan=1, column=0, columnspan=3)
        
        self.motor_position_update(stage_position)

        units = tk.Label(motor_control, text="mm")
        units.grid(row=1, rowspan=1, column=3, columnspan=2)
        
        walk_up = tk.Button(motor_control, text="^^")
        walk_up.grid(row=2, rowspan=1, column=0)

        walk_up.bind('<ButtonPress-1>', lambda event: self.stage.start_jog(1, motor_control))
        walk_up.bind('<ButtonRelease-1>', lambda event: self.stage.stop_jog(motor_control))

        step_up = tk.Button(motor_control, text="^", command=lambda: self.stage.step(self.stage.step_size))
        step_up.grid(row=2, rowspan=1, column=1)

        home = tk.Button(motor_control, text="H", command=self.stage.home)
        home.grid(row=2, rowspan=1, column=2)

        step_down = tk.Button(motor_control, text="V", command=lambda: self.stage.step(-self.stage.step_size))
        step_down.grid(row=2, rowspan=1, column=3)

        walk_down = tk.Button(motor_control, text="VV")
        walk_down.grid(row=2, rowspan=1, column=4)

        walk_down.bind('<ButtonPress-1>', lambda event: self.stage.start_jog(-1, motor_control))
        walk_down.bind('<ButtonRelease-1>',lambda event: self.stage.stop_jog(motor_control))

if __name__ == '__main__':
    window = tk.Tk()
    window.title("UI Test Envirment")
    window.geometry("750x270")

    test = IStage.stage("NOSTAGE", -999)

    motor_control = motor_controls(test)
    motor_control.drawTo(window)

    window.mainloop()