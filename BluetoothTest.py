try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print("Error importing RPi.GPIO.. Try running as admin")
    
from bluetooth import *
import time
import sys

print("Running version " + sys.version)

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
