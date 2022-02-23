import serial.tools.list_ports
from time import sleep
import threading
import serial
import time

Robot_MODE = "MANU"

def ZUMO_Read():
    global Robot_MODE
    while True:
        cc = str(robot.readline())
        cc = cc[2:-5]
            
        if cc == "MANU":
            Robot_MODE = "MANU"
            print("Robot mode changed to : " + Robot_MODE)
        elif cc == "AUTO":
            Robot_MODE = "AUTO"
            print("Robot mode changed to : " + Robot_MODE)

def Get_Mode():
    global Robot_MODE
    return Robot_MODE

print("Looking for COM ports...")
ports = serial.tools.list_ports.comports(include_links=False)

if (len(ports) != 0): # if a COM port has been found

    print (str(len(ports)) + " active ports has been found") 

    for count, port in enumerate(ports, start=1) :  # Show name of all ports
        print(str(count) + ' : ' + port.device)

    Choosed_port = int(input('Choose the used port: '))

    print('1: 9600   2: 38400    3: 115200')

    baud = int(input('Choose a baud rate: '))

    if (baud == 1):
        baud = 9600
    if (baud == 2):
        baud = 38400
    if (baud == 3):
        baud = 115200

    port = ports[Choosed_port - 1].device

    # Connecting to the Pololu Zumo robot
    print('Connecting to ' + str(port) + ' with a baud rate of ' + str(baud))
    robot = serial.Serial(port, baud, timeout=1)

    t1 = threading.Thread(target=ZUMO_Read)
    # starting thread 1 for recieving from the zumo robot
    t1.start()
    
else: 
    print("No serial port has been found")
            

def Forward():
    print("Direction : Forward")
    robot.write(bytes("F", 'utf-8'))
    time.sleep(0.05)

def Backward():
    print("Direction : Backward")
    robot.write(bytes("B", 'utf-8'))
    time.sleep(0.05)

def Right():
    print("Direction : Right")
    robot.write(bytes("R", 'utf-8'))
    time.sleep(0.05)

def Left():
    print("Direction : Left")
    robot.write(bytes("L", 'utf-8'))
    time.sleep(0.05)

def Stop():
    print("Direction : Stop")
    robot.write(bytes("S", 'utf-8'))
    time.sleep(0.05)

def AUTO():
    global Robot_MODE
    print("Mode : Autonomous")
    Robot_MODE = "AUTO"
    robot.write(bytes("A", 'utf-8'))
    time.sleep(0.05)

def MANU():
    global Robot_MODE
    print("Mode : Manual")
    Robot_MODE = "MANU"
    robot.write(bytes("M", 'utf-8'))
    time.sleep(0.05)
    
