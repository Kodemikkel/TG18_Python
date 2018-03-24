import threading

class PcControl(threading.Thread):
    def __init__(self, pi, receiveQueue):
        print("Initializing PcControl thread")
        threading.Thread.__init__(self)
        self.pi = pi
        self.pinOnOff = 5 # Physical pin 29
        self.pinRestart = 6 # Physical pin 31
        self.receiveQueue = receiveQueue

        print("PcControl thread initialized")

    def run(self):
        print("Starting PcControl thread")
        while True:
            data = self.receiveQueue.get()
            if data[0] == "4": # Indicates data is for us
                if data[2] == "G":
                    self.pi.write(self.pinOnOff, 0)
                elif data[2] == "H":
                    self.pi.write(self.pinOnOff, 1)
                elif data[2] == "I":
                    self.pi.write(self.pinRestart, 0)
                elif data[2] == "J":
                    self.pi.write(self.pinRestart, 1)
