try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print("Error importing RPi.GPIO.. Try running as admin")
    
from bluetooth import *
import time
import sys

print("Running version " + sys.version)


ledVal = {"R": 0, "G": 0, "B": 0, "A": 0}
ledValPrev = {"R": 0, "G": 0, "B": 0}

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

rPin = GPIO.PWM(11,490) #R pin
gPin = GPIO.PWM(13,490) #G pin
bPin = GPIO.PWM(15,490) #B pin

rPin.start(0) #Start R pin with a value of 0
gPin.start(0) #Start G pin with a value of 0
bPin.start(0) #Start B pin with a value of 0

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
def flash(aVal):
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
    
def strobe(aVal):
    for strobeVal in range(255):
        strobeVal = strobeVal + aVal
        if strobeVal > 255:
            strobeVal = 255
            
        ledVal["R"] = (255 - strobeVal)
        ledVal["G"] = (255 - strobeVal)
        ledVal["B"] = (255 - strobeVal)
        time.sleep(.05)
        
    for strobeVal in range(255):
        strobeVal = strobeVal + aVal
        if strobeVal > 255:
            strobeVal = 255
            
        ledVal["R"] = strobeVal
        ledVal["G"] = strobeVal
        ledVal["B"] = strobeVal
        time.sleep(.05)
    
def fade(aVal):
    ledVal["G"] = 0
    ledVal["B"] = 0
    
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["R"] = fadeVal
        time.sleep(.05)
        
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["R"] = (255 - fadeVal)
        time.sleep(.05)
        
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["G"] = fadeVal
        time.sleep(.05)
        
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["G"] = (255 - fadeVal)
        time.sleep(.05)
        
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["B"] = fadeVal
        time.sleep(.05)
        
    for fadeVal in range(255):
        fadeVal = fadeVal + aVal
        if fadeVal > 255:
            fadeVal = 255
            
        ledVal["B"] = (255 - fadeVal)
        time.sleep(.05)
        
def smooth(aVal):
    ledVal["R"] = 255
    ledVal["G"] = 0
    ledVal["B"] = 0
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["G"] = smoothVal
        time.sleep(.05)
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["R"] = (255 - smoothVal)
        time.sleep(.05)
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["B"] = smoothVal
        time.sleep(.05)
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["G"] = (255 - smoothVal)
        time.sleep(.05)
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["R"] = smoothVal
        time.sleep(.05)
        
    for smoothVal in range(255):
        smoothVal = smoothVal + aVal
        if smoothVal > 255:
            smoothVal = 255
            
        ledVal["B"] = (255 - smoothVal)
        time.sleep(.05)
        
def lightControl(data):
    if data[2] == "g": #Flash
        aVal = int(data[8:10], 16) / 510
        flash(aVal)
    
    elif data[2] == "h": #Strobe
        aVal = int(data[8:10], 16) / 255
        strobe(aVal)
        
    elif data[2] == "i": #Fade
        aVal = int(data[8:10], 16)
        fade(aval)
        
    elif data[2] == "j": #Smooth
        aVal = int(data[8:10], 16)
        smooth(aVal)
    
    else:
        rVal = (int(data[2:4], 16) * 100) / 255
        gVal = (int(data[4:6], 16) * 100) / 255
        bVal = (int(data[6:8], 16) * 100) / 255
        ledVal["R"] = rVal
        ledVal["G"] = gVal
        ledVal["B"] = bVal

def heightControl(action):
    if action == "G": #Top
        print("HERE")
        GPIO.output(pinMonitorUp, 1)
    elif action == "H": #Up
        GPIO.output(pinMonitorUp, 0)
    elif action == "I": #Stop
        GPIO.output(pinMonitorUp, 0)
        GPIO.output(pinMonitorDown, 0)
    elif action == "J": #Down
        GPIO.output(pinMonitorDown, 0)
    elif action == "K": #Bottom
        GPIO.output(pinMonitorDown, 1)

def pcControl(action):
    if action == "G": #On/Off
        GPIO.output(pinPcOnOff, 1)
    elif action == "H": #On/Off release
        GPIO.output(pinPcOnOff, 0)
    elif action == "I": #Reset
        GPIO.output(pinPcReset, 1)
    elif action == "J": #Reset release
        GPIO.output(pinPcReset, 0)
    
      
def getPrefix(data):
    if data[0] == "1": #System
        print(data)
    elif data[0] == "2": #Light control
        lightControl(data)
            
    elif data[0] == "3": #Height control
        heightControl(data[2])
        
    elif data[0] == "4": #PC control
        pcControl(data[2])

def changeLED():
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
            getPrefix(decodedData)
            changeLED();
    
    clientSock.close()
    print("Connection closed")
    
server_sock.close()
    

##GPIO.setmode(GPIO.BOARD)
##
##GPIO.setup(21, GPIO.OUT)
##
##GPIO.output(21, 1)
##    
##time.sleep(2)
##
##GPIO.output(21, 0)
##
### Clears the GPIO pins used
##GPIO.cleanup()
