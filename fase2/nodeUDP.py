import threading
from fase2.dispatcher import *

class NodeUdp:

    # constructor del nodo
    def __init__(self, ip, port):
        #Guardamos la dirección del nodo
        self.ip = ip
        self.port = port

        #Creamos el servidor que se va a encargar de recibir todos los mensajes, que vengan de otro nodo
        self.serverSocket = Dispatcher()

        # Mapa que contiene toda la informaión de los sockets con los que actualmente está conectado
        self.socketMapping = {}

        #Creamos la bitacora donde se va a guardar cualquier movimiento importante que hace el nodo
        self.binnacle = []

        #Decimos que el nodo está vivo, y ya podrá contestar como escuchar  mensajes
        self.alive = True

        #Creamos el thread
        self.listener = threading.Thread(name='daemon',target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()



    def listen(self):
        # Asociamos el socket a nuestro Ip y Puerto
        self.serverSocket.bind(self.ip,self.port)

        # Ponemos el socket a escuchar paquetes
        self.serverSocket.listen()

        while self.alive:
            try:
                connectionSocket,otherAddress = self.serverSocket.accept()

                # Creamos el thread
                socketThread = threading.Thread(name='daemon', target=self.listenMessage, args=(connectionSocket, otherAddress))
                socketThread.setDaemon(True)
                socketThread.start()
                # Agregar info a bitácora
            except:
                # Agregar info a bitácora
                # No se logró finalizar la conexión
                pass

        self.serverSocket.close()



    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket, clientAddress):
        while self.alive:
            try:
                # Aquí esperamos que al socket le lleguen todos los paquetes del mensaje y lo recibimos
                packetMessage = connectionSocket.recv(MAXPACKETSIZE)

                # Agregar info a bitacora
            except:
                break



    # Método con el que se empieza la conexión con otro nodo
    def startConnection(self,otherIp,otherPort):
        success = True

        clientSocket = Dispatcher()
        otherAddress = (otherIp,otherPort)
        try:
            clientSocket.connect(otherIp,otherPort)
            self.socketMapping[otherAddress] = clientSocket
            #Agregar info a bitácora
        except:
            success = False
            #Agregar info a bitácora

        return success



    #Método que cierra la conexion con el nodo seleccionado
    def closeConnection(self):
        return 0



    #Método que cierra todas las conexiones
    def closeAllConnection(self):
        return 0


    # Metodo que envia mensajes a otra conexion
    def send(self,otherAddress,message):
        # Obtiene la conexión ya existente con el otro nodo
        clientSocket = self.socketMapping[otherAddress]

        # Envía el mensaje por medio del socket
        clientSocket.send(message)



    # Método que retorn un string con la lista de conexiones vivas
    def getConnectionList(self):
        stringList = ""
        num = 1

        for connection in self.connectionList:
            stringList += "\t" + num + ". (" + connection[0] + "," + connection[1] + ")\n"
            ++num

        return stringList



    # Metodo que retorna el numero de conexiones que hay abiertas en ese momento
    def numOpenConnections(self):
        return len(self.connectionList)