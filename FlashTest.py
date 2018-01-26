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

aVal = 0

while True:
    sleepTime = (((aVal - 0) * (0.5 - 0.1)) / (255 - 0)) + 0.1
    pi.set_PWM_dutycycle(pinR, 255)
    pi.set_PWM_dutycycle(pinG, 0)
    pi.set_PWM_dutycycle(pinB, 0)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 0)
    pi.set_PWM_dutycycle(pinG, 255)
    pi.set_PWM_dutycycle(pinB, 0)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 0)
    pi.set_PWM_dutycycle(pinG, 0)
    pi.set_PWM_dutycycle(pinB, 255)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 255)
    pi.set_PWM_dutycycle(pinG, 255)
    pi.set_PWM_dutycycle(pinB, 0)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 255)
    pi.set_PWM_dutycycle(pinG, 0)
    pi.set_PWM_dutycycle(pinB, 255)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 0)
    pi.set_PWM_dutycycle(pinG, 255)
    pi.set_PWM_dutycycle(pinB, 255)
    time.sleep(sleepTime)
    
    pi.set_PWM_dutycycle(pinR, 255)
    pi.set_PWM_dutycycle(pinG, 255)
    pi.set_PWM_dutycycle(pinB, 255)
    time.sleep(sleepTime)
        
pi.stop

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
