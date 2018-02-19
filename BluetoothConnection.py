import threading
from bluetooth import *
import queue

class BluetoothConnection(threading.Thread):
    def __init__(self, lightQueue, heightQueue, pcQueue, stateQueue):
        print("Initializing BluetoothConnection thread")
        threading.Thread.__init__(self)
        self.name = "Raspberry_BT_Server"
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        self.serverSocket = BluetoothSocket(RFCOMM)
        self.clientSocket = ""
        self.address = ""
        self.lightQueue = lightQueue
        self.heightQueue = heightQueue
        self.pcQueue = pcQueue
        self.stateQueue = stateQueue

        self.serverSocket.bind(("", PORT_ANY))
        self.serverSocket.listen(1)

        advertise_service(self.serverSocket, self.name,
                          service_id = self.uuid,
                          service_classes = [self.uuid, SERIAL_PORT_CLASS],
                          profiles = [SERIAL_PORT_PROFILE],
                          protocols = [OBEX_UUID])

        print("BluetoothConnection thread initialized")

    def run(self):
        while True:
            print("Waiting for connection...")
            self.clientSocket, self.address = self.serverSocket.accept()
            print("Accepted connection from ", self.address, " syncing states...")
            self.syncStates()
            while True:
                try:
                    data = self.clientSocket.recv(1024)
                except BluetoothError as e:
                    break

                if len(data) == 0: break
                decoded = data.decode("utf-8")
                dataList = list(filter(None, decoded.split(";")))
                for decodedData in dataList:
                    print("Received from device: ", decodedData)
                    self.lightQueue.put(decodedData)
                    self.heightQueue.put(decodedData)
                    self.pcQueue.put(decodedData)

            self.clientSocket.close()
            self.lightQueue.put("0_A0000000") # Tell the system to save states
            self.heightQueue.put("0_A0000000") # Tell the system to save states
            self.pcQueue.put("0_A0000000") # Tell the system to save states
            print("Connection closed... states saved")

        self.serverSocket.close()

    def syncStates(self):
        while True:
            try:
                data = self.stateQueue.get(False)
                self.clientSocket.send(data)
                print("States synced: ", data)
            except queue.Empty:
                print("Nothing to sync")
                break
