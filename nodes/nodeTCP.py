from nodes.node import *
from socket import *
from nodes.bitnator import *
from nodes.application import *
import threading



class NodeTcp(Node):

    def __init__(self, serverAddress):
        Node.__init__(self, serverAddress)
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.encryptor = Bitnator()
        self.currentConnection = {}
        self.alive = True
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()




    def listen(self):
        self.serverSocket.bind((self.serverIp, self.serverPort))
        self.serverSocket.listen(1)
        print("The server is listening and ready to receive\n\n")
        while self.alive:
            connectionSocket, addr = self.serverSocket.accept()
            self.currentConnection[addr] = connectionSocket
            threading.Thread(target=self.listenMessage, args=(connectionSocket, addr)).start()

        self.serverSocket.close()
        print("I dont feel good Mr Stark...")

    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket, clientAddress):
        while True:
            try:
                #Optiene la información, sí es que la hay
                sentence = connectionSocket.recv(1024)
                if sentence:
                    #Preguntamos el tamaño del mensaje
                    if len(sentence) is 8:
                        #Si es de tamaño 8 quiere decir que el address que envio el mensaje murió
                        self.currentConnection.pop(clientAddress)
                        copy = self.reachabilityTable.copy()
                        for addr in copy:
                            value = self.reachabilityTable.get(addr)
                            if value[1] == clientAddress:
                                self.reachabilityTable.pop(addr)
                    else:
                        #Decodifica la información
                        #self.decrypt(sentence, clientAddress)
                        print("Ya llegue")
                        self.encryptor.bitDecrypt(sentence,clientAddress)
                        #Da una respuesta al cliente
                else:
                    raise error('Client disconnected')
            except:
                connectionSocket.close()
                return False

    def send(self,serverName,serverPort):
        #Pregunta por el puerto donde quiere enviar el mensaje
        #serverName = input("\nGive me your bruhh's IP: ")
        #serverMascara = input("\nGive me your bruhh's Mascara: ")
        #serverPort = int(input("\nGive me the port: "))
        address = (serverName, serverPort)

        #Verifica si existe una conexión, de no ser así la crea y la guarda
        if address in self.currentConnection:
            print('Connection exist')
            clientSocket = self.currentConnection[address]
        else:
            print('New connection')
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            self.currentConnection[address] = clientSocket

            #Creamos un hilo para escuchar lo que responda la conexión.
            threading.Thread(target=self.listenMessage, args=(clientSocket, address)).start()


        #Envía un mensaje codificado
        #clientSocket.send(self.encode().encode('utf-8'))
        clientSocket.send(self.encryptor.bitEncript().encode('utf-8'))




    #Método para borrar un nodo
    def kill(self):
        # Matamos el servidor
        self.alive = False

        #Buscamos los sockets que se han creado y les enviamos un mensaje de que está muriendo
        #además se cierran los respectivos sockets
        for address in self.currentConnection:
            clientSocket = self.currentConnection[address]
            clientSocket.send('00000000'.encode('utf-8'))
            clientSocket.close()
