from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port
from uerrno import ENODEV

crocodile=True

#hub = TechnicHub()
# Dictionary of device identifiers along with their name.
device_names = {
    # pybricks.pupdevices.DCMotor
    1: "Wedo 2.0 Medium Motor",
    2: "Powered Up Train Motor",
    # pybricks.pupdevices.Light
    8: "Powered Up Light",
    # pybricks.pupdevices.Motor
    38: "BOOST Interactive Motor",
    46: "Technic Large Motor",
    47: "Technic Extra Large Motor",
    48: "SPIKE Medium Angular Motor",
    49: "SPIKE Large Angular Motor",
    65: "SPIKE Small Angular Motor",
    75: "Technic Medium Angular Motor",
    76: "Technic Large Angular Motor",
    # pybricks.pupdevices.TiltSensor
    34: "Wedo 2.0 Tilt Sensor",
    # pybricks.pupdevices.InfraredSensor
    35: "Wedo 2.0 Infrared Motion Sensor",
    # pybricks.pupdevices.ColorDistanceSensor
    37: "BOOST Color Distance Sensor",
    # pybricks.pupdevices.ColorSensor
    61: "SPIKE Color Sensor",
    # pybricks.pupdevices.UltrasonicSensor
    62: "SPIKE Ultrasonic Sensor",
    # pybricks.pupdevices.ForceSensor
    63: "SPIKE Force Sensor",
    # pybricks.pupdevices.ColorLightMatrix
    64: "SPIKE 3x3 Color Light Matrix",
}
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

# Look up the name.
try:
    #print(Port.A, ":", device_names[id])
    if id == 2:
        print("train")
        crocodile=False
    elif id == 46:
        print("crocodile")
        crocodile=True
except KeyError:
    print(port, ":", "Unknown device with ID", id)

print(":" + str(crocodile))

if crocodile :
    train = Motor(Port.A)
    # Get the settings for this motor.
    max_speed, acceleration, torque = train.control.limits()

    # Change 0.5 to something smaller for more realism.
    train.control.limits(acceleration = acceleration * 0.5)
else:
    train = DCMotor(Port.A)

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
    if Button.RIGHT_PLUS in pressed:
        STEP_NOW += 1
    if Button.RIGHT_MINUS in pressed:
        STEP_NOW -= 1
    if Button.RIGHT in pressed:
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
    else:
        train.stop()

    # Wait for the button to be released.
    while pressed:
        pressed = remote.buttons.pressed()
        wait(10)
