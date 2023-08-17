# Keck-XrayImaging
Real Space XRay Imaging

# Requierments
(Must be added to path)
- Python 3.10
- Git command line

# Install
## Windows
Download all files from github repository then run the installer

The Thorlabs stages will need to have virtual com port enabled in the device manager. This may or may not require the installation of the drivers from the Thorlabs website. The Virtual com port can be enabled by going to: Univeral Serial Bus Controllers --> APT USB Device --> Properties --> Advanced --> enable 'Load VCP'. This will have to be done for all APT USB Devices

## Linux
Download all files from github repository then run
```
pip install -r requierments.txt
```

# How to use
## General overview
When you open up the application there will be a short delay while the program finds the stages connected to the computer. The only time the program scans for stages is on start up.

When a stage is found there should be a control pannel the looks like this:
        
![Image of stage control](images/MotorControl.png)
        
This control pannel contains all the information about the stage. It contains at the top a dropdown of positions that the stage can go to. Then below that there is the name of the stage, which you can edit by left clicking on it. Then below that is the current position of the stage, you can tell the stage where to go by clicking on the position. The position reports in mm with percision to 10 nm as the stages are rated to within 30 nm percision. Below the position is the walk and stepping buttons. The "<<" and ">>" walk the stage by holding down the button. The "\<" and "\>" step the stage by 30 nm per press, the step appont can be changed in a saved config, but not in the program itself. Next to the walking and stepping is the limit setter, which allows for setting manual limits to the motor.
        
## More detail
![Image of stage positions dropdown ](images/PositionDropdown.png)
        
The position dropdown has the default buttons of "+" which adds a new named position at the current stage position, "Home" which homes the stage, and "Set Home" which sets the stages home to the current position. When a new position is added it get added to the bottom of the drop down and can be clicked to tell the mstage to go to that position at any point. Positions can only be deleted by editing the save file.
        
![Image of limit dropdown](images/LimitDropdown.png)
        
The limit dropdown contains the different types of limits which can be set. The MIN and MAX limits allows you to set the minnimum and maximum distance of the stages in mm. The MOTOR limit allows you to set limits between two stages. The limits distance is the current distance between the two stages. There are two types of motor limits, parallel and antiparallel. To create a parallel limit type in "p", "parallel", "+", "1", or "same" in the dialog box. Parallel motors currently only work when the "left" motor is behind the "right" motor, or when the "left" motor  can extend into the "right" motor. To create an antiparallel motor type in anyhting elxe into the dialog box. Anti parallel motros work with any two stages.

![Image of a dialog box](images/ExampleDialog.png)

You can type into the input box of a dialog. By pressing "confirm", or either enter key you will submit the value in the dialog box. If you press the esc key, "Cancel" or "X" the value in the dialog will be discareded.
        
## Config file
A config file is created by saving the current setup of stages, by going File --> Save. It is saved as a JSON file. To load a config file got to File --> Load.
        
Each stage is saved as the stage's serial number. The fields are as follows:
- The user created name of the stage
- The minimum step size in mm
- The list of positions
  - Each position is it's name followed by the position that the motor should go to.
- The list of limits
  - Each limit type has a number, where 0 is MIN, 1 is MAX, and 2 is MOTOR
    - Motor limits are saved as the serial number of linked stage followed by the distace between the two stages at time of creation, wheter of not the limit is parallel "-1" or antiparallel "1", the left stage (serial number and position at time of creation) and the right stage (serial number and position at time of creation)
        
Example of an entry in the config is:
```
  "27264725": {
        "name": "X-Axis Left",
        "step": 3e-05,
        "positions": {
            "Reset Position": 21.0
        },
        "limits": {
            "0": 0.0,
            "1": 22.0,
            "2": {
                "27263725": {
                    "dist": 10.0,
                    "parallel": -1,
                    "left": [
                        27264725,
                        12.0
                    ],
                    "right": [
                        27263725,
                        2.0
                    ]
                }
            }
        }
    }
```
# Additional
Thorlabs stages are homed on start up, so important locations before turning off the stages. Note: Thorlabs stages loose their position when they loose power.

# User guide
Default Limits:
Thorlabs: 0mm - 24mm

## General Use
1. Power on Computer
2. Power on Motors
3. If the lose power they will required to be homed or their position will be wrong
4. Launch application using ‘run.bat’
5. The thorlabs stages will automatically home when the application starts
6. Open up saved configuration by going to File → Load → \[configfile\].json

## UI Instruction
- Use the ‘<<’ & ‘>>’ for - and + jogging which stops when the button is released. When used on the current computer the jog is a little non-responsive and may take a moment to start and stop.

- Use the ‘<’ & ‘>’ for - and + stepping which only moves one step for every push of the button. Default step size is 30 nm.

- Press the position readout to tell the motor to go to a specific position in mm
- Press the name of the motor to rename it

- Click the ‘Home’ drop down to receive a list of saved positions, when selected the motor will move to that location and the dropdown's name will change
  - The ‘+’ will create a new saved position at the current location
  - The ‘Set Home’ button will set the home location to the current position

- Click the ‘limits’ drop down to set up limits for the motors to never exceed
  - The min and max limits will let you set them at any position from any position
  - The motor limits will set a limit of the current distance between the current motor and the motor selected in it’s drop down
  - The only way to remove limits and saved positions in by editing the configuration file

### Config editing
To edit the settings of the program you will have to locate and open the configuration file in a text editor such as notepad or notepad++. There you can edit the step size and remove saved locations or limits. When removing a limit the limit on both the current motor and the paired motor must be deleted.

Limit removal is done under the limits section of the motor which is identified by its com port. For removing a min or max limit delete the ‘0’ or ‘1’ entry line. For removing a motor limit you look under section ‘2’ and find the block that corresponds to the motor limit you are removing. A block contains the motor’s com port as an identifier, distance, parallel value, left, and right. You will need to remove this block to remove the limit.
If done incorrectly the config file will fail to load.

To remove a position you will need to find the position name and delete that line.

To save and load a configuration goto the top left of the application and click on file. There, the save and load options will be available. You will need to name your file every time you save and will have to select the correct configuration when loading. I suggest you know where these are saved.

## First run
When first run without having a configuration file you will want to identify the stages by setting a unique position and checking the controllers for the matching positions then renaming the stage in the application.

If a stage is not being detected it may be because it is either off, not plugged in, or not configured.

To configure a stage you must close the application and go to the windows ‘device manager’ and enable the virtual com port (VCP). To enable VCP you navigate through:Universal Serial Bus Controllers --> APT USB Device –(right click)-->  Properties --> Advanced --> enable 'Load VCP'. If the usb locations are changed this will have to be done again for every stage.

