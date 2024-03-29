from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait
from pybricks.tools import multitask, run_task

# This imports the DuploTrain from the duplo.py file.
from RemoteHub import RemoteTechnicHub, RemoteMotor, RemoteMario

print("start")

# Initialize the hub and devices. You can use any other hub too.
hub = TechnicHub()
sensor = ColorDistanceSensor(Port.A)

# connects but hangs
#mario = RemoteMario()


test = RemoteTechnicHub()
hub.light.on(Color.GREEN)
test.light.on(Color.GREEN)
wait(1000)

# print(str(test.battery.voltage()))

remotemotor = RemoteMotor(Port.A, test)
remotemotor.dc(50)
wait (2000)
remotemotor.dc(0)

def main():
    #global last_color
    last_color = Color.BLACK
    while True:
        # If the measured color changed, play choo choo
        # and set the hub and train light to match.
        color = sensor.color()
        if last_color != color:
            last_color = color
            test.light.on(color)
            hub.light.on(color)
        wait( 50)

def main2():
    last_color = Color.GREEN
    while True:
        # If the measured color changed, play choo choo
        # and set the hub and train light to match.
        if last_color == Color.GREEN:
            color = Color.RED
        if last_color == Color.RED:
            color = Color.GREEN
        if last_color != color:
            last_color = color
            test.light.on(color)
            hub.light.on(color)
        wait( 10)

main()


    

