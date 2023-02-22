import sys
import tkinter as tk
import stage.motor_ini.core as stg

# Stage -> stage, name, step, saved_positions[], limits[], inverted, port(?)
class stage:
    def __init__ (self, stage, stage_id):
        self.platform = sys.platform
        if stage == "NOSTAGE":
            self.platform = "TEST"
        else:
            self.port = stage.ser_port
        print(self.platform)


        self.stage = stage 
        self.id = stage_id
        self.name = tk.StringVar(value=f"stage {stage_id}")
        self.step_size = 0.000030 # Default 30 nm (smallest possible step size)
        self.acceleration = 0.

        self.poss = -999
        self.position = tk.StringVar(value=f'{self.pos:.5f}')

        self.jog_id = 0

    @property
    def pos (self):
        if self.platform == 'linux':
            return self.stage.pos
        else:
            return self.poss

    def home (self):
        if self.platform == 'linux':
            self.stage.move_home(blocking=True)
        else:
            self.poss = 0
            print("Platform not supported")

    def goto (self, position):
        if self.platform == 'linux':
            self.stage.set_pos(position, blocking=True)
        else:
            self.poss = position
            print("Platform not supported")

    def step (self, dist):
        if self.platform == 'linux':
            self.stage.move_by(dist, blocking=True)
        else:
            self.poss += dist
            print("Platform not supported")

    def start_jog (self, direction, frame):
        self.velocity = self.step_size * direction
        self.jog(direction, frame)

    def jog (self, direction, frame):
        dt = 0.01
        lim = self.stage.max_vel
        self.velocity = max(min(self.velocity * direction + self.stage.accn * dt * direction, lim), -lim)  
        if self.platform == 'linux':
            self.stage.move_by(self.velocity * dt, blocking=True)
        else:
            self.poss += self.velocity * dt

        self.jog_id = frame.after(1, self.jog, direction, frame)

    def stop_jog (self, frame):
        frame.after_cancel(self.jog_id)