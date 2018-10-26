import queue
from socket import *
from threading import *
from fase2.bitnator import *
import threading
import queue

# Variables para identificar estado actual del socket
LISTENING = 0
CONNECTING = 1
ESTABLISHED = 2

# Timeouts
TIMEOUT_CONNECT = 3


# Variables para identificar las partes de un paquete
IPORIGEN = 0
PUERTOORIGEN = 1
IPDESTINO = 2
PUERTODESTINO = 3
SYN = 4
RN = 5
SN = 6
ACK = 7
FIN = 8
RELLENO = 9
MENSAJE = 10

MAXPACKETSIZE = 2048
MAXQUEUEZISE = 0

class Dispatcher:

    # Diseño del paquete:
    #################################################################################################################
    #           #               #            #                #       #    #    #     #     #         #           ##
    # IP Origen # Puerto Origen # IP Destino # Puerto Destino #  SYN  # RN # SN # ACK # FIN # Relleno #  Mensaje  ##
    #           #               #            #                #       #    #    #     #     #         #           ##
    ################################################################################################################
    #           #               #            #                #       #    #    #     #     #         #           ##
    # 4 Bytes   #   2 Bytes     #  4 Bytes   #    2 Bytes     #  bit  # bit# bit# bit # bit # 3 bits  #  1 byte   ##
    #           #               #            #                #       #    #    #     #     #         #           ##
    ################################################################################################################
    def __init__(self):
        # Direccion IP y puerto del nodo que crea el socket

        self.ipDispatcher = ""
        self.portDispatcher = 0

        # Direccion IP y puerto del otro extremo del socket
        self.ipDestination = ""
        self.portDestination = 0

        # Variables necesarias para manejar paquetes e hilos
        self.SN = 0
        self.RN = 0
        self.lock = threading.Lock()

        # Lista d que contiene los Keys con los que se puede identificar el posible socket con el que se esta realizando la conexión
        self.keys = []

        # Creacion del socket UDP para usarlo para mandar mensajes
        self.socketUtil = socket(AF_INET, SOCK_DGRAM)

        # Diccionario de conexiones aceptadas en el handshake
        self.acceptedConnections = {}

        # Clase que se encarga de codificar y decodificar información
        self.bitnator = Bitnator()

        #Buzón donde se guardan los mensajes que se reciben
        self.mailbox = queue.Queue(MAXQUEUEZISE);

        #Buzon para los mensajes del handshake
        self.connMailbox = queue.Queue(MAXQUEUEZISE)

        # Diccionario que contiene los sockets de las posibles conexiones
        self.posibleConnections = queue.Queue(MAXQUEUEZISE)

        # Mapeo de conexiones
        self.connections ={}

        self.data = bytearray()



    def bind(self,ip,port):
        self.ipDispatcher = ip
        self.portDispatcher = port

    # El dispatcher se quedara escuchando por mensajes nuevos mediante un thread
    def listen(self):
        listenMessageThread = Thread(target=self.listenMessage)
        listenMessageThread.setDaemon(True)
        listenMessageThread.start()

    # Inicia escucha de mensajes, revisa que empiece el handshake
    def listenMessage(self):
        while True:
            # Es distinto cuando escucha un nodo creado a cuando un cliente se conecta y queda escuchando
            # por una respuesta por lo que se debe manejar eso por aqui

            # Recibo el paquete mediante el socket UDP
            packetMessage, clientAddress = self.socketUtil.recvfrom(MAXPACKETSIZE)

            # Crea un hilo que se encarga de desencriptar el mensaje
            messageDecryptorThread = Thread(target=self.decryptPacket, args=(packetMessage))
            messageDecryptorThread.setDaemon(True)
            messageDecryptorThread.start()

            # Debo analizar el paquete y si el SYN Flag esta encendido, debo procesar handshake
            # Puede ser que sea solo el SYN o con el ACK para aceptar la conexion
            # Si no tiene el SYN Flag encendido, puede ser un mensaje de datos o de fin de comunicacion



    def decryptPacket(self,packetMessage):

        # Llama al método que desencripta un mensaje
        decryptedMessage = self.bitnator.decrypt(packetMessage)

        # Si la dirección que viene en el mensaje es correcta, además de que el ACK y SYN están en 0, quiere decir que la conexión sí puede iniciar
        if decryptedMessage[IPDESTINO] == self.ipDispatcher and decryptedMessage[PUERTODESTINO] == self.portDispatcher:
            if decryptedMessage[SYN] == 1 and decryptedMessage[ACK] == 0 and decryptedMessage[FIN] == 0:
                self.processHandshake(decryptedMessage, self.ipDispatcher,self.portDispatcher,self.socketUtil)
            else:
                existingConn = self.connections[(decryptedMessage[IPORIGEN],decryptedMessage[PUERTOORIGEN])]
                existingConn.debugPacket(decryptedMessage)
        else:
            # El paquete es ignorado
            pass





    # El cliente crea la conexion con la info del destino
    def connect(self, ipAddress, port):
        self.ipDestination = ipAddress
        self.portDestination = port
        self.SN = 1


        mensaje = []

        # Creacion del socket UDP para usarlo para mandar mensajes
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        packetToSend = self.bitnator.encrypt(self.ipDispatcher, self.portDispatcher, self.ipDestination,
                                                self.portDestination, 1, self.RN, self.SN,
                                                1, 1, mensaje)

        clientSocket.sendto()
        clientSocket.sendto(packetToSend, (self.ipDestination, self.portDestination))












    # Acepta la conexion, en otras palabras el handshaking
    def accept(self):
        # Esperamos a que en la lista con los que de las posibles conexiones haya al menos una Key
        while len(self.keys) == 0:
            pass

        # Optenemos el primer key que hay en la lista
        key = self.keys.pop()
        # Obtenemos el socket asociado a ese key
        posibleSocket = self.posibleConnections.pop(key)

        # Encriptamos el mensaje donde se devuelve un ACK al cliente
        acceptingMessage = self.bitnator.encrypt(
            origenIp=self.ipDispatcher,
            origenPort=self.portDispatcher,
            destinationIp=key[0],
            destinationPort=key[1],
            syn=0,
            rn=0,
            sn=0,
            ack=1,
            fin=0,
            message=""
        )

        # Creacion del socket UDP por e que se va a enviar el mensaje de aceptación
        acceptingSocket = socket(AF_INET, SOCK_DGRAM)
        # Enviamos el mensaje de aceptación
        acceptingSocket.sendto(acceptingMessage, (key[0], key[1]))
        #Cerramos la conexión del socket UDP
        acceptingSocket.close()

        try:
            # Esperamos que nos llegue un mesnaje
            posibleSocket.mailbox.get()

            # Agregar informacion a la bitácora

            return posibleSocket,key
        except:
            # Agregar informacion a la bitácora
            pass




    # Se recibe el mensaje completo en el nodo, por lo que se revisa por paquete
    def recv(self):
        #Se queda esperando hasta que en la lista haya un mensaje que devolver
        while len(self.mailbox) == 0:
            pass

        return self.mailbox.pop()



    # Se envia el mensaje, se envia por paquetes por lo que se analiza su encabezado para ver su comportamiento
    def send(self,message):

        pass

    # Cierra la conexion despues del envio, por lo que se cierra en dos pasos(msj - ack)
    def close(self):
        pass



    # Analiza el paquete, revisando el RN y SN y tomando la accion adecuada.
    def debugPacket(self,packetMessage):
        if packetMessage[SYN] == 1 and packetMessage[FIN] == 0:
            msgResponse = self.bitnator.encrypt(self.ipDispatcher, self.portDispatcher, self.ipDestination,
                                                self.portDestination, 1, self.RN, self.SN,
                                                1, 1, 0)
            # Envia el mensaje para terminar e=con el handshake del lado del cliente
            self.socketUtil.sendto(msgResponse, (self.ipDestination, self.portDestination))

        elif packetMessage[SYN] == 1 and packetMessage[FIN] == 1:
            # Esto en el lado del server libera la cola y continua el accept
            self.connMailbox.put_nowait(packetMessage)

        # Es mensaje de datos
        elif packetMessage[SN] == self.SN:
            self.RN = (self.RN + 1) % 2
            # Envio el ACK y reviso si es mensaje final o no
            if packetMessage[FIN] == 1:
                #Envir mensaje de fin y parar el analizar mensaje
                msgResponse = self.bitnator.encrypt(self.ipDispatcher, self.portDispatcher, self.ipDestination,
                                                    self.portDestination, 0, self.RN, self.SN,
                                                    1, 1, 0)
                self.socketUtil.sendto(msgResponse, (self.ipDestination, self.portDestination))
            else:
                self.mailbox.put_nowait(packetMessage)
                self.data += packetMessage[MENSAJE]
                msgResponse = self.bitnator.encrypt(self.ipDispatcher, self.portDispatcher, self.ipDestination,
                                                    self.portDestination, 0, self.RN, self.SN,
                                                    1, 0, 0)
                self.socketUtil.sendto(msgResponse, (self.ipDestination, self.portDestination))
        else:
            # Recibo el ACK y actualizo el SN
            self.SN = packetMessage[RN]







    # Una vez que se detecto el SYN Flag encendio en el paquete se pasa a este metodo para procesarlo
    # El paquete puede ser solo el SYN o el SYN y el ACK.
    def processHandshake(self,decryptedMessage,myIp,myPort,mySocket):

        socketConexion = Dispatcher()
        socketConexion.ipDispatcher = myIp
        socketConexion.portDispatcher = myPort
        socketConexion.ipDestination = decryptedMessage[IPORIGEN]
        socketConexion.portDestination = decryptedMessage[PUERTOORIGEN]
        socketConexion.socketUtil = mySocket
        socketConexion.RN = (decryptedMessage[RN] + 1) % 2
        socketConexion.SN = 0
        # Comienzo handshake en el nodo server

        # Añado esta conexión al mapa de conexiones del nodo
        self.connections[(socketConexion.IPDestino, socketConexion.puertoDestino)] = socketConexion

        #Agregamos a la cola para iniciar el accept
        self.posibleConnections.put_nowait(socketConexion)

        # Respondo al nodo que esta esperando en connect
        msgResponse = self.bitnator.encrypt(self.ipDispatcher,self.portDispatcher,socketConexion.ipDestination,
                                            socketConexion.portDestination,1,socketConexion.RN,socketConexion.SN,
                                            1,0,0)

        self.socketUtil.sendto(msgResponse,(socketConexion.ipDestination,socketConexion.portDestination))



