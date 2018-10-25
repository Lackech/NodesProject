from socket import *
from threading import *
from fase2.bitnator import *
import threading

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

        # Creacion del socket UDP para usarlo para mandar mensajes
        self.socketUtil = socket(AF_INET, SOCK_DGRAM)

        # Diccionario de conexiones aceptadas en el handshake
        self.acceptedConnections = {}

        # Clase que se encarga de codificar y decodificar información
        self.bitnator = Bitnator()

        #Buzón donde se guardan los mensajes que se reciben
        self.mailbox = []



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
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

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
        #Guarda ese mensaje en la lista que tiene todos los mensajes que le llegan
        self.mailbox.append(decryptedMessage)



    # El cliente crea la conexion con la info del destino
    def connect(self, ipAddress, port):
        pass

    # Acepta la conexion, en otras palabras el handshaking
    def accept(self,decryptedMessage):
        #Si el SYN y ACK tienen el valor 0, quiere decir que se quiere comenzar a realizar una comunicación
        if decryptedMessage[SYN] == 0 and decryptedMessage[ACK] == 0:
            #Encriptamos el mensaje que accepta una conexión
            acceptingMessage = self.bitnator.encryptAcceptMessage()

            # Creacion del socket UDP por e que se va a enviar el mensaje de aceptación
            acceptingSocket = socket(AF_INET, SOCK_DGRAM)
            #Enviamos el mensaje de aceptación
            acceptingSocket.sendto(acceptingMessage,(decryptedMessage[IPORIGEN],decryptedMessage[PUERTOORIGEN]))

        # Quiere decir que el mensaje recibido no fue el correcto, por lo que le responde con un NACK
        else:



    # Se recibe el mensaje completo en el nodo, por lo que se revisa por paquete
    def recv(self):
        #Se queda esperando hasta que en la lista haya un mensaje que devolver
        while len(self.mailbox) is 0:
            pass

        return self.mailbox.pop()



    # Se envia el mensaje, se envia por paquetes por lo que se analiza su encabezado para ver su comportamiento
    def send(self):
        pass

    # Cierra la conexion despues del envio, por lo que se cierra en dos pasos(msj - ack)
    def close(self):
        pass



    # Analiza el paquete, revisando el RN y SN y tomando la accion adecuada.
    def debugPacket(self,packetMessage):
        pass

    # Una vez que se detecto el SYN Flag encendio en el paquete se pasa a este metodo para procesarlo
    # El paquete puede ser solo el SYN o el SYN y el ACK.
    def processHandshake(self,packetMessage):
        pass
