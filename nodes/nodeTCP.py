from nodes.node import *
from socket import *
import threading


class nodeTCP(Node):

    def __init__(self, serverIp, serverPort):
        Node.__init__(self, serverIp, serverPort)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.reachabilityTable = {}
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
            threading.Thread(target=self.listenMessage, args=(connectionSocket, addr)).start()

        print("I dont feel good Mr Stark...")

    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket, addr):
        print(addr)
        while True:
            try:
                data = connectionSocket.recv(1024)
                if data:
                    # Usa la información recibida como respuesta
                    response = data
                    connectionSocket.send(response)
                    print(data)
                else:
                    raise error('Client disconnected')
            except:
                connectionSocket.close()
                return False

    def send(self):
        serverName = input("\nGive me your bruhh's IP: ")
        serverPort = int(input("\nGive me the port: "))

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        # posible creacion de hilo
        clientSocket.send(self.encode().encode('utf-8'))
        modifiedSentence = clientSocket.recv(1024)
        print("From Server:"), modifiedSentence
