from nodes.node import *
from socket import *
import threading


class nodeTCP(Node):

    def __init__(self, serverIp, serverPort):
        Node.__init__(self, serverIp, serverPort)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.currentConnection = {}
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(1)
        print("The server is listening and ready to receive\n\n")
        while self.alive:
            connectionSocket, addr = self.serverSocket.accept()
            self.currentConnection[addr] = connectionSocket
            threading.Thread(target=self.listenMessage, args=(connectionSocket, addr)).start()

        print("I dont feel good Mr Stark...")

    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket):
        while True:
            try:
                #Optiene la información, sí es que la hay
                data = connectionSocket.recv(1024)
                if data:
                    #Decodifica la información
                    pass
                    #Da una respuesta al cliente
                else:
                    raise error('Client disconnected')
            except:
                connectionSocket.close()
                return False

    def send(self):
        #Pregunta por el puerto donde quiere enviar el mensaje
        serverName = input("\nGive me your bruhh's IP: ")
        serverMascara = input("\nGive me your bruhh's Mascara: ")
        serverPort = int(input("\nGive me the port: "))
        address = (serverName, serverPort)

        #Verifica si existe una conexión, de no ser así la crea y la guarda
        if self.currentConnection[address] is None:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            self.currentConnection[address] = clientSocket
        else:
            clientSocket = self.currentConnection[address]

        #Envía un mensaje codificado
        clientSocket.send(self.encode().encode('utf-8'))
        #Creamos un hilo para escuchar lo que responda la conexión.
        threading.Thread(target=self.listenMessage, args=(clientSocket, address)).start()


    # Método para borrar un nodo
    def kill(self):
        self.alive = False
        for key in self.connectionsNow:

