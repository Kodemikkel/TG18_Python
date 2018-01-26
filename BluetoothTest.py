import pigpio
from multiprocessing import Queue
import threading
from bluetooth import *
import time
import sys



# Function for setting up everything
def setup():
    print("Running version " + sys.version)
    global pi
    pi = pigpio.pi()

    global ledVal
    global ledValPrev
    ledVal = {"R": 0, "G": 0, "B": 0, "A": 0}
    ledValPrev = {"R": 0, "G": 0, "B": 0, "A": 0}

    global pinMonitorUp
    global pinMonitorDown
    global pinPcOnOff
    global pinPcReset
    global pinEndStopTop
    global pinEndStopBottom
    global pinLevelSwitch
    global pinProximitySwitch

    pinMonitorUp = 23#16
    pinMonitorDown = 24#18
    pinPcOnOff = 5#29
    pinPcReset = 6#31
    pinEndStopTop = 4#7
    pinEndStopBottom = 25#22
    pinLevelSwitch = 20#38
    pinProximitySwitch = 21#40
    
    global pinR
    global pinG
    global pinB
    pinR = 17 #11
    pinG = 27 #13
    pinB = 22 #15

    pi.set_PWM_frequency(pinR, 200)
    pi.set_PWM_frequency(pinG, 200)
    pi.set_PWM_frequency(pinB, 200)

    pi.set_PWM_dutycycle(pinR, 0)
    pi.set_PWM_dutycycle(pinG, 0)
    pi.set_PWM_dutycycle(pinB, 0)

    global aVal
    global mode
    aVal = 255
    mode = "solid"
            
# A thread for bluetooth
def bluetoothConnection(out_q):
        
    name = "Raspberry_BT_Server"
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    server_sock = BluetoothSocket(RFCOMM)

    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    advertise_service(server_sock, name,
                      service_id = uuid,
                      service_classes = [uuid, SERIAL_PORT_CLASS],
                      profiles = [SERIAL_PORT_PROFILE],
                      protocols = [OBEX_UUID])
    while True:
        global ledVal
        global mode
        global aVal
        print("Waiting for connection...")
        clientSock, address = server_sock.accept()
        print("Accepted connection from ", address)
        if mode == "flash":
            hexA = "0x{:02x}".format(aVal)[2:]
            clientSock.send(";1_G00000"+hexA)
        elif mode == "strobe":
            hexA = "0x{:02x}".format(aVal)[2:]
            clientSock.send(";1_H00000"+hexA)
        elif mode == "fade":
            hexA = "0x{:02x}".format(aVal)[2:]
            clientSock.send(";1_I00000"+hexA)
        elif mode == "smooth":
            hexA = "0x{:02x}".format(aVal)[2:]
            clientSock.send(";1_J00000"+hexA)
        else:
            hexR = "0x{:02x}".format(int(ledVal["R"]))[2:]
            hexG = "0x{:02x}".format(int(ledVal["R"]))[2:]
            hexB = "0x{:02x}".format(int(ledVal["R"]))[2:]
            hexA = "0x{:02x}".format(int(ledVal["R"]))[2:]
            clientSock.send(";1_"+hexR+hexG+hexB+hexA)

        while True:
            try:
                data = clientSock.recv(1024)
            except BluetoothError as e:
                break
            
            if len(data) == 0: break
            decoded = data.decode("utf-8")
            dataList = list(filter(None, decoded.split(";")));
            for decodedData in dataList:
                print("Received from device: " + decodedData)
                clientSock.send("Data recieved")
                out_q.put(decodedData)
        
        clientSock.close()
        print("Connection closed")
        
    server_sock.close()
    
    
# A thread for light control
def lightControl(in_q):
    while True:
        # Get data from the queue
        data = in_q.get()
        # Control the lights if the prefix matches lightControl
        if data[0] == "2": #Light control
            global aVal
            global mode
            global ledVal
            if data[2] == "G": #Flash
                aVal = int(data[8:10], 16)
                mode = "flash"
            
            elif data[2] == "H": #Strobe
                aVal = int(data[8:10], 16)
                mode = "strobe"
                
            elif data[2] == "I": #Fade
                aVal = int(data[8:10], 16)
                mode = "fade"
                
            elif data[2] == "J": #Smooth
                aVal = int(data[8:10], 16)
                mode = "smooth"
            
            else:
                mode = "solid"
                rVal = int(data[2:4], 16)
                gVal = int(data[4:6], 16)
                bVal = int(data[6:8], 16)
                aVal = int(data[8:10], 16)
                ledVal["A"] = aVal / 255
                ledVal["R"] = rVal * ledVal["A"]
                ledVal["G"] = gVal * ledVal["A"]
                ledVal["B"] = bVal * ledVal["A"]
                
def heightControl(in_q):
    while True:
        # Get data from the queue
        data = in_q.get()
        if data[0] == "3": #Height control
            if data[2] == "G": #Top
                pi.write(pinMonitorUp, 1)
            elif data[2] == "H": #Up
                pi.write(pinMonitorUp, 0)
            elif data[2] == "I": #Stop
                pi.write(pinMonitorUp, 0)
                pi.write(pinMonitorDown, 0)
            elif data[2] == "J": #Down
                pi.write(pinMonitorDown, 0)
            elif data[2] == "K": #Bottom
                pi.write(pinMonitorDown, 1)

def pcControl(in_q):
    while True:
        # Get data from the queue
        data = in_q.get()
        if data[0] == "4": #PC control
            if data[2] == "G": #On/Off
                pi.write(pinPcOnOff, 1)
            elif data[2] == "H": #On/Off release
                pi.write(pinPcOnOff, 0)
            elif data[2] == "I": #Reset
                pi.write(pinPcReset, 1)
            elif data[2] == "J": #Reset release
                pi.write(pinPcReset, 0)

setup()

# Create the shared queue and launch both threads
q = Queue()
lm_q = Queue()
t1 = threading.Thread(target=bluetoothConnection, args=(q,))
t2 = threading.Thread(target=lightControl, args=(q,))
t3 = threading.Thread(target=heightControl, args=(q,))
t4 = threading.Thread(target=pcControl, args=(q,))
t1.start()
t2.start()
t3.start()
t4.start()
while True:
    while mode == "flash":
        sleepTime = (((aVal - 0) * (0.5 - 0.1)) / (255 - 0)) + 0.1
        pi.set_PWM_dutycycle(pinR, 255)
        pi.set_PWM_dutycycle(pinG, 0)
        pi.set_PWM_dutycycle(pinB, 0)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 0)
        pi.set_PWM_dutycycle(pinG, 255)
        pi.set_PWM_dutycycle(pinB, 0)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 0)
        pi.set_PWM_dutycycle(pinG, 0)
        pi.set_PWM_dutycycle(pinB, 255)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 255)
        pi.set_PWM_dutycycle(pinG, 255)
        pi.set_PWM_dutycycle(pinB, 0)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 255)
        pi.set_PWM_dutycycle(pinG, 0)
        pi.set_PWM_dutycycle(pinB, 255)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 0)
        pi.set_PWM_dutycycle(pinG, 255)
        pi.set_PWM_dutycycle(pinB, 255)
        time.sleep(sleepTime)
        if mode != "flash": break
        
        pi.set_PWM_dutycycle(pinR, 255)
        pi.set_PWM_dutycycle(pinG, 255)
        pi.set_PWM_dutycycle(pinB, 255)
        time.sleep(sleepTime)
        if mode != "flash": break
        
    while mode == "strobe":
        sleepTime = (((aVal - 0) * (0.01 - 0.0005)) / (255 - 0)) + 0.0005
        for strobeVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinR, strobeVal)
            pi.set_PWM_dutycycle(pinG, strobeVal)
            pi.set_PWM_dutycycle(pinB, strobeVal)
            time.sleep(sleepTime)
        if mode != "strobe": break
            
        for strobeVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinR, strobeVal)
            pi.set_PWM_dutycycle(pinG, strobeVal)
            pi.set_PWM_dutycycle(pinB, strobeVal)
            time.sleep(sleepTime)
        if mode != "strobe": break
        
    while mode == "fade":
        sleepTime = (((aVal - 0) * (0.01 - 0.001)) / (255 - 0)) + 0.001
        pi.set_PWM_dutycycle(pinR, 0)
        pi.set_PWM_dutycycle(pinG, 0)
        pi.set_PWM_dutycycle(pinB, 0)
        
        for fadeVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinR, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
        
        for fadeVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinR, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
        
        for fadeVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinG, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
        
        for fadeVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinG, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
        
        for fadeVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinB, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
        
        for fadeVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinB, fadeVal)
            time.sleep(sleepTime)
        if mode != "fade": break
            
    while mode == "smooth":
        sleepTime = (((aVal - 0) * (0.05 - 0.0005)) / (255 - 0)) + 0.0005
        pi.set_PWM_dutycycle(pinR, 255)
        pi.set_PWM_dutycycle(pinG, 0)
        pi.set_PWM_dutycycle(pinB, 0)
        
        for smoothVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinG, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
        
        for smoothVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinR, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
        
        for smoothVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinB, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
        
        for smoothVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinG, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
        
        for smoothVal in range(0, 255, 1):
            pi.set_PWM_dutycycle(pinR, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
        
        for smoothVal in range(255, 0, -1):
            pi.set_PWM_dutycycle(pinB, smoothVal)
            time.sleep(sleepTime)
        if mode != "smooth": break
            
    while mode == "solid":
        if ledVal["R"] != ledValPrev["R"]:
            pi.set_PWM_dutycycle(pinR, ledVal["R"])
            ledValPrev["R"] = ledVal["R"]
        
        if ledVal["G"] != ledValPrev["G"]:
            pi.set_PWM_dutycycle(pinG, ledVal["G"])
            ledValPrev["G"] = ledVal["G"]
        
        if ledVal["B"] != ledValPrev["B"]:
            pi.set_PWM_dutycycle(pinB, ledVal["B"])
            ledValPrev["B"] = ledVal["B"]
            
        if ledVal["A"] != ledValPrev["A"]:
            pi.set_PWM_dutycycle(pinR, ledVal["R"])
            pi.set_PWM_dutycycle(pinR, ledVal["G"])
            pi.set_PWM_dutycycle(pinR, ledVal["B"])
            ledValPrev["A"] = ledVal["A"]

pi.stop()

