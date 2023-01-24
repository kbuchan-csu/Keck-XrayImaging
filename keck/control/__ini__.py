from stage.motor_ini.core import find_stages

stages = list(find_stages())

stage0 = stages[0]

print(stage0.status)