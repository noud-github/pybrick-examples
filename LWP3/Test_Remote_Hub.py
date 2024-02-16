from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait

# This imports the DuploTrain from the duplo.py file.
from RemoteHub import RemoteHub

# Initialize the hub and devices. You can use any other hub too.
hub = TechnicHub()
#dial = Motor(Port.A)
sensor = ColorDistanceSensor(Port.A)

# Connect to the train.
test = RemoteHub()

# These variables are used to monitor the angle and color state.

last_color = Color.BLACK
hub.light.on(Color.CYAN)
test.light(Color.GREEN)
wait(1000)
while True:
    # If the measured color changed, play choo choo
    # and set the hub and train light to match.
    color = sensor.color()
    if last_color != color:
        last_color = color
        #if color != Color.NONE:
        #    train.choo_choo()
        hub.light.on(color)
        test.light(color)
        
    
    

