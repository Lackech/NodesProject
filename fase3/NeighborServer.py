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

        self.uploadNeighborsTable("vecinos.csv")


        self.listener = threading.Thread(name='vecinillos', target=self.findNodeNeighbors)
        self.listener.setDaemon(True)
        self.listener.start()



        self.nodeUDPMenu()




    def uploadNeighborsTable(self,file):
        success = True

        try:
            csvarchivo = open(file)
            entrada = csv.DictReader(csvarchivo)
            for row in entrada:

                nodeAddress = (row[NODE_IP], row[NODE_PORT])
                nodeAddressValue = (row[NEIGHBOR_IP],row[NEIGHBOR_PORT],row[NEIGHBOR_MASCARA],row[DISTANE])
                # Tengo que pasarlo a listas
                listaValor = [nodeAddressValue]
                if self.allNeighbors.get(nodeAddress) is None:
                    self.allNeighbors[nodeAddress] = listaValor
                else:
                    lista = self.allNeighbors[nodeAddress]
                    listaValor.extend(lista)
                    self.allNeighbors[nodeAddress] = listaValor

        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success

    def findNodeNeighbors(self):
        self.socketServer.bind(("", 2000))

        while self.alive:
            packetMessage, clientAddress = self.socketServer.recvfrom(2048)
            decryptPacket = self.bitnator.decrypt(packetMessage)

            #Analizamos el paquete recibido y le enviamos sus vecinos
            if(decryptPacket[SERVER_REQUEST] == 1):
                # Armo un paquete con los vecinos y lo envio
                ipRequest = decryptPacket[SOURCE_IP]
                portRequest = decryptPacket[SOURCE_PORT]
                # Ocupo la mascara, preguntarle a Fake si lo saco de aqui o si modificamos todo el resto
                dicAddress = (ipRequest,str(portRequest))
                listaVecinos = self.allNeighbors.get(dicAddress)
                print("LLegue aca")
                if listaVecinos is not None:
                    # Armo el paquete para enviar
                    encryptedMessage = self.bitnator.encrypt(
                        addressOrigen=NEIGHBOR_SERVER_ADDRESS,
                        ps=0,
                        rs=1,
                        sa=0,
                        saAck=0,
                        act=0,
                        actAck=0,
                        type=0,
                        tv=len(listaVecinos),
                        data=listaVecinos
                    )
                    print("Antes de enviar")
                    self.socketServer.sendto(encryptedMessage,(ipRequest,portRequest))
                    print("Despues de enviar")




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





