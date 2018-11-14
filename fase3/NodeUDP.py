from socket import *
from fase3.Node import *

class NodeUDP(Node):

    def __init__(self,address,mascara):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(address, mascara) # Ver como manejamos las direcciones aca

        # Tablas
        self.reachabilityTable = {}
        self.neighborTable = {}

        # Candados
        self.lockReach = threading.Lock()
        self.lockLog = threading.Lock()
        self.lockNeighbor = threading.Lock()

        # Creamos el socket servido del nodo
        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.bind(self.ad)

        self.listener = threading.Thread(name='daemon', target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()





    # Metodo que se encarga de recibir todos los mensajes que le llegan al nodo
    def listen(self):
        while self.alive:
            # Recibimos el paquete
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

            # Desencrptamos el paquete
            decrytedMessage = self.bitnator.decrypt(packetMessage)

            # Creamo un hilo que analiza el paquete
            thread = threading.Thread(name='Analizador', target=self.analysMessage, args=decrytedMessage)
            thread.setDaemon(True)
            thread.start()

        self.serverSocket.close()





    # Se encarga de analizar el paquete y dependiendo de las banderas que vienen activadas varía lo que hace
    def analysMessage(self,decryptedMessage):
        # Ve cuales son las banderas que están activadas, y dependiendo de esto hace algo diferente
        if decryptedMessage[SERVER_ACK] == 1:
            # Entramos en el caso de que el servidor le haya devuelto una respuesta con la información de los vecinos
            pass
        elif decryptedMessage[HELLO] == 1:
            # Entramos en el caso donde el despachador esta verificando sí el nodo está despierto o no
            self.send((decryptedMessage[SOURCE_IP],decryptedMessage[SOURCE_PORT]),0,0,0,1,0,0,0,0,"empty")
            pass
        elif decryptedMessage[UPDATE] == 1:
            # Entramos en el caso donde el mensaje recibido es una actualización de la tabla de alcanzabilidad
            pass
        elif decryptedMessage[TYPE] == 1:
            # Entramos en el caso donde lo recibido es un mensaje de datos
            pass





    # Se encarga de construir y enviar el mensaje al nodo que debe
    def send(self, otherAddress, ps, rs, sa, saAck, act, actAck, type, tv, data):
        success = False
        # Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # Envía un mensaje codificado
        encryptedMessage = self.bitnator.encrypt(
            addressOrigen=self.address,
            ps=ps,
            rs=rs,
            sa=sa,
            saAck=saAck,
            act=act,
            actAck=actAck,
            type=type,
            tv=tv,
            data=data
        )

        try:
            # Tratamos de enviar el mensaje, con la respuesta
            clientSocket.sendto(encryptedMessage, otherAddress)

        except:
            # No hacemo nada
            pass

        # Cerramos la conexión
        clientSocket.close()

        return success





    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False