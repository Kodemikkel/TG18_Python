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

clientSock, address = server_sock.accept()
print("Accepted connection from ", address)

try:
    while True:
        data = clientSock.recv(1024)
        if len(data) == 0: break
        decoded = data.decode("utf-8")
        print("Received from device #1: " + decoded)
        
except IOError:
    pass

time.sleep(5)
print("Have slept")

clientSock.close()
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
