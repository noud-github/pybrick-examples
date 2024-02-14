from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, DCMotor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port
from uerrno import ENODEV

crocodile=True
dual_motor=False

# Try to get the device, if it is attached.
try:
    device = PUPDevice(Port.A)
except OSError as ex:
    if ex.args[0] == ENODEV:
        # No device found on this port.
        print(Port.A, ": ---")
    else:
        raise

# Get the device id
id = device.info()["id"]

if id == 2:
    print("Train Motor")
    crocodile=False
    # Try to get the device, if it is attached.
    try:
        device = PUPDevice(Port.B)
    except OSError as ex:
        if ex.args[0] == ENODEV:
            # No device found on this port.
            print("Single Motor")
        else:
            raise
    if (device.info()["id"] == 2):
        print("Dual Motor")
        dual_motor=True

elif id == 46:
    print("Crocodile Motor")
    crocodile=True




if crocodile :
    train = Motor(Port.A)
    # Get the settings for this motor.
    max_speed, acceleration, torque = train.control.limits()

    # Change 0.5 to something smaller for more realism.
    train.control.limits(acceleration = acceleration * 0.5)
else:
    train = DCMotor(Port.A,Direction.CLOCKWISE)
    if dual_motor:
        train2 = DCMotor(Port.B,Direction.COUNTERCLOCKWISE)

remote = Remote()

# Choose how many speeds steps you want.
NUM_STEPS = 10
STEP_NOW = 0

while True:

    # Wait for any button to be pressed.
    pressed = ()
    while not pressed:
        pressed = remote.buttons.pressed()
        wait(10)

    # Depending on what was pressed, get the speed level.
    if Button.LEFT_PLUS in pressed:
        STEP_NOW += 1
    if Button.LEFT_MINUS in pressed:
        STEP_NOW -= 1
    if Button.LEFT in pressed:
        STEP_NOW = 0

    # Limit level to the maximum number of steps.
    STEP_NOW = max(-NUM_STEPS, min(STEP_NOW, NUM_STEPS))
    print("Speed level:", STEP_NOW)

    # Drive the train at the requested speed.
    if STEP_NOW:
        if crocodile :
            train.run(max_speed * STEP_NOW // NUM_STEPS)
        else:
            train.dc(10 * STEP_NOW)
            if dual_motor:
                train2.dc(10 * STEP_NOW)
    else:
        train.stop()
        if dual_motor:
            train2.stop()

    # Wait for the button to be released.
    while pressed:
        pressed = remote.buttons.pressed()
        wait(10)
