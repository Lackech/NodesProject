from nodes.node import *
from socket import *
import threading

class NodeUdp(Node):

    # constructor del nodo
    def __init__(self, serverAddress):
        Node.__init__(self, serverAddress)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)


        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        print("Im working")

        while self.alive:
            sentence, clientAddress = self.serverSocket.recvfrom(2048)

            #Decodificamos el mensaje recibido
            self.decrypt(sentence,clientAddress)

            #Retornamos una respuesta

        self.serverSocket.close()
        print("I dont feel good Mr Stark...")

    def send(self,otherAddress):
        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        clientSocket.sendto(self.encode().encode('utf-8'), address)
        #Cerramos la conexión
        clientSocket.close()

    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False
