try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print("Error importing RPi.GPIO.. Try running as admin")
from queue import Queue
import threading
from bluetooth import *
import time
import sys

# Function for setting up everything
def setup():
    global ledVal
    ledVal = {"R": 0, "G": 0, "B": 0, "A": 0}
    global ledValPrev
    ledValPrev = {"R": 0, "G": 0, "B": 0}
    global lightFunction
    lightFunction = ""
    global aVal
    aVal = 0

    pinMonitorUp = 16
    pinMonitorDown = 18
    pinPcOnOff = 29
    pinPcReset = 31
    pinEndStopTop = 7
    pinEndStopBottom = 22
    pinLevelSwitch = 38
    pinProximitySwitch = 40

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pinMonitorUp, GPIO.OUT) #Monitor up
    GPIO.setup(pinMonitorDown, GPIO.OUT) #Monitor down

    GPIO.setup(pinPcOnOff, GPIO.OUT) #PC on/off
    GPIO.setup(pinPcReset, GPIO.OUT) #PC reset

    GPIO.setup(pinEndStopTop, GPIO.IN) #End stop top
    GPIO.setup(pinEndStopBottom, GPIO.IN) #End stop bottom

    GPIO.setup(11,GPIO.OUT) #R
    GPIO.setup(13,GPIO.OUT) #G
    GPIO.setup(15,GPIO.OUT) #B

    global rPin
    rPin = GPIO.PWM(11,490) #R pin
    global gPin
    gPin = GPIO.PWM(13,490) #G pin
    global bPin
    bPin = GPIO.PWM(15,490) #B pin

    rPin.start(0) #Start R pin with a value of 0
    gPin.start(0) #Start G pin with a value of 0
    bPin.start(0) #Start B pin with a value of 0

def flash():
    while True:
        global lightFunction
        global aVal
        if lightFunction == "flash":
            ledVal["R"] = 100
            ledVal["G"] = 0
            ledVal["B"] = 0
            time.sleep(aVal)

            ledVal["R"] = 0
            ledVal["G"] = 100
            ledVal["B"] = 0
            time.sleep(aVal)

            ledVal["R"] = 0
            ledVal["G"] = 0
            ledVal["B"] = 100
            time.sleep(aVal)

            ledVal["R"] = 100
            ledVal["G"] = 100
            ledVal["B"] = 0
            time.sleep(aVal)

            ledVal["R"] = 100
            ledVal["G"] = 0
            ledVal["B"] = 100
            time.sleep(aVal)

            ledVal["R"] = 0
            ledVal["G"] = 100
            ledVal["B"] = 100
            time.sleep(aVal)

            ledVal["R"] = 100
            ledVal["G"] = 100
            ledVal["B"] = 100
            time.sleep(aVal)

def strobe():
    while True:
        global lightFunction
        global aVal
        if lightFunction == "strobe":
            for strobeVal in range(100):
                strobeVal = strobeVal + aVal
                if strobeVal > 100:
                    strobeVal = 100

                ledVal["R"] = (100 - strobeVal)
                ledVal["G"] = (100 - strobeVal)
                ledVal["B"] = (100 - strobeVal)
                time.sleep(1)

            for strobeVal in range(100):
                strobeVal = strobeVal + aVal
                if strobeVal > 100:
                    strobeVal = 100

                ledVal["R"] = strobeVal
                ledVal["G"] = strobeVal
                ledVal["B"] = strobeVal
                time.sleep(1)

def fade():
    while True:
        global lightFunction
        global aVal
        if lightFunction == "fade":
            ledVal["G"] = 0
            ledVal["B"] = 0

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["R"] = fadeVal
                time.sleep(.05)

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["R"] = (100 - fadeVal)
                time.sleep(.05)

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["G"] = fadeVal
                time.sleep(.05)

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["G"] = (100 - fadeVal)
                time.sleep(.05)

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["B"] = fadeVal
                time.sleep(.05)

            for fadeVal in range(100):
                fadeVal = fadeVal + aVal
                if fadeVal > 100:
                    fadeVal = 100

                ledVal["B"] = (100 - fadeVal)
                time.sleep(.05)

def smooth():
    while True:
        global lightFunction
        global aVal
        if lightFunction == "smooth":
            ledVal["R"] = 100
            ledVal["G"] = 0
            ledVal["B"] = 0

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["G"] = smoothVal
                time.sleep(.05)

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["R"] = (100 - smoothVal)
                time.sleep(.05)

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["B"] = smoothVal
                time.sleep(.05)

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["G"] = (100 - smoothVal)
                time.sleep(.05)

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["R"] = smoothVal
                time.sleep(.05)

            for smoothVal in range(100):
                smoothVal = smoothVal + aVal
                if smoothVal > 100:
                    smoothVal = 100

                ledVal["B"] = (100 - smoothVal)
                time.sleep(.05)

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
        print("Waiting for connection...")
        clientSock, address = server_sock.accept()
        print("Accepted connection from ", address)

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
                clientSock.send("Data received")
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
        if data[0] == "2":
            global aVal
            global lightFunction
            if data[2] == "G": #Flash
                with threading.Lock():
                    aVal = ((int(data[8:10], 16) * 2.9) / 255) + 0.1
                    lightFunction = "flash"

            elif data[2] == "H": #Strobe
                with threading.Lock():
                    aVal = int(data[8:10], 16) / 255
                    lightFunction = "strobe"

            elif data[2] == "I": #Fade
                with threading.Lock():
                    aVal = int(data[8:10], 16)
                    lightFunction = "fade"

            elif data[2] == "J": #Smooth
                with threading.Lock():
                    aVal = int(data[8:10], 16)
                    lightFunction = "smooth"

                lightFunction = ""
                rVal = (int(data[2:4], 16) * 100) / 255
                gVal = (int(data[4:6], 16) * 100) / 255
                bVal = (int(data[6:8], 16) * 100) / 255
                ledVal["R"] = rVal
                ledVal["G"] = gVal
                ledVal["B"] = bVal

def changeLED():
    while True:
        if ledVal["R"] != ledValPrev["R"]:
            print(ledVal["R"])
            rPin.ChangeDutyCycle(ledVal["R"])
            ledValPrev["R"] = ledVal["R"]

        if ledVal["G"] != ledValPrev["G"]:
            print(ledVal["G"])
            gPin.ChangeDutyCycle(ledVal["G"])
            ledValPrev["G"] = ledVal["G"]

        if ledVal["B"] != ledValPrev["B"]:
            print(ledVal["B"])
            bPin.ChangeDutyCycle(ledVal["B"])
            ledValPrev["B"] = ledVal["B"]

# A thread for height control
def heightControl(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data


# A thread for pc control
def pcControl(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        print(data)

setup()

# Create the shared queue and launch both threads
q = Queue()
t1 = threading.Thread(target=bluetoothConnection, args=(q,))
t2 = threading.Thread(target=lightControl, args=(q,))
t3 = threading.Thread(target=changeLED)
t4 = threading.Thread(target=flash)
t5 = threading.Thread(target=strobe)
t6 = threading.Thread(target=fade)
t7 = threading.Thread(target=smooth)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
