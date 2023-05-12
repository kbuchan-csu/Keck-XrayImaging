import tkinter as tk
#from tkinter import *
import IStage
import __main__

class popup (tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        geometry = "450x150"

        self.geometry(geometry)

        self.focus_force()
        self.lift()

class dialog (object):
    def __init__(self, parent, title, default_text=""):
        self.popup = popup(parent)
        self.popup.title(title)

        self.default_text = default_text

        self.popup.bind('<Key>', lambda event: self._close_onEvent(event))
        self.popup.protocol('WM_DELETE_WINDOW', lambda: self._close_noSave())

        frame = tk.Frame(self.popup)
        frame.pack()

        self.textvariable = tk.StringVar()
        self.textvariable.set(default_text)

        self.edit_box = tk.Entry(frame, textvariable=self.textvariable)
        self.edit_box.grid(row=0, rowspan=1, column=0, columnspan=2)

        cancel = tk.Button(frame, text="Cancel", command=lambda: self._close_noSave())
        cancel.grid(row=1, rowspan=1, column=0, columnspan=1)
        
        confirm = tk.Button(frame, text="Confirm", command=lambda: self._close_save())
        confirm.grid(row=1, rowspan=1, column=1, columnspan=1)

    def show(self):
        self.popup.wait_window()
        return self.textvariable.get()

    def _close_noSave(self):
        self.textvariable.set(self.default_text)
        self.popup.destroy()

    def _close_save(self):
        self.popup.destroy()

    def _close_onEvent(self, event):
        if event.keycode == 9:
            self._close_noSave()
        elif event.keycode == 36:
            self._close_save()
        elif event.keycode == 104:
            self._close_save()
        

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
        name = dialog(self, "Set Stage Name", default_text=self.textvariable.get()).show().strip()
        if name != "":
            self.textvariable.set(name)
            for motor in __main__.active_motors:
                motor.refresh_limits()

class position (tk.Canvas):
    def __init__ (self, parent, stage):
        tk.Canvas.__init__(self, parent, width= 110, height= 20)
        self.stage = stage

        self.text = self.create_text(110/2, 20/2 + 4, text=stage.position.get(), fill='black', font=('Helvetica 10'), anchor="center")

        self.bind('<ButtonPress-1>', lambda event: self.setwindow())
        self.after(1, self.motor_position_update)

    def setwindow (self):
        pos = float(dialog(self, "Set Position", default_text=f'{self.stage.pos:.5}').show())
        if pos <= self.stage.pos - 0.00029 or pos >= self.stage.pos + 0.00029:
            self.stage.goto(pos)

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

    def _save_position(self, drop_down, string_var):
        name = dialog(drop_down, "Name New Saved Position").show().strip()
        if name != "":
            if not (name in self.stage.saved_positions.keys()):
                drop_down['menu'].add_command(label=name, command=lambda: self._load_postion(string_var, name))
            self.stage.save_position(name)
            string_var.set(name)

    def _home_motor (self, string_var):
        self.stage.home()
        string_var.set("Home")

    def _set_motor_home (self, string_var):
        self.stage.set_home(self.stage.pos)
        string_var.set("Home")

    def _load_postion(self, string_var, name):
        string_var.set(name)
        self.stage.goto_saved_position(name)

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
        current_selected_position = tk.StringVar()
        current_selected_position.set('Saved Positions')
        
        saved_positions = tk.OptionMenu(motor_control, current_selected_position, [])
        saved_positions.grid(row=0, rowspan=1, column=0, columnspan=4)

        saved_positions['menu'].delete(0, 'end')
        saved_positions['menu'].add_command(label="+", command=lambda: self._save_position(saved_positions, current_selected_position))
        saved_positions['menu'].add_command(label="Home", command=lambda: self._home_motor(current_selected_position))
        saved_positions['menu'].add_command(label="Set Home", command=lambda: self._set_motor_home(current_selected_position))
        saved_positions['menu'].add_separator()

        for saved in self.stage.saved_positions.keys():
            saved_positions['menu'].add_command(label=saved, command=lambda: self._load_postion(current_selected_position, saved))
        
        """
        # Button to close the motor UI
        close_motor = ...
        close_motor.grid(row=0, rowspan=1, column=0, columnspan=5)
        """
        
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
        limit_name = tk.StringVar()
        limit_name.set("Limits")
        limit_set = tk.OptionMenu(motor_control, limit_name, [])
        limit_set.grid(row=3, rowspan=1, column=4, columnspan=1)

        limit_set['menu'].delete(0, 'end')
        limit_set['menu'].add_command(label="MIN", command=lambda: self._set_limit(limit_set, IStage.LOWER))
        limit_set['menu'].add_command(label="MAX", command=lambda: self._set_limit(limit_set, IStage.UPPER))

        self.avaliable_motors = tk.Menu(limit_set)

        self.refresh_limits()

        limit_set['menu'].add_cascade(label="MOTOR", menu=self.avaliable_motors)

    def refresh_limits(self):
        self.avaliable_motors.delete(0, 'end')

        for SN, motor in __main__.motors.items():
            if SN == self.stage.serial_number:
                continue
            else:
                p = self.avaliable_motors.add_command(label=motor.name.get(), command=lambda SN=SN: self._set_limit(p, IStage.STAGE, SN))

    def _set_limit(self, parent, limit_type, SN=-999):
        if SN != -999:
            motor = __main__.motors[SN]
            dir = dialog(parent, "Motor Direction").show()
            para = 1

            parallel = ['same', 'p', 'parallel', '+', '1']
            if dir in parallel:
                para = -1

            self.stage.set_limit_stage(motor, para)

        else:
            current_lim = self.stage.limits.get(limit_type)
            if current_lim is None:
                current_lim = ''
            pos = dialog(parent, "Set Motor Limit", current_lim).show()
            if pos != '':
                self.stage.set_limit(limit_type, float(pos))
        

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