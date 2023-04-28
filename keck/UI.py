import tkinter as tk
from tkinter import *
import IStage

class dropwindow (tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        height = parent.winfo_height()
        geometry = "+%d+%d" % (x, y + height)

        self.geometry(geometry)

        self.wm_attributes('-type', 'splash')
        self.focus_force()
        self.lift()

class editable_label (tk.Label):
    def __init__(self, parent, textvariable):
        tk.Label.__init__(self, parent, textvariable=textvariable)
        self.textvariable = textvariable
        self.bind('<ButtonPress-1>', lambda event: self.edit(self))

    def edit (self, parent):
        edit_window = dropwindow(parent)

        edit_window.geometry("200x200")  # Size of the window 
        edit_window.title("label edit")

        edit_window.bind('<Key>', lambda event: self.close(event, edit_window))

        edit_box = tk.Entry(edit_window, textvariable=self.textvariable)
        edit_box.icursor(len(self.textvariable.get()))
        edit_box.pack(fill=BOTH)

        edit_box.focus_set()

        edit_window.mainloop()

    def close (self, event, window):
        if event.keycode == 36:
            window.destroy()

class position (tk.Canvas):
    def __init__ (self, parent, stage):
        tk.Canvas.__init__(self, parent, width= 110, height= 20)
        self.stage = stage

        self.text = self.create_text(110/2, 20/2 + 4, text=stage.position.get(), fill='black', font=('Helvetica 10'), anchor="center")

        self.bind('<ButtonPress-1>', lambda event: self.setwindow(self))
        self.after(1, self.motor_position_update)

    def setwindow (self, parent):
        set_window = dropwindow(parent)

        set_window.geometry("200x200")  # Size of the window 
        set_window.title("set stage position")

        set_window.bind('<Key>', lambda event: self.check_close(event, set_window, pos))

        pos = StringVar(value=self.stage.position.get())

        edit_box = tk.Entry(set_window, textvariable=pos)
        edit_box.grid(row=0, rowspan=1, column=0, columnspan=2)

        cancel = tk.Button(set_window, text='Cancel', command=lambda: self.close(set_window))
        cancel.grid(row=1, rowspan=1, column=0, columnspan=1)

        move = tk.Button(set_window, text='Move', command=lambda: self.gotoPosition(set_window, pos))
        move.grid(row=1, rowspan=1, column=1, columnspan=1)

        edit_box.focus_set()

        set_window.mainloop()

    def check_close (self, event, window, value):
        if event.keycode == 36:
            self.gotoPosition(window, value)

    def gotoPosition (self, window, value):
        self.stage.goto(float(value.get()))
        self.close(window)

    def close (self, window):
        window.destroy()

    def motor_position_update (self):
        self.stage.position.set(f'{self.stage.pos:.5f}') # 5 decimal places after mm is 10 nm
        self.itemconfig(self.text, text=self.stage.position.get())
        self.after(1, self.motor_position_update)

class motor_controls:
    def __init__ (self, stage: IStage.stage):
        self.stage = stage

    def motor_position_update (self, text_area):
        text_area.config(text=f'{self.stage.pos:.5f}') # 5 decimal places after mm is 10 nm
        text_area.after(1, self.motor_position_update, text_area)

    def drawTo (self, parent):
        """
        r\c |  0  | 1 | 2 |  3  | 4 |
        --- =========================
         0  | Saved Positions |  X  |
        --- +-----------------------+
         1  |      Stage Label      |
        --- +-----------------------+
         2  |   00.00000      | mm  |
        --- +-----------------------+
         3  | << | < | > | >> | Lim |
        --- =========================
        """

        motor_control = tk.Frame(parent)
        motor_control.pack()

        # Drop down window for selecting and saving positions
        saved_positions = ...
        saved_positions.grid(row=0, rowspan=1, column=0, columnspan=4)

        
        
        # Button the closes the motor control UI
        close_button = ...
        close_button.grid(row=0, rowspan=1, column= 4, columnspan=1)

        
        
        # Label for the stage, can be editied when clicked 
        stage_label = editable_label(motor_control, self.stage.name)
        stage_label.grid(row=1, rowspan=1, column=0, columnspan=5)

        
        
        # Position of the stage, can be told to go to a psotion when clicked
        stage_position = position(motor_control, self.stage)
        stage_position.grid(row=2, rowspan=1, column=0, columnspan=4)

        
        
        # Units of position
        units = tk.Label(motor_control, text="mm")
        units.grid(row=2, rowspan=1, column=4, columnspan=1)

        
        
        # Button for walking the stage in negative direction
        walk_down = tk.Button(motor_control, text="<<")
        walk_down.grid(row=3, rowspan=1, column=0, columnspan=1)

        walk_down.bind('<ButtonPress-1>', lambda event: self.stage.start_jog(-1, motor_control))
        walk_down.bind('<ButtonRelease-1>',lambda event: self.stage.stop_jog(motor_control))

        
        
        # Button for stepping the stage in negative direction
        step_down = tk.Button(motor_control, text="<", command=lambda: self.stage.step(-self.stage.step_size))
        step_down.grid(row=3, rowspan=1, column=1, columnspan=1)

        
        
        # Button for stepping the stage in positive direction
        step_up = tk.Button(motor_control, text=">", command=lambda: self.stage.step(self.stage.step_size))
        step_up.grid(row=3, rowspan=1, column=2, columnspan=1)

        
        
        # Button for walking the stage in positive direction
        walk_up = tk.Button(motor_control, text=">>")
        walk_up.grid(row=3, rowspan=1, column=3, columnspan=1)

        walk_up.bind('<ButtonPress-1>', lambda event: self.stage.start_jog(1, motor_control))
        walk_up.bind('<ButtonRelease-1>', lambda event: self.stage.stop_jog(motor_control))

        
        
        # Dropdown window for setting the limits of a motor
        limit_set = ... 
        limit_set.grid(row=3, rowspan=1, column=4, columnspan=1)



    def drawTo_old (self, parent):
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

        stage_label = editable_label(motor_control, self.stage.name)
        stage_label.grid(row=0, rowspan=1, column=0, columnspan=4)

        stage_remove = tk.Button(motor_control, text="X")
        stage_remove.grid(row=0, rowspan=1, column=4, columnspan=1)


        # TODO Test with real motors
        stage_position = position(motor_control, self.stage) #tk.Label(motor_control, text="00.00000")
        stage_position.grid(row=1, rowspan=1, column=0, columnspan=3)
        
        #self.motor_position_update(stage_position)

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

# DEBUG functions
class UI_DEBUG:
    def __init__(self):
        self.id = -999

    def add_new_test_motor (self, window):
        test = IStage.stage_none(None, self.id)
        self.id -= 1

        motor_control = motor_controls(test)
        motor_control.drawTo(window)

        return motor_control

if __name__ == '__main__':

    debug = UI_DEBUG()
    test_motors = []

    window = tk.Tk()
    window.title("UI Test Envirment")
    window.geometry("750x270")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    fileMenu = tk.Menu(menubar)
    fileMenu.add_command(label="Save")
    fileMenu.add_command(label="Load")
    menubar.add_cascade(label="File", menu=fileMenu)

    tk.Button(window, text="Add Motor", command=lambda: test_motors.append(debug.add_new_test_motor(window))).pack()

    window.mainloop()