from nodes.Node import Node
from socket import *
import threading

class nodeUDP(Node):

    # constructor del nodo
    def __init__(self, serverIp, serverPort):
        Node.__init__(self, serverIp, serverPort)
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)

        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        print("Im working")

        while self.alive:
            print("top")
            sentence, clientAddress = self.serverSocket.recvfrom(2048)
            print("bottom")
            print(sentence.decode())

            print("META")
        print("I dont feel good Mr Stark...")

    def send(self):
        othersName = input("\nGive me your bruhh's IP: ")
        othersPort = int(input("\nGive me the port: "))
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        message = input("Input lowercase sentence:")
        clientSocket.sendto(message, (othersName, othersPort))
        clientSocket.close()
