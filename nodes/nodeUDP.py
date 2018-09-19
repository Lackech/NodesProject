from socket import *
import threading
import os
import sys


class nodeUDP:

    # constructor del nodo
    def __init__(self, ip, port):
        self.ip = ip

        self.port = int(port)

        self.serverSocket = socket(AF_INET, SOCK_STREAM)

        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        self.alive = True

        self.nodeMenu()

    def listen(self):
        serverPort = int(self.port)
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(("", serverPort))
        print("Im working")

        while self.alive:
            print("top")
            sentence, clientAddress = serverSocket.recvfrom(2048)
            print("bottom")
            print(sentence.decode())

            print("META")
        print("I dont feel good Mr Stark...")

    def send(self):
        serverName = input("\nGive me your bruhh's IP: ")
        serverPort = int(input("\nGive me the port: "))
        clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = input("Input lowercase sentence:")
        clientSocket.sendto(message, (serverName, serverPort))
        clientSocket.close()



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

    # metodo para borrar un nodo
    def kill(self):
        pass
