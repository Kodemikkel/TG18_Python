import pigpio
import time

class Indication():
    def __init__(self, pi, sendQueue):
        self.pi = pi
        self.pinWaterSwitch = 20 # Physical pin 38
        self.pinSodaSwitch = 21 # Physical pin 40
        self.pinWaterInd = 13 # Physical pin 33
        self.pinSodaInd = 19 # Physical pin 35

        self.pi.set_mode(self.pinWaterInd, pigpio.OUTPUT)
        self.pi.set_mode(self.pinSodaInd, pigpio.OUTPUT)
        self.pi.set_mode(self.pinWaterSwitch, pigpio.INPUT)
        self.pi.set_mode(self.pinSodaSwitch, pigpio.INPUT)

        self.pi.set_pull_up_down(self.pinWaterSwitch, pigpio.PUD_DOWN)
        # As the proximity switch used for detecting soda level has a built-in pullup resistor, we don't need to use RPi's internal

        self.pi.set_glitch_filter(self.pinWaterSwitch, 5000)
        self.pi.set_glitch_filter(self.pinSodaSwitch, 5000)

	self.sendQueue = sendQueue

        waterCallback = self.pi.callback(self.pinWaterSwitch, pigpio.EITHER_EDGE, self.indicateWater)
        sodaCallback = self.pi.callback(self.pinSodaSwitch, pigpio.EITHER_EDGE, self.indicateSoda)


    def indicateWater(self, gpio, level, tick):
        time.sleep(5) # Delay for 5 seconds to avoid false indication
        self.pi.write(self.pinWaterInd, self.pi.read(self.pinWaterSwitch))
        print("Water", gpio, level, tick)

    def indicateSoda(self, gpio, level, tick):
        time.sleep(2) # Delay for 2 seconds to avoid false indication
        self.pi.write(self.pinSodaInd, not self.pi.read(self.pinSodaSwitch))
	self.sendQueue.put(";1_G0000000") # Add message for indication of low soda to sendQueue
        print("Soda", gpio, level, tick)
