import queue
from socket import *
from threading import *
from fase2.bitnator import *
import threading

# Variables para identificar estado actual del socket
LISTENING = 0
CONNECTING = 1
ESTABLISHED = 2

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
        self.mailbox = queue.Queue()

        # Diccionario que contiene los sockets de las posibles conexiones
        self.posibleConnections = {}



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
            packetMessage, clientAddress = self.serverSocket.recvfrom(MAXPACKETSIZE)

            # Crea un hilo que se encarga de desencriptar el mensaje
            messageDecryptorThread = Thread(target=self.decryptPacket, args=(packetMessage))
            messageDecryptorThread.setDaemon(True)
            messageDecryptorThread.start()

            # Debo analizar el paquete y si el SYN Flag esta encendido, debo procesar handshake
            # Puede ser que sea solo el SYN o con el ACK para aceptar la conexion
            # Si no tiene el SYN Flag encendido, puede ser un mensaje de datos o de fin de comunicacion



    def decryptPacket(self,packetMessage):
        #Llama al método que desencripta un mensaje
        decryptedMessage = self.bitnator.decryptPacket(packetMessage)

        #Preguntamos sí el mensaje es la respuesta del cliente al ACK del servidor
        if self.posibleConnections.get((decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN])) is not None:
            posibleSocket = self.posibleConnections.get((decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN]))
            posibleSocket.mailbox.append(decryptedMessage)
        else:
            #Guarda ese mensaje en la lista que tiene todos los mensajes que le llegan, pues el nodo se encarga de a que socket dárselo
            self.mailbox.append(decryptedMessage)



    # El cliente crea la conexion con la info del destino
    def connect(self, ipAddress, port):
        pass

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