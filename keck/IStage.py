import sys
import tkinter as tk

"""
# PLATFORM SPECIFIC IMPORTS + GUARDS
platform = sys.platform
if platform == 'win32':
    import thorlabs_apt as apt          # windows thorlabs wrapper

elif platform == 'linux':
    import stage.motor_ini.core as stg  # linux thorlabs wrapper
"""

from thorlabs_apt_device import KDC101

#import optosigma as OPTO
import __main__

# Limit types
LOWER = '0'
UPPER = '1'
STAGE = '2'

# Stage -> stage, name, step, saved_positions[], limits[]
class stage:
    def __init__ (self, stage, name: str = None, saved_positions: dict = {}, limits: dict = {}, step_size: float = 0.000030):
        self.stage = stage 

        if name is None:
            name = f"stage {self.serial_number}"

        self.name = tk.StringVar(value=name)
        self.step_size = step_size # Default 30 nm (smallest possible step size for thor labs motor)

        self.position = tk.StringVar(value=f'{self.pos:.5f}')

        self.saved_positions = saved_positions
        self.limits = limits

        self._jog_id = 0

    @property
    def pos (self) -> float:
        pass

    @pos.setter
    def pos (self, position: float) -> None:
        if not self.within_limits(position):
            return

    @property
    def serial_number (self):
        pass

    @property
    def max_velocity (self) -> float:
        pass

    @property
    def acceleration (self) -> float:
        pass

    def home (self) -> None:
        pass

    def set_home (self, position: float) -> None:
        pass

    def goto (self, position: float) -> None:
        if not self.within_limits(position):
            return

    def step (self, dist: float) -> None:
        if not self.within_limits(self.pos + dist):
            return

    def start_jog (self, direction: int, frame):
        self.velocity = self.step_size * direction
        self._jog(direction, frame)

    def _jog (self, direction: int, frame):
        dt = 0.001
        lim = self.max_velocity
        self.velocity = max(min(self.velocity + self.acceleration * dt * direction, lim), -lim)
        step_dist = self.velocity * dt
        self.step(step_dist)

        self._jog_id = frame.after(1, self._jog, direction, frame)

    def stop_jog (self, frame):
        frame.after_cancel(self._jog_id)

    def set_limit (self, limit_type, dist: float):
        if limit_type == LOWER or limit_type == UPPER:
            self.limits[limit_type] = dist

    def set_limit_stage (self, stage, parallel: int):
        big = max(self.pos, stage.pos)
        small = min(self.pos, stage.pos)
        dist = big + parallel * small
        self.limits[STAGE] = self.limits.get(STAGE) or {}
        stage.limits[STAGE] = stage.limits.get(STAGE) or {}

        if self.pos > stage.pos:
            left = self
            right = stage
        else:
            left = stage
            right = self

        self.limits[STAGE][str(stage.serial_number)] = {
            'dist': dist,
            'parallel': parallel,
            'left': [left.serial_number, left.pos],
            'right': [right.serial_number, right.pos]
        }
        stage.limits[STAGE][str(self.serial_number)] = {
            'dist': dist,
            'parallel': parallel,
            'left': [left.serial_number, left.pos],
            'right': [right.serial_number, right.pos]
        }

    def remove_limit (self, limit_type, stage=None):
        if limit_type == LOWER or limit_type == UPPER:
            self.limits.pop(limit_type)
        elif limit_type == STAGE: # Don't let two stages get closer than dist to each other
            if stage is None or stage is self:
                raise Exception("A seperate stage is requiered to gemove a stage limit")
            else:
                self.limits.pop(stage.serial_number)

    def save (self):
        SAVE = {
            'name': self.name.get(),
            'step': self.step_size,
            'positions': self.saved_positions,
            'limits': self.limits,
        }
        return SAVE

    def load (self, name, step_size, positions, limits):
        self.name.set(name)
        self.step_size = step_size
        self.saved_positions = positions
        self.limits = limits

        print(self.limits)

    def within_limits (self, pos: float) -> bool:
        """
        Antiparallel works perfectly
        Parallel works when left motor position > right motor position when set, or when right motor can not extedn into left motor
        if right motor can extend into left motor does not work
        """
        within = True
        for limit_type, dist in self.limits.items():
            # print(limit_type, dist, pos)
            if limit_type == LOWER:
                within = within and (pos >= dist)
            elif limit_type == UPPER:
                within = within and (pos <= dist)
            elif limit_type == STAGE:
                for SN, lim in dist.items():
                    motor = __main__.motors[int(SN)]
                    if lim['parallel'] == -1: # Parallel case
                        left = __main__.motors[lim['left'][0]]
                        right = __main__.motors[lim['right'][0]]

                        if left.serial_number == self.serial_number:
                            dist = pos - right.pos

                        else:
                            dist = left.pos - pos

                        if  dist > lim['dist']:
                            within = False

                    elif lim['parallel'] == 1: # Antiparallel case
                        within = pos + motor.pos <= lim['dist']
            if not within:
                break
        print (within)
        return within

    def save_position (self, pos_name: str) -> None:
        self.saved_positions[pos_name] = self.pos

    def goto_saved_position (self, pos_name: str) -> None:
        self.goto(self.saved_positions[pos_name])

class stage_linux (stage):
    """
        Class for Linux systems
        blocking = True --> Non blocking actions
        stage is the raw stage from `list(stg.find_stages())`
    """
    def __init__ (self, stage, name=None, saved_positions=[], limits=[], step_size=0.000030):
        super().__init__(stage, name=name, saved_positions=saved_positions, limits=limits, step_size=step_size)

    @property
    def pos (self):
        return self.stage.pos

    @pos.setter
    def pos (self, position):
        if not self.within_limits(position):
            return
        self.stage.set_pos(position, blocking=True)

    @property
    def serial_number (self):
        return self.stage.ser_no

    @property
    def max_velocity (self):
        return self.stage.max_vel

    @property
    def acceleration (self):
        return self.stage.accn

    def home (self):
        self.stage.move_home(blocking=True)

    def set_home (self, position):
        home_params = self.stage.get_move_home_params
        self.stage.set_home_params(home_params[0], home_params[1], home_params[2], home_offset_distance = position)

    def goto (self, position):
        if not self.within_limits(position):
            return
        self.stage.set_pos(position, blocking=True)

    def step (self, dist):
        if not self.within_limits(self.pos + dist):
            return
        self.stage.move_by(dist, blocking=True)

class stage_windows (stage):
    """
        Class for Windows systems
        blocking = False --> Non blocking actions
        serial_number is second number in `apt.list_available_devices()` tupel
    """
    def __init__ (self, serial_number, name=None, saved_positions=[], limits=[], step_size=0.000030):
        super().__init__(apt.Motor(serial_number), name=name, saved_positions=saved_positions, limits=limits, step_size=step_size)

    @property
    def pos (self):
        return self.stage.position

    @pos.setter
    def pos (self, position):
        if not self.within_limits(position):
            return
        self.stage.position = position

    @property
    def serial_number (self):
        return self.stage.serial_number

    @property
    def max_velocity (self):
        return self.stage.get_dc_joystick_parameters()[1]

    @property
    def acceleration (self):
        return self.stage.get_dc_joystick_parameters()[3]

    def home (self):
        self.stage.move_home(False)

    def set_home (self, position):
        home_params = self.stage.get_move_home_parameters()
        self.stage.set_move_home_parameters(home_params[0], home_params[1], home_params[2], position)

    
    def goto (self, position):
        if not self.within_limits(position):
            return
        self.stage.move_to(position, blocking=False)

    def step (self, dist):
        if not self.within_limits(self.pos + dist):
            return
        self.stage.move_by(dist, blocking=False)


# All distances are in encoder steps
# TODO convert between encoder steps and millimeters 
class stage_thorlabs (stage):
    def __init__ (self, stage, serno, name=None, saved_positions=[], limits=[], step_size=0.000030):
        super().__init__(stage, name, saved_positions, limits, step_size)
        self.serial_number = serno
    
    @property
    def pos (self):
        return self.stage.status['position']
    
    @pos.setter
    def pos (self, position):
        if not self.within_limits(position):
            return
        self.stage.move_absolute(position=position) 

    @property
    def serial_number(self):
        return self.serial_number
    
    @property
    def max_velocity (self):
        return self.stage.velparams_['max_velocity']

    @property
    def acceleration (self):
        return self.stage.velparams_['acceleration']
    
    def home (self):
        self.stage.home()

    def set_home (self, position):
        params = self.stage.homeparams_
        self.stage.set_home_params(params['home_velocity'], position)

    def goto (self, position):
        if not self.within_limits(position):
            return
        self.stage.move_absolute(position=position) 

    def step (self, dist):
        if not self.within_limits(self.pos + dist):
            return
        self.stage.move_relative(dist)

    # TODO implement jog from thorlabs_apt_device

class stage_none (stage):
    """
        Class for testing and unsuported systems
    """
    def __init__ (self, stage, name=None, saved_positions=[], limits=[], step_size=0.000030):
        self.poss = -999
        super().__init__(stage, name, saved_positions, limits, step_size)

    @property
    def pos (self):
        return self.poss

    @pos.setter
    def pos (self, position):
        self.poss = position

    @property
    def serial_number (self):
        return -99999

    @property
    def max_velocity (self):
        return 5

    @property
    def acceleration (self):
        return 0.05

    def home (self):
        self.poss = -999
    
    def goto (self, position):
        self.poss = position

    def step (self, dist):
        self.poss += dist