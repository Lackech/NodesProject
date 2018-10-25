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

        #Mapa que va a tener como KEY = (otroIp, otroPuerto), VALUE = (Dispatcher*)
        self.socketMapping = {}

        #Buzon que contiene la lista de mensajes recibidos por el Dispatcher
        self.mailbox = []

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
            # Se encarga de recibir todos los paquetes que son enviados a esta dirección
            decryptedMessage = self.serverSocket.recv()
            otherAddres = (decryptedMessage[IPORIGEN],decryptedMessage[PUERTOORIGEN])

            if self.socketMapping.get(otherAddres) is not None:
                # Quiere decir que el paquete llego de una conexión ya existente

                pass
            else:
                # Quiere decir que el paquete llego de un Socket con el que es primera vez que se comunica
                try:
                    connectionSocket,otherAddress = self.serverSocket.accept(decryptedMessage)
                    data = {otherAddres,connectionSocket}
                    self.socketMapping.update(data)
                    # Agregar info a bitácora
                except:
                    # Agregar info a bitácora
                    pass

        self.serverSocket.close()



    #Método para comenzar la conexion con otro nodo
    def startConnection(self,otherIp,otherPort):
        clientSocket = Dispatcher(self.ip,self.port)
        try:
            clientSocket.connect(otherIp,otherPort)
            data = {(otherIp,otherPort),clientSocket}
            self.socketMapping.update(data)
            #Agregar info a bitácora
        except:
            #Agregar info a bitácora
            return  0



    #Método que cierra la conexion con el nodo seleccionado
    def closeConnection(self,nodeOption):
        return 0



    #Método que cierra todas las conexiones
    def closeAllConnection(self):
        return 0


    # Metodo que envia mensajes a otra conexion
    def send(self,nodeOption,message):
        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        clientSocket.sendto(self.encryptor.bitEncript(messageList),otherAddress)

        #Cerramos la conexión
        clientSocket.close()

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