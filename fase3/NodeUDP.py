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

        # Decimos que el nodo está vivo
        self.alive = True

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
            pass
        elif decryptedMessage[UPDATE] == 1:
            # Entramos en el caso donde el mensaje recibido es una actualización de la tabla de alcanzabilidad
            pass
        elif decryptedMessage[TYPE] == 1:
            # Entrams en el caso donde lo recibido es un mensaje de datos
            pass





    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False