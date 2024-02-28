from pybricks.iodevices import LWP3Device
from pybricks.parameters import Color, Port
from pybricks.tools import wait

# Device identifier for the Hub.

LEGO_BOOST_HUB_ID = 0x40
LEGO_TECHNIC_HUB_ID = 0x80
LEGO_CITY_HUB_ID = 0x41
LEGO_MARIO_HUB_ID = 0X43
LEGO_LUIGI_HUB_ID = 0X43
LEGO_PEACH_HUB_ID = 0X43

# sensor IDs
MARIO_HUB_PANT_SENSOR = 0x4A
MARIO_HUB_GESTURE_SENSOR = 0x47
MARIO_HUB_BARCODE_SENSOR = 0x49

TECHNIC_HUB_LED_PORT = 0x32
# quess:
CITY_HUB_LED_PORT = 0x32

PORTS = {
    Port.A: 0x00,
    Port.B: 0x01
}


# Mapping that converts colors to LEGO color identifiers.
COLORS = {
    Color.NONE: 0,
    #Color.PINK: 1,
    Color.MAGENTA: 2,
    Color.BLUE: 3,
    #Color.LIGHTBLUE: 4,
    Color.CYAN: 5,
    Color.GREEN: 6,
    Color.YELLOW: 7,
    Color.ORANGE: 8,
    Color.RED: 9,
    Color.WHITE: 10,
}

PORT_OUTPUT_COMAND = 0x81
PORT_OUTPUT_COMAND_SUB_COMMAND_DIRECT_WRITE = 0x51
PORT_INFORMATION_REQEST = 0x21

class RemoteHub():
    def __init__(self, hub_kind, name=None, timeout=10000):
        """Scans for a hub connect, and prepare it to receive commands."""
        print("Searching for the Hub. Make sure it is on.")
        self.device = LWP3Device(hub_kind, name=name, timeout=timeout)
        #self.battery = _Battery(self.device)

class RemoteTechnicHub(RemoteHub):
    """Class to connect to the Hub and send commands to it."""
    def __init__(self, name=None, timeout=10000):
        RemoteHub.__init__(self, LEGO_TECHNIC_HUB_ID, name, timeout)
        #self.device.write(bytes([0x0a, 0x00, 0x41, TECHNIC_HUB_LED_PORT, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01]))
        #self.device.write(bytes([0x0a, 0x00, 0x41, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01]))
        print("Connected!")
        wait(500)
        self.light = _Light(TECHNIC_HUB_LED_PORT, self.device)

    def ports():
        return [Port.A,Port.B,Port.C,Port.D]
    
class Remote_City_Hub():
    """Class to connect to the Hub and send commands to it."""
    def __init__(self, name=None, timeout=10000):
        RemoteHub.__init__(self, LEGO_TECHNIC_HUB_ID, name, timeout)
        #self.device.write(bytes([0x0a, 0x00, 0x41, TECHNIC_HUB_LED_PORT, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01]))
        #self.device.write(bytes([0x0a, 0x00, 0x41, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01]))
        print("Connected!")
        wait(500)
        self.light = _Light(CITY_HUB_LED_PORT_HUB_LED_PORT, self.device)

    def ports():
        return [Port.A,Port.B,]
    

class RemoteMario():
    """Class to connect to the Hub and send commands to it."""
    def __init__(self, name=None, timeout=10000):
        RemoteHub.__init__(self, LEGO_MARIO_HUB_ID, name, timeout)
        #self.device.write(bytes([0x0a, 0x00, 0x41, TECHNIC_HUB_LED_PORT, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01]))
        self.device.write(bytes([0x0a, 0x00, 0x41, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01]))
        print("Connected!")
        wait(500)
   
   

class _CommandBuilder():
    def __init__(self, MessageType, Port = None, PayloadValue = None, SubCommand = None, Mode = 0x00):
        # setup Header:
        # lenght
        # Hub ID NOT USE Always set to 0x00
        # Message Type
        self.list = [0x00,0x00,MessageType]

        if MessageType == PORT_OUTPUT_COMAND:
            # port
            self.list.append(Port)
            # Startup and Completion Information 0001 0001 (0x11) Execute immediately Command feedback (Status)
            self.list.append(0x11)
            # sub command
            self.list.append(SubCommand)
            # payload mode
            self.list.append(Mode)
            # payload value
            self.list.append(PayloadValue)
       
            #print(len(self.list))
        # set correct lenght        
        self.list[0] = len(self.list)  

        #print(len(self.list))          
        
    def __iter__(self):
        return iter(self.list)

    def __bytes__(self):
        return bytes(self.list)


class RemoteMotor():
    def __init__(self, port, remotehub):
        self.port = port
        self.remotehub = remotehub
    def angle():
        return 0
    def dc(self, power):
        command = _CommandBuilder( PORT_OUTPUT_COMAND, Port = PORTS[self.port], SubCommand = PORT_OUTPUT_COMAND_SUB_COMMAND_DIRECT_WRITE,  PayloadValue = power)

        self.remotehub.device.write(bytes(command))  


class _Battery():
    def __init__(self, device):
        self.device = device
    def voltage(self):
        return 50
    def current(self):
        return 50 


class _Light():
    def __init__(self, port, device):
        self.port = port
        self.device = device
    def on(self,color):
        if color not in COLORS:
            return
        command = _CommandBuilder( PORT_OUTPUT_COMAND, Port = self.port, SubCommand = PORT_OUTPUT_COMAND_SUB_COMMAND_DIRECT_WRITE,  PayloadValue = COLORS[color])
        self.device.write(bytes(command))  
    def off(self):
        command = _CommandBuilder( PORT_OUTPUT_COMAND, Port = self.port, SubCommand = PORT_OUTPUT_COMAND_SUB_COMMAND_DIRECT_WRITE,  PayloadValue = 0x00)
        self.device.write(bytes(command))  
        
