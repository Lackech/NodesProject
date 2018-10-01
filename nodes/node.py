import os
import sys
from nodes.bitnator import *

class Node:

    #Constructor de la clase nodo
    def __init__(self, serverAddress):
        self.serverAddress = serverAddress
        self.reachabilityTable = {}
        self.encryptor = Bitnator(self)

    def listen(self):
        #Debe ser sobreescrito por el método del nodo hijo
        pass

    def send(self,serverName,serverPort):
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
        else:
            self.reachabilityTable.update(d1)



    def closingConnection(self,connectionSocket,clientAddress):
        print("Deleting data")
        connectionSocket.close()
        self.currentConnection.pop(clientAddress)

        copy = self.reachabilityTable.copy()
        for addr in copy:
            value = self.reachabilityTable.get(addr)
            if value[1] == clientAddress:
                self.reachabilityTable.pop(addr)