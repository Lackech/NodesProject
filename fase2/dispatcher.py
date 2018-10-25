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

        # Creacion del socket UDP para usarlo para mandar mensajes
        self.socketUtil = socket(AF_INET, SOCK_DGRAM)

        # Diccionario de conexiones aceptadas en el handshake
        self.acceptedConnections = {}

        # Clase que se encarga de codificar y decodificar información
        self.bitnator = Bitnator()

        #Buzón donde se guardan los mensajes que se reciben
        self.mailbox = []

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

        # Llama al método que desencripta un mensaje
        decryptedMessage = self.bitnator.decrypt(packetMessage)

        # Si la dirección que viene en el mensaje es correcta, además de que el ACK y SYN están en 0, quiere decir que la conexión sí puede iniciar
        if decryptedMessage[IPDESTINO] == self.ipDispatcher and decryptedMessage[PUERTODESTINO] == self.portDispatcher:
            if decryptedMessage[SYN] == 1 and decryptedMessage[ACK] == 1:
                self.processHandshake(decryptedMessage)
            else:
                self.debugPacket(decryptedMessage)
        else:
            # El paquete es ignorado
            pass





    # El cliente crea la conexion con la info del destino
    def connect(self, ipAddress, port):


        pass

    # Acepta la conexion, en otras palabras el handshaking
    def accept(self,decryptedMessage):

            # Encriptamos el mensaje donde se devuelve un ACK al cliente
            acceptingMessage = self.bitnator.encrypt(
                origenIp=self.ipDispatcher,
                origenPort=self.portDispatcher,
                destinationIp=decryptedMessage[IPORIGEN],
                destinationPort=decryptedMessage[PUERTOORIGEN],
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
            acceptingSocket.sendto(acceptingMessage, (decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN]))
            acceptingSocket.close()

            # Creamos un socket que se toma como un posible socket de conexión, en caso de que el handshake se efectue correctamente
            posibleSocket = Dispatcher()
            data = {(decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN]),posibleSocket}
            self.posibleConnections.update(data)

            # Esperamos una respuesta del cliente
            while len(posibleSocket.mailbox) == 0:
                pass
            finalAnswer = posibleSocket.mailbox.pop()


            # Si el cliente responde correctamente devolvemos el socet ya con toda la información para trabajar, si sale mal descartamos la conexión
            if finalAnswer[SYN] == 1 and finalAnswer[ACK] == 1 and finalAnswer[IPDESTINO] == self.ipDispatcher and finalAnswer[PUERTODESTINO] == self.portDispatcher:
                # Sacamos del diccionario de posibles conexiones el socket, pues ya es una conexión establecida
                self.posibleConnections.pop((decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN]))

                # Retornamos los datos necesarios para que el nodo pueda trabajar
                return posibleSocket,(finalAnswer[IPORIGEN], finalAnswer[PUERTOORIGEN])

            else:
                # Sacamos del diccionario de posibles conexiones el socket, pues la conexión no se pudo establecer correctamente
                self.posibleConnections.pop((decryptedMessage[IPORIGEN], decryptedMessage[PUERTOORIGEN]))

        # Quiere decir que el mensaje recibido no fue el correcto, por lo que no hace nada
        else:
            pass



    # Se recibe el mensaje completo en el nodo, por lo que se revisa por paquete
    def recv(self):
        #Se queda esperando hasta que en la lista haya un mensaje que devolver
        while len(self.mailbox) == 0:
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
