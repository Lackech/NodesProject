import sys
from socket import *
from fase3.Node import *
import csv
import threading


class NeighborServer(Node):

    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,NEIGHBOR_SERVER_ADDRESS, NEIGHBOR_SERVER_MASCARA)

        self.allNeighbors = {}
        self.alive = True

        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketServer.bind(self.address)


        self.listener = threading.Thread(name='vecinillos', target=self.findNodeNeighbors)
        self.listener.setDaemon(True)
        self.listener.start()

        #self.nodeUDPMenu()





    def uploadNeighborsTable(self,fileName):
        success = True

        try:
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    # Lo metemos primero en el nodo que esta a la derecha
                    nodeAddress = (row[NODE_IP], int(row[NODE_PORT]))
                    nodeAddressValue = (row[NEIGHBOR_IP],int(row[NEIGHBOR_PORT]),int(row[NEIGHBOR_MASCARA]),int(row[DISTANCE]))

                    # Lo metemos en el nodo que esta de segundo
                    neighbourAddress = (row[NEIGHBOR_IP], int(row[NEIGHBOR_PORT]))
                    neighbourAddressValue = (row[NODE_IP], int(row[NODE_PORT]), int(row[NODE_MASCARA]), int(row[DISTANCE]))

                    # Lo agregamos a la lista para cada uno de los nodos anteriores
                    if self.allNeighbors.get(nodeAddress) is None:
                        self.allNeighbors[nodeAddress] = [nodeAddressValue]
                    elif not (nodeAddress in self.allNeighbors[nodeAddress]):
                            self.allNeighbors[nodeAddress].append(nodeAddressValue)

                    if self.allNeighbors.get(neighbourAddress) is None:
                        self.allNeighbors[neighbourAddress] = [neighbourAddressValue]
                    elif not (neighbourAddress in self.allNeighbors[neighbourAddress]):
                            self.allNeighbors[neighbourAddress].append(neighbourAddressValue)

        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success





    def findNodeNeighbors(self):
        while self.alive:
            packetMessage, clientAddress = self.socketServer.recvfrom(2048)
            decryptPacket = self.bitnator.decryptPacket(packetMessage)

            #Analizamos el paquete recibido y le enviamos sus vecinos
            if(decryptPacket[TYPE] == SERVER):
                # Obtengo la lista de vecinos
                listaVecinos = self.allNeighbors.get(clientAddress)

                if listaVecinos is not None:
                    # Armo el paquete que se va a enviar
                    encryptedMessage = self.bitnator.encryptNeighboursPacket(len(listaVecinos),listaVecinos)
                    self.socketServer.sendto(encryptedMessage,clientAddress)





    def nodeUDPMenu(self):
        print("Running")
        while self.alive:
            answer = input("Enter any number to close the server!")

            try:
                intAnswer = int(answer)
                if intAnswer != 9999:
                    self.alive = False
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            except:
                print(self.warningMessage + answer + self.invalidOptionMessage)





