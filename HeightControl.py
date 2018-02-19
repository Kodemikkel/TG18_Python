import threading
import pigpio

class HeightControl(threading.Thread):
    def __init__(self, pi, receiveQueue):
        print("Initializing HeightControl thread")
        threading.Thread.__init__(self)
        self.pi = pi
        self.pinUp = 23 # Physical pin 16
        self.pinDown = 24 # Physical pin 18
        self.pinTopPos = 4 # Physical pin 7
        self.pinBottomPos = 25 # Physical pin 22
        
        self.pi.set_mode(self.pinUp, pigpio.OUTPUT)
        self.pi.set_mode(self.pinDown, pigpio.OUTPUT)
        self.pi.set_mode(self.pinTopPos, pigpio.INPUT)
        self.pi.set_mode(self.pinBottomPos, pigpio.INPUT)
        
        self.pi.set_pull_up_down(self.pinTopPos, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(self.pinBottomPos, pigpio.PUD_DOWN)
        
        self.monitorThread = threading.Thread(target=self.monitorInput)
        self.receiveQueue = receiveQueue

        print("HeightControl thread initialized")

    def run(self):
        print("Starting HeightControl thread")
        self.monitorThread.start()
        while True:
            data = self.receiveQueue.get()
            if data[0] == "3": # Indicates data is for us
                if data[2] == "G" and not self.pi.read(self.pinTopPos): # Indicates "top" has been pressed or "up" is being held
                    print("Up")
                    self.pi.write(self.pinDown, 0)
                    self.pi.write(self.pinUp, 1)
                elif data[2] == "H": # Indicates "up" has been released
                    self.pi.write(self.pinUp, 0)
                elif data[2] == "I": # Indicates "stop" has been pressed
                    print("Stop")
                    self.pi.write(self.pinUp, 0)
                    self.pi.write(self.pinDown, 0)
                elif data[2] == "J": # Indicates "down" has been released
                    self.pi.write(self.pinDown, 0)
                elif data[2] == "K" and not self.pi.read(self.pinBottomPos): # Indicates "bottom" has been pressed, or "down" is being held
                    print("Down")
                    self.pi.write(self.pinUp, 0)
                    self.pi.write(self.pinDown, 1)
            elif data[0] == "0": # Indicates data is for some internal message
                if data[2] == "A": # Indicates user has disconnected
                    self.pi.write(self.pinUp, 0)
                    self.pi.write(self.pinDown, 0)

    def monitorInput(self):
        while True:
            if self.pi.read(self.pinTopPos):
                self.pi.write(self.pinUp, 0)
            if self.pi.read(self.pinBottomPos):
                self.pi.write(self.pinDown, 0)
