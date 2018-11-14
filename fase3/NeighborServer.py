import sys
from socket import *
from fase3.Node import *
import csv

class NeighborServer(Node):

    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,NEIGHBOR_SERVER_ADDRESS, NEIGHBOR_SERVER_MASCARA)

        self.allNeighbors = {}

        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.bind(("", 2000))


        self.listener = threading.Thread(name='daemon', target=self.findNodeNeighbors)
        self.listener.setDaemon(True)
        self.listener.start()



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

        while True:
            packetMessage, clientAddress = self.socketServer.recvfrom(2048)
            decryptPacket = self.bitnator.decrypt(packetMessage)

            #Analizamos el paquete recibido y le enviamos sus vecinos
            if(decryptPacket[SERVER_REQUEST] == 1):
                # Armo un paquete con los vecinos y lo envio
                ipRequest = decryptPacket[SOURCE_IP]
                portRequest = decryptPacket[SOURCE_PORT]
                # Ocupo la mascara, preguntarle a Fake si lo saco de aqui o si modificamos todo el resto
                dicAddress = (ipRequest,portRequest)
                listaVecinos = self.allNeighbors.get(dicAddress)
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
                    socketServer.sendto(encryptedMessage,(ipRequest,portRequest))









