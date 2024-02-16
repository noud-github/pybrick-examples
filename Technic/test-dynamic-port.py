from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port
from uerrno import ENODEV

inactivity_timer = StopWatch()
motor_timer = StopWatch()

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

# Make a list of known ports.
ports = [Port.A, Port.B]

# On hubs that support it, add more ports.
try:
    ports.append(Port.C)
    ports.append(Port.D)
except AttributeError:
    pass

# On hubs that support it, add more ports.
try:
    ports.append(Port.E)
    ports.append(Port.F)
except AttributeError:
    pass

sensor = None
motor = None

# Go through all available ports.
for port in ports:

    # Try to get the device, if it is attached.
    try:
        device = PUPDevice(port)
    except OSError as ex:
        if ex.args[0] == ENODEV:
            # No device found on this port.
            print(port, ": ---")
            continue
        else:
            raise

    # Get the device id
    id = device.info()["id"]

    # Look up the name.
    try:
        print(port, ":", device_names[id])
        if id == 37:
            if sensor is None:
                sensor = ColorDistanceSensor(port)
        if id == 47:
            if motor is None:
                motor = Motor(port)
                motor.dc(100)
    except KeyError:
        print(port, ":", "Unknown device with ID", id)

try:
    if sensor is not None:
        found_color = None
        found_angle = None
        while True:
            # Read the color.
            if motor is not None:
                angle = motor.angle()
                if found_angle != angle:
                    found_angle = angle
                    print(":" + str(angle))
                    inactivity_timer.reset()
            color = sensor.color()
            if color != found_color :
                # Print the measured color.
                print(color)
                found_color = color
                hub.light.on(color)
                inactivity_timer.reset()
            # Move the sensor around and see how
            # well you can detect colors.
            if inactivity_timer.time() > 120000:  # 2 minute in milliseconds
                print("time is up poweroff")
                hub.system.shutdown()
            if motor_timer.time() > 1200:  # 2 minute in milliseconds
                motor_timer.reset()
                motor_timer.pause()
                if motor is not None:
                    print("motor off")
                    motor.stop()
            # Wait so we can read the value.
            wait(100)
except OSError as ex :
    print("stopping")
    #hub.system.shutdown()
   
    
