from socket import *
import threading

class NodeUdp:

    # constructor del nodo
    def __init__(self, serverAddress):
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)

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

    def send(self,otherAddress,messageList):
        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        clientSocket.sendto(self.encryptor.bitEncript(messageList),otherAddress)

        #Cerramos la conexión
        clientSocket.close()

    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False