from nodes.Node import Node
from socket import *
import threading

class nodeUDP(Node):

    # constructor del nodo
    def __init__(self, serverIp, serverPort):
        Node.__init__(self, serverIp, serverPort)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.currentConnection = []
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        print("Im working")

        while self.alive:
            sentence, clientAddress = self.serverSocket.recvfrom(2048)

            #Decodificamos el mensaje recibido

            #Retornamos una respuesta

        print("I dont feel good Mr Stark...")

    def send(self):
        #Pregunta por el puerto donde quiere enviar el mensaje
        serverName = input("\nGive me your bruhh's IP: ")
        serverMascara = input("\nGive me your bruhh's Mascara: ")
        serverPort = int(input("\nGive me the port: "))
        address = (serverName, serverPort)

        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        clientSocket.sendto(self.encode().encode('utf-8'), address)
        self.currentConnection.append(address)
        #Cerramos la conexión
        clientSocket.close()

    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False

        #Creamos el socket para enviar mensajes de que está mueriendo
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        for address in self.currentConnection:
            #Enviamos los mensajes a los diferentes address
            clientSocket.sendto('00000000'.encode('utf-8'), address)

        clientSocket.close()
