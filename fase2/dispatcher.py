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
        pass

    # Inicia escucha de mensajes, revisa que empiece el handshake
    def listenMessage(self):
        pass

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



