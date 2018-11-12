import sys
from socket import *
from fase3.Node import *
import csv

class NeighborServer:

    def __init__(self, ip, port, mask):
        self.ipServer = ip
        self.portServer = port
        self.mask = mask
        self.allNeighbors = {}
        socketServer = socket(AF_INET, SOCK_DGRAM)
        socketServer.bind(("", port))



    def uploadNeighborsTable(self,file):
        success = True

        try:
            csvarchivo = open(file)
            entrada = csv.DictReader(csvarchivo)
            for row in entrada:
                nodeAddress = (row[NODE_IP], row[NODE_PORT])
                nodeMascara = row[NODE_MASCARA]
                nodeAddressValue = (row[NEIGHBOR_IP],row[NEIGHBOR_PORT])
                nodeMascaraValue = row[NEIGHBOR_MASCARA]
                self.allNeighbors[nodeAddress] = [nodeAddressValue]

        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success

    def findNodeNeighbors(self, ipNode, portNode, table):
        while True:
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

            #Analizamos el paquete recibido y le enviamos sus vecinos





