from socket import *
import os
import sys
import threading


class nodeTCP:

    # constructor del nodo
    def __init__(self, ip, port):
        # ip del nodo creado
        self.ip = ip
        # puerto habilitado del nodo
        self.port = port
        # bool para controlar la escucha de un nodo
        self.alive = True
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(("", self.port))
        # hilo para mantener el nodo escuchando
        listener_thread = threading.Thread(target=self.listen())
        listener_thread.start()
        # menu de nodo
        self.nodeMenu()

    # metodo para escuchar mensajes
    def listen(self):

        self.serverSocket.listen(5)
        print("The server is ready to receive")
        while True:
            print("Por aqui")
            # Aceptar conexiones
            connectionSocket, addr = self.serverSocket.accept()
            print("Por aca")
            # sentence guarda lo que recibio
            sentence = connectionSocket.recv(1024)
            if sentence == '':
                break
            threading.Thread(target=self.listen_message(), args=(connectionSocket, sentence)).start()
        print("I dont feel good Mr Stark...")

    # metodo para escuchar simultaneamente
    def listenMessage(self,connectionSocket,sentence):
        size = 1024
        while True:
            try:
                data = connectionSocket.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    connectionSocket.send(response)
                else:
                    raise error('Client disconnected')
            except:
                connectionSocket.close()
                return False

    # metodo que envia un mensaje
    def send(self, serverName, serverPort):
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
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
        print("\t9 - Just give a sh#$t and go away")

    def nodeMenu(self):
        while self.alive:
            self.menu()
            opcionMenu = input("Pick a number: ")

            if opcionMenu == "1":
                serverName = input("\nGive me your bro's IP: ")
                serverPort = int(input("\nGive me the port: "))
                self.send(serverName,serverPort)
                print("")
                input("Sending a message...\nPress any key to continue")

            elif opcionMenu == "2":
                self.kill()
                self.alive = False
                print("")
                input("Shit, dying was forever...\nPress any key to continue")

            elif opcionMenu == "9":
                sys.exit()

            else:
                print("")
                input("Its not that hard, just pick the right number\nPress any key to continue")
