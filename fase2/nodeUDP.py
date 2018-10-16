from socket import *
from fase2.bitnator import *
import threading

class NodeUdp:

    # constructor del nodo
    def __init__(self, serverAddress):
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.connectionList = {}
        self.encryptor = Bitnator(self)

        self.alive = True

        self.listener = threading.Thread(name='daemon',target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()



    def listen(self):
        self.serverSocket.bind(self.serverAddress)

        while self.alive:
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

            if len(packetMessage) is 1:
                # Si es de tamaño 8 quiere decir que el address que envio el mensaje murió
                self.closingConnection(UDP, clientAddress)
                break
            else:
                # Decodifica la información
                self.encryptor.bitDecrypt(packetMessage, clientAddress)

                #Retornamos una respuesta

        self.serverSocket.close()
        print("I dont feel good Mr Stark...")



    # Metodo para comenzar la conexion con otro nodo
    def startConnection(self,otrherAddress):
        return 0



    # Metodo que cierra la conexion con el nodo seleccionado
    def closeConnection(self,nodeOption):
        return 0



    # Metodo que cierra todas las conexiones
    def closeAllConnection(self):
        return 0


    # Metodo que envia mensajes a otra conexion
    def send(self,nodeOption,message):
        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        clientSocket.sendto(self.encryptor.bitEncript(messageList),otherAddress)

        #Cerramos la conexión
        clientSocket.close()

    # Método que retorn un string con la lista de conexiones vivas
    def getConnectionList(self):
        stringList = ""
        num = 1

        for connection in self.connectionList:
            stringList += "\t" + num + ". (" + connection[0] + "," + connection[1] + ")\n"
            ++num

        return stringList



    # Metodo que retorna el numero de conexiones que hay abiertas en ese momento
    def numOpenConnections(self):
        return len(self.connectionList)