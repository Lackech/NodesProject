from socket import *
import os
import sys
import threading


class nodeTCP:

    def __init__(self, ip, port):

        self.ip = ip

        self.port = int(port)

        self.serverSocket = socket(AF_INET, SOCK_STREAM)

        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

        self.nodeMenu()

    def listen(self):

        self.serverSocket.bind(("", self.port))
        self.serverSocket.listen(1)
        print("The server is listening and ready to receive\n\n")
        while self.alive:
            connectionSocket, addr = self.serverSocket.accept()
            sentence = connectionSocket.recv(1024)

            threading.Thread(target=self.listenMessage, args=(connectionSocket, sentence)).start()
        print("I dont feel good Mr Stark...")

    def listenMessage(self, connectionSocket, sentence):
        pass

    def send(self):
        serverName = input("\nGive me your bro's IP: ")
        serverPort = int(input("\nGive me the port: "))
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        # posible creacion de hilo
        print("Im on the highway")
        sentence = input("Say it: ")
        clientSocket.send(sentence)

    # metodo para borrar un nodo
    def kill(self):
        pass

    def menu(self):
        os.system('cls')
        print("What you gonna do????")
        print("\t1 - Say something to some bruhh")
        print("\t2 - Kill myself")
        print("\t3 - Just give a sh#$t and go away")

    def nodeMenu(self):
        while self.alive:
            self.menu()
            opcionMenu = int(input("Pick a number: "))

            if opcionMenu == 1:

                self.send()
                print("")
                input("Sending a message...\nPress any key to continue")

            elif opcionMenu == 2:
                self.kill()
                self.alive = False
                print("")
                input("Shit, dying was forever...\nPress any key to continue")

            elif opcionMenu == 3:
                sys.exit()
                self.alive = False
                break

            else:
                print("")
                input("Its not that hard, just pick the right number\nPress any key to continue")
