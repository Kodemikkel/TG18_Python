import pigpio

import multiprocessing
import time
import sys

pi = pigpio.pi()

pinR = 17 #R pin
pinG = 27 #G pin
pinB = 22 #B pin

aVal = 0

pi.set_PWM_frequency(pinR, 200)
pi.set_PWM_frequency(pinG, 200)
pi.set_PWM_frequency(pinB, 200)

#pi.write(17, 1)
#print("Dass")
#time.sleep(1)
#print("Here")

aVal = 255

while True:
    sleepTime = (((aVal - 0) * (0.05 - 0.0005)) / (255 - 0)) + 0.0005
    pi.set_PWM_dutycycle(pinR, 255)
    pi.set_PWM_dutycycle(pinG, 0)
    pi.set_PWM_dutycycle(pinB, 0)
    
    for fadeVal in range(0, 255, 1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinG, fadeVal)
        time.sleep(sleepTime)
    
    for fadeVal in range(255, 0, -1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinR, fadeVal)
        time.sleep(sleepTime)
    
    for fadeVal in range(0, 255, 1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinB, fadeVal)
        time.sleep(sleepTime)
    
    for fadeVal in range(255, 0, -1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinG, fadeVal)
        time.sleep(sleepTime)
    
    for fadeVal in range(0, 255, 1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinR, fadeVal)
        time.sleep(sleepTime)
    
    for fadeVal in range(255, 0, -1):
        print(fadeVal)
        pi.set_PWM_dutycycle(pinB, fadeVal)
        time.sleep(sleepTime)
        
pi.stop

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
