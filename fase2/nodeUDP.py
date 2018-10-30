import threading
from fase2.dispatcher import *

class NodeUdp:

    # constructor del nodo
    def __init__(self, ip, port):
        #Guardamos la dirección del nodo
        self.ip = ip
        self.port = port

        # Candado para la bitacora
        self.lock = threading.Lock()
        #Creamos el servidor que se va a encargar de recibir todos los mensajes, que vengan de otro nodo
        self.serverSocket = Socket()

        # Mapa que contiene toda la informaión de los sockets con los que actualmente está conectado
        self.socketMapping = {}

        #Creamos la bitacora donde se va a guardar cualquier movimiento importante que hace el nodo
        self.binnacle = []

        #Decimos que el nodo está vivo, y ya podrá contestar como escuchar  mensajes
        self.alive = True

        #Creamos el thread
        self.listener = threading.Thread(name='server',target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()



    def listen(self):
        # Asociamos el socket a nuestro Ip y Puerto
        self.serverSocket.bind(self.ip,self.port)

        # Ponemos el socket a escuchar paquetes
        self.serverSocket.listen()

        while self.alive:
            try:
                connectionSocket = self.serverSocket.accept()

                # Creamos el thread
                socketThread = threading.Thread(name='reciver', target=self.listenMessage, args=[connectionSocket])
                socketThread.setDaemon(True)
                socketThread.start()
                # Agregar info a bitácora
            except:
                # Agregar info a bitácora
                # No se logró finalizar la conexión
                pass

        self.serverSocket.close()



    # Escucha cada conexion para procesar el mensaje
    def listenMessage(self, connectionSocket):
        while self.alive:
            try:
                # Aquí esperamos que al socket le lleguen todos los paquetes del mensaje y lo recibimos
                message = connectionSocket.recv()
                print(message)

                # Agregar info a bitacora
            except:
                break



    # Método con el que se empieza la conexión con otro nodo
    def startConnection(self,otherIp,otherPort):
        success = True
        if otherIp == 'localhost':
            otherIp = '127.0.0.1'

        clientSocket = Socket()
        clientSocket.bind(self.ip,self.port)
        otherAddress = (otherIp,otherPort)
        try:
            # Lo agregamos al mapa de posibles conexiones que contiene el servidor
            self.serverSocket.posibleConnections[otherAddress] = clientSocket
            # Iniciamos la conexión
            clientSocket.connect(otherIp,otherPort)
            # Si se logró correctamente lo agregamos al mapa de conexiones establecidas y lo eliminamos de las posibles conexiones
            self.serverSocket.posibleConnections.pop(otherAddress)
            self.serverSocket.acceptedConnections[otherAddress] = clientSocket

            # Creamos el thread
            socketThread = threading.Thread(name='reciver', target=self.listenMessage, args=[clientSocket])
            socketThread.setDaemon(True)
            socketThread.start()

            #Agregar info a bitácora
        except:
            success = False
            #Agregar info a bitácora

        return success





    #Método que cierra la conexion con el nodo seleccionado
    def closeConnection(self,otherAddress):
        clientSocket = self.serverSocket.acceptedConnections[otherAddress]
        clientSocket.close()





    # Metodo que envia mensajes a otra conexion
    def send(self,otherAddress,message):
        # Obtiene la conexión ya existente con el otro nodo
        if self.serverSocket.acceptedConnections.get(otherAddress) is not None:
            clientSocket = self.serverSocket.acceptedConnections[otherAddress]
            # Envía el mensaje por medio del socket
            clientSocket.send(message)
        else:
            if self.startConnection(otherAddress[0],otherAddress[1]) is True:
                clientSocket = self.serverSocket.acceptedConnections[otherAddress]
                # Envía el mensaje por medio del socket
                clientSocket.send(message)
            else:
                # No se logro enviar el mensaje
                pass






    # Método que retorn un string con la lista de conexiones vivas
    def getConnectionList(self):
        stringList = ""
        num = 1

        for connection in self.serverSocket.acceptedConnections:
            stringList += "\t" + str(num) + ". (" + connection[0] + "," + str(connection[1]) + ")\n"
            num = num + 1

        return stringList



    def getSelectedAddress(self,num):
        i = 1
        address = None
        for connection in self.serverSocket.acceptedConnections:
            if i == num:
                address = connection
                break
            else:
                i = i + 1

        return address



    # Metodo que retorna el numero de conexiones que hay abiertas en ese momento
    def numOpenConnections(self):
        return len(self.serverSocket.acceptedConnections)
