from nodes.Node import Node
from socket import *
import os
import sys
import threading


class nodeTCP(Node):

    def __init__(self, serverIp, serverPort):
        Node.__init__(self, serverIp, serverPort)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)

        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(1)
        print("The server is listening and ready to receive\n\n")
        while self.alive:
            connectionSocket, addr = self.serverSocket.accept()
            sentence = connectionSocket.recv(1024)
            print(sentence.decode())
            threading.Thread(target=self.listenMessage, args=(connectionSocket, sentence)).start()
        print("I dont feel good Mr Stark...")

    # escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket, sentence):
        while 1:
            sentence = connectionSocket.recv(1024)
            print(sentence)

    def send(self):
        serverName = input("\nGive me your bruhh's IP: ")
        serverPort = int(input("\nGive me the port: "))
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        # posible creacion de hilo
        print("Im on the highway")
        sentence = input("Say it: ")
        clientSocket.send(sentence.encode('utf-8'))
        modifiedSentence = clientSocket.recv(1024)
        print("From Server:"), modifiedSentence