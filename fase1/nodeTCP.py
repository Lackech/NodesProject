from fase1.node import *
from socket import *
import threading



class NodeTcp(Node):

    def __init__(self, serverAddress):
        Node.__init__(self, serverAddress)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)

        self.alive = True

        self.listener = threading.Thread(name='daemon',target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()



    def listen(self):
        self.serverSocket.bind(self.serverAddress)
        self.serverSocket.listen(1)

        while self.alive:
            connectionSocket, addr = self.serverSocket.accept()
            self.currentConnection[addr] = connectionSocket

            t = threading.Thread(name='daemon',target=self.listenMessage, args=(connectionSocket, addr))
            t.setDaemon(True)
            t.start()

        self.serverSocket.close()



    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket, clientAddress):
        while self.alive:
            try:
                #Optiene la información, sí es que la hay
                packetMessage = connectionSocket.recv(1024)
                if packetMessage:
                    #Preguntamos el tamaño del mensaje
                    if len(packetMessage) is 1:
                        #Si es de tamaño 8 quiere decir que el address que envio el mensaje murió
                        self.closingConnection(TCP,clientAddress)
                        break
                    else:
                        #Decodifica la información
                        self.encryptor.bitDecrypt(packetMessage,clientAddress)

                        #Da una respuesta al cliente

            except:
                self.closingConnection(connectionSocket, clientAddress)
                break



    def send(self,otherAddress,messageList):
        #Verifica si existe una conexión, de no ser así la crea y la guarda
        successful = True
        if otherAddress in self.currentConnection:
            clientSocket = self.currentConnection[otherAddress]
            clientSocket.send(self.encryptor.bitEncript(messageList))
        else:

            try:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect(otherAddress)
                self.currentConnection[otherAddress] = clientSocket

                #Creamos un hilo para escuchar lo que responda la conexión.
                t = threading.Thread(name='daemon',target=self.listenMessage, args=(clientSocket, otherAddress))
                t.setDaemon(True)
                t.start()

                clientSocket.send(self.encryptor.bitEncript(messageList))

            except:
                clientSocket.close()
                successful = False

        #Envía un mensaje codificado
        return successful




    #Método para borrar un nodo
    def kill(self):
        # Matamos el servidor
        self.alive = False

        #Buscamos los sockets que se han creado y les enviamos un mensaje de que está muriendo
        #además se cierran los respectivos sockets
        for address in self.currentConnection:
            clientSocket = self.currentConnection[address]
            clientSocket.send(b'\x00')
            clientSocket.close()
