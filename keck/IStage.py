import sys
import stage.motor_ini.core as stg

# Stage -> stage, name, step, saved_positions[], limits[], inverted, port(?)
class stage:
    def __init__ (self, stage, stage_id):
        self.stage = stage 
        self.id = stage_id
        self.name = f"stage {stage_id}"
        self.step_size = 0.000030 # Default 30 nm (smallest possible step size)
        self.acceleration = 0.
        self.platform = sys.platform

        if stage == "NOSTAGE":
            self.platform = "TEST"
        else:
            self.port = stage.ser_port

        print(self.platform)

        self.jog_id = 0
        

    @property
    def pos (self):
        if self.platform == 'linux':
            return self.stage.pos
        else:
            return -999

    def set_name (self, name):
        self.name = name

    def home (self):
        if self.platform == 'linux':
            self.stage.move_home(blocking=True)
        else:
            print("Platform not supported")

    def step (self, dist):
        if self.platform == 'linux':
            self.stage.move_by(dist, blocking=True)
        else:
            print("Platform not supported")

    def start_jog (self, direction, frame):
        self.velocity = self.step_size * direction
        self.jog(direction, frame)

    def jog (self, direction, frame):
        dt = 0.01
        lim = self.stage.max_vel
        self.velocity = max(min(self.velocity * direction + self.stage.accn * dt * direction, lim), -lim)  # max of 1 mm/ms
        if self.platform == 'linux':
            self.stage.move_by(self.velocity * dt, blocking=True)
        else:
            pass
        self.jog_id = frame.after(1, self.jog, direction, frame)

    def stop_jog (self, frame):
        frame.after_cancel(self.jog_id)