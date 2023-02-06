import sys
import stage.motor_ini.core as stg

# Stage -> stage, name, step, saved_positions[], limits[], inverted, port(?)
class stage:
    def __init__ (self, stage, stage_id):
        self.stage = stage 
        self.id = stage_id
        self.name = f"stage {stage_id}"
        self.step = 0.000030 # Default 30 nm (smallest possible step size)
        self.platform = sys.platform

        if stage == "NOSTAGE":
            self.platform = "TEST"
        else:
            self.port = stage.ser_port

        print(self.platform)
        

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
            print("Not supported")