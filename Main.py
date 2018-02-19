import threading
import pigpio
import multiprocessing

import BluetoothConnection
import LightControl
import HeightControl
import PcControl
import Indication

class Controller():
    def __init__(self):
        self.pi = pigpio.pi()
        
        self.lightQueue = multiprocessing.Queue()
        self.heightQueue = multiprocessing.Queue()
        self.pcQueue = multiprocessing.Queue()
        self.stateQueue = multiprocessing.Queue()
        
        self.bluetoothConnection = BluetoothConnection.BluetoothConnection(self.lightQueue, self.heightQueue, self.pcQueue, self.stateQueue)
        self.lightControl = LightControl.LightControl(self.pi, self.lightQueue, self.stateQueue)
        self.heightControl = HeightControl.HeightControl(self.pi, self.heightQueue)
        self.pcControl = PcControl.PcControl(self.pi, self.pcQueue)
        self.indication = Indication.Indication(self.pi)
        
        self.bluetoothConnection.start()
        self.lightControl.start()
        self.heightControl.start()
        self.pcControl.start()

if __name__ == '__main__':
    controller = Controller()
