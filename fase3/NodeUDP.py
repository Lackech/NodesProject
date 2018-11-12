from socket import *
from fase3.Node import *

class NodeUDP:

    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(ADDRESS, MASCARA) # Ver como manejamos las direcciones aca

        # Tablas
        self.reachabilityTable = {}
        self.neighborTable = {}
        # Candados
        self.lockReach = threading.Lock()
        self.lockLog = threading.Lock()
        self.lockNeighbor = threading.Lock()

        # Decimos que el nodo está vivo
        self.alive = True

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))

