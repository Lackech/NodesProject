from socket import *
from threading import *
import threading

class dispatcher:

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
    def __init__(self,IP,Port):
        # Direccion IP y puerto del nodo que crea el socket
        self.ipDispatcher = IP
        self.portDispatcher = Port
        # Direccion IP y puerto del otro extremo del socket
        self.ipDestination = ""
        self.portDestination = ""
        # Variables necesarias para manejar paquetes e hilos
        self.SN = 0
        self.RN = 0
        self.lock = threading.Lock()
        # Creacion del socket UDP para usarlo para mandar mensajes
        self.socketUtil = socket(AF_INET, SOCK_DGRAM)
        # Diccionario de conexiones aceptadas en el handshake
        self.acceptedConnections = {}

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

            # Debo analizar el paquete y si el SYN Flag esta encendido, debo procesar handshake
            # Puede ser que sea solo el SYN o con el ACK para aceptar la conexion
            # Si no tiene el SYN Flag encendido, puede ser un mensaje de datos o de fin de comunicacion


    # El cliente crea la conexion con la info del destino
    def connect(self):
        pass

    # Se recibe el mensaje completo en el nodo, por lo que se revisa por paquete
    def recv(self):
        pass

    # Se envia el mensaje, se envia por paquetes por lo que se analiza su encabezado para ver su comportamiento
    def send(self):
        pass

    # Cierra la conexion despues del envio, por lo que se cierra en dos pasos(msj - ack)
    def close(self):
        pass

    # Acepta la conexion, en otras palabras el handshaking
    def accept(self):
        pass

    # Analiza el paquete, revisando el RN y SN y tomando la accion adecuada.
    def debugPacket(self,packetMessage):
        pass

    # Una vez que se detecto el SYN Flag encendio en el paquete se pasa a este metodo para procesarlo
    # El paquete puede ser solo el SYN o el SYN y el ACK.
    def processHandshake(self,packetMessage):
        pass
