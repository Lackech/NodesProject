import sys
from socket import *
from fase3.Node import *
import csv

class NeighborServer:

    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(NEIGHBOR_SERVER_ADDRESS, NEIGHBOR_SERVER_MASCARA)

        self.allNeighbors = {}
        socketServer = socket(AF_INET, SOCK_DGRAM)
        socketServer.bind(("", NEIGHBOR_SERVER_ADDRESS))

        self.listener = threading.Thread(name='daemon', target=self.findNodeNeighbors())
        self.listener.setDaemon(True)
        self.listener.start()



    def uploadNeighborsTable(self,file):
        success = True

        try:
            csvarchivo = open(file)
            entrada = csv.DictReader(csvarchivo)
            for row in entrada:
                nodeAddress = (row[NODE_IP], row[NODE_PORT], row[NODE_MASCARA])
                nodeAddressValue = (row[NEIGHBOR_IP],row[NEIGHBOR_PORT],row[NEIGHBOR_MASCARA],row[DISTANE])
                # Tengo que pasarlo a listas
                self.allNeighbors[nodeAddress] = [nodeAddressValue]

        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success

    def findNodeNeighbors(self):
        while True:
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)
            decryptPacket = Node.decrypt(packetMessage)
            #Analizamos el paquete recibido y le enviamos sus vecinos
            if(decryptPacket[SERVER_REQUEST]):
                # Armo un paquete con los vecinos y lo envio
                pass







