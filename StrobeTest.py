import pigpio

import multiprocessing
import time
import sys

pi = pigpio.pi()

global rPin
rPin = 17 #R pin
global gPin
gPin = 27 #G pin
global bPin
bPin = 22 #B pin

aVal = 0

pi.set_PWM_frequency(rPin, 200)
pi.set_PWM_frequency(gPin, 200)
pi.set_PWM_frequency(bPin, 200)

#pi.write(17, 1)
#print("Dass")
#time.sleep(1)
#print("Here")

sleepTime = 0.00000001

while True:
    #sleepTime = (((aVal - 0) * (0.01 - 0.0005)) / (255 - 0)) + 0.0005
    for strobeVal in range(0, 255, 1):
        print("+ ", strobeVal)
        pi.set_PWM_dutycycle(rPin, strobeVal)
        pi.set_PWM_dutycycle(gPin, strobeVal)
        pi.set_PWM_dutycycle(bPin, strobeVal)
        time.sleep(sleepTime)
        
    for strobeVal in range(255, 0, -1):
        print("- ", strobeVal)
        pi.set_PWM_dutycycle(rPin, strobeVal)
        pi.set_PWM_dutycycle(gPin, strobeVal)
        pi.set_PWM_dutycycle(bPin, strobeVal)
        time.sleep(sleepTime)
        
pi.stop

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
