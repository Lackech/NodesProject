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
MAXQUEUEZISE = 5

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

    # Banderas activadas para cada caso
    # Mensaje de inicio de conexion que envia el connect (cliente): ||SYN = 1, ACK = 0, FIN = 0||
    # Mensaje de respuesta al inicio de conexion que envia el accept (servidor): ||SYN = 1, ACK = 1, FIN = 0||
    # Mensaje de respuesta que hace el cliente a la respuesta de conexion que envía el servidor : ||SYN = 1, ACK = 1, FIN = 1||
    # Mensaje que contiene datos: ||SYN = 0, ACK = 0, FIN|| = 0 ó ||SYN = 0, ACK = 0, FIN = 1|| (en caso de que sea el final del mensaje)
    # Mensaje que contiene el ack a los datos que recibió: ||SYN = 0, ACK = 1, FIN = 0||
    # Mensaje para finalizar la conexión: ||SYN = 1, ACK = 0, FIN = 1||


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
        # Diccionario que contiene los sockets de las posibles conexiones
        self.posibleConnections = {}

        # Diccionario de conexiones aceptadas en el handshake
        self.acceptedConnections = {}

        # Creación del socet UDP que va a funcionar como servidor
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)

        # Creacion del socket UDP para usarlo para mandar mensajes
        self.socketUtil = socket(AF_INET, SOCK_DGRAM)

        # Clase que se encarga de codificar y decodificar información
        self.bitnator = Bitnator()

        #Buzón donde se guardan los mensajes que se reciben
        self.messageMailbox = queue.Queue(MAXQUEUEZISE);
        self.ackMailbox = queue.Queue(MAXQUEUEZISE);

        #Buzon para los mensajes del handshake
        self.connMailbox = queue.Queue(MAXQUEUEZISE)



        # Mapeo de conexiones
        self.connections ={}

        self.data = bytearray()



    def bind(self,ip,port):
        self.ipDispatcher = ip
        self.portDispatcher = port

    # El dispatcher se quedara escuchando por mensajes nuevos mediante un thread
    def listen(self):
        self.serverSocket.bind((self.ipDispatcher,self.portDispatcher))
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
            if decryptedMessage[SYN] == 1 and decryptedMessage[ACK] == 0 and decryptedMessage[FIN] == 0:
                # Entramos en el caso donde el paquete recibido es de tipo inicio de conexión
                self.processHandshake(decryptedMessage, self.ipDispatcher,self.portDispatcher,self.socketUtil)

            elif packetMessage[SYN] == 1 and packetMessage[ACK] == 0 and packetMessage[FIN] == 1:
            # Entramos en el caso donde el paquete recibido es de tipo cierre de conexión
                # Lo agregamos a la cola que guarda paquete de conexión
                self.connMailbox.put_nowait(packetMessage)

            else:
                otherAddress = (decryptedMessage[IPORIGEN],decryptedMessage[PUERTOORIGEN])
                # Verificamos que si haya un socket que está en proceso de finalizar la conexión
                if self.posibleConnections.get(otherAddress) is not None:
                    # Obtenemos la socket específico y le agregamos a la cola de mensajes de conexión el mensaje, para que lo procese
                    posibleConnection = self.posibleConnections[otherAddress]
                    posibleConnection.debugPacket(decryptedMessage)
                else:
                    existingConn = self.acceptedConnections[otherAddress]
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
                                                0, 0, mensaje)

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
            syn=1,
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
            # Esperamos que nos llegue un mensaje
            posibleSocket.connMailbox.get()

            # Agregar informacion a la bitácora

            return posibleSocket,key
        except:
            # Agregar informacion a la bitácora
            pass




    # Se recibe el mensaje completo en el nodo, por lo que se revisa por paquete
    def recv(self):
        message = ""
        completed = False

        while completed:
            # Esperamos a que nos llegue un paquete
            packetMessage = self.messageMailbox.get()
            message += packetMessage[MENSAJE]

            if packetMessage[FIN] == 1:
                completed = True

            # Cuando nos llega un mensaje revisamos si el rn y el sn están correctos
            if self.RN == packetMessage[SN]:
                self.RN = (self.RN + 1) % 2

            ackMessage = self.bitnator.encrypt(
                origenIp=self.ipDispatcher,
                origenPort=self.portDispatcher,
                destinationIp=packetMessage[IPORIGEN],
                destinationPort=packetMessage[PUERTOORIGEN],
                syn=0,
                rn=self.RN,
                sn=0,
                ack=1,
                fin=0,
                message=""
            )

            # Creacion del socket UDP por e que se va a enviar el mensaje de aceptación
            ackSocket = socket(AF_INET, SOCK_DGRAM)
            # Enviamos el mensaje de aceptación
            ackSocket.sendto(ackMessage, (packetMessage[IPORIGEN],packetMessage[PUERTOORIGEN]))
            # Cerramos la conexión del socket UDP
            ackSocket.close()

        return message



    # Se envia el mensaje, se envia por paquetes por lo que se analiza su encabezado para ver su comportamiento
    def send(self,message):
        fin = 0
        success = False
        for i in range(0,len(message)):
            if i == len(message) - 1:
                fin = 1

            dataMessage = self.bitnator.encrypt(
                origenIp=self.ipDispatcher,
                origenPort=self.portDispatcher,
                destinationIp=self.ipDestination,
                destinationPort=self.portDestination,
                syn=0,
                rn=0,
                sn=self.SN,
                ack=0,
                fin=fin,
                message=message[i]
            )


            while success == False:
                # Creacion del socket UDP por e que se va a enviar el mensaje de aceptación
                ackSocket = socket(AF_INET, SOCK_DGRAM)
                # Enviamos el mensaje de aceptación
                ackSocket.sendto(dataMessage, (self.ipDestination, self.portDestination))
                # Cerramos la conexión del socket UDP
                ackSocket.close()

                try:
                    ackMessage = self.ackMailbox.get()
                    if ackMessage[RN] != self.SN:
                        self.SN = ackMessage[RN]

                    success = True
                except:
                    # No hacemos nada pues el mensaje se vuelve a enviar con el while
                    pass



    # Cierra la conexion despues del envio, por lo que se cierra en dos pasos(msj - ack)
    def close(self):
        # Creamos el paquete de close
        closeMessage = self.bitnator.encrypt(
            origenIp=self.ipDispatcher,
            origenPort=self.portDispatcher,
            destinationIp=self.ipDestination,
            destinationPort=self.portDestination,
            syn=1,
            rn=0,
            sn=self.SN,
            ack=0,
            fin=1,
            message=""
        )

        # Creacion del socket UDP por e que se va a enviar el mensaje de cierre
        ackSocket = socket(AF_INET, SOCK_DGRAM)
        # Enviamos el mensaje de aceptación
        ackSocket.sendto(closeMessage, (self.ipDestination, self.portDestination))
        # Cerramos la conexión del socket UDP
        ackSocket.close()

        try:
            # Si le llega un mesaje quiere decir que al otro le llego, pero independientemente de si le llega o no el nodo se muere
            # en cualquier otro caso al otro le toca solucionar el problema
            answerMessage = self.connMailbox.get()
        except:
            pass


    # Analiza el paquete, revisando el RN y SN y tomando la accion adecuada.
    def debugPacket(self,packetMessage):
        if packetMessage[SYN] == 1 and packetMessage[ACK] == 1 and packetMessage[FIN] == 0:
        # Entramos en el caso donde el paquete recibido es un ACK al paquete que inicia el handshake
            # Lo agregamos a la cola que guarda mensajes de conexión
            self.connMailbox.put_nowait(packetMessage)

        elif packetMessage[SYN] == 1 and packetMessage[ACK] == 1 and packetMessage[FIN] == 1:
        # Entramos en el caso donde el paquete recibido es un ACK al ACK enviado después de recibir un paquete que inicia el handshake
            # Lo agregamos a la cola que guarda paquete de conexión
            self.connMailbox.put_nowait(packetMessage)

        elif packetMessage[SYN] == 0 and packetMessage[ACK] == 0:
        # Entramos en el caso donde el paquete recibido lo que contiene son datos, no se pregunta por la bandera FIN, pues el
        # paquete puede no ser el útlimo de este tipo o sí, por lo que no importa el estado de la bandera FIN
            # Lo agregamos a la cola que guarda paquete con datos
            self.messageMailbox.put_nowait(packetMessage)

        elif packetMessage[SYN] == 0 and packetMessage[ACK] == 1 and packetMessage[FIN] == 0:
        # Entramos en el caso donde el paquete recibido lo que contiene es un ack al paquete que se envió con datos
            # Lo agregamos a la cola que guarda paquete de tipo ack
            self.ackMailbox.put_nowait(packetMessage)




    # Una vez que se detecto el SYN Flag encendio en el paquete se pasa a este metodo para procesarlo
    # El paquete puede ser solo el SYN o el SYN y el ACK.
    def processHandshake(self,decryptedMessage,myIp,myPort,mySocket):
        # Creo el socket que en caso de que se logre la conexion, será el que envía mensajes de respuesta al otro Nodo
        socketConexion = Dispatcher()
        socketConexion.socketUtil = mySocket
        socketConexion.RN = (decryptedMessage[RN] + 1) % 2
        socketConexion.SN = 0


        # Añado esta conexión al mapa de conexiones del nodo
        self.posibleConnections[(socketConexion.IPDestino, socketConexion.puertoDestino)] = socketConexion

        #Agregamos a la cola para iniciar el accept, esto hace que el método accept se empiece a ejecutar
        self.keys.append((socketConexion.IPDestino, socketConexion.puertoDestino))



    # Cerramos la conexión específica


