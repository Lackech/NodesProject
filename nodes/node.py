import os
import sys

class Node:

    #Constructor de la clase nodo
    def __init__(self, serverAddress):
        self.serverIp = serverAddress[0]
        self.serverPort = serverAddress[1]
        self.reachabilityTable = {}

    def listen(self):
        #Debe ser sobreescrito por el método del nodo hijo
        pass

    def send(self):
        # Debe ser sobreescrito por el método del nodo hijo
        pass

    def kill(self):
        #Debe ser sobrescrito por el método del nodo hijo
        pass

    def saveDataTable(self, address, mask, cost, senderAddress):
        key = (address, mask)
        value = (cost, senderAddress)
        d1 = {key: value}
        if self.reachabilityTable.get(key) is not None:
            row = self.reachabilityTable.get(key)
            if row[0] > cost:
                self.reachabilityTable.update(d1)
                print("Data updated")
        else:
            self.reachabilityTable.update(d1)
            print("Data inserted")

