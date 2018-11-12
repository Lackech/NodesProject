from fase3.Router import *
import threading
from socket import *

# La dirección predeterminada del activador de nodos
NODE_AWAKENER_ADDRESS = ('localhost',12000)
NODE_AWAKENER_MASCARA = 2

# La dirección predeterminada del nodo con la información de los vecinos
NEIGHBOR_SERVER_ADDRESS = ('localhost',2000)
NEIGHBOR_SERVER_MASCARA = 2

# Lista con los nombres para localizar la información en el diccionario creado por el lector de archivos
NODE_IP = 'Node_ip'
NODE_MASCARA = 'Node_mascara'
NODE_PORT = 'Node_port'
NEIGHBOR_IP = 'Neighbor_ip'
NEIGHBOR_MASCARA = 'Neighbor_mascara'
NEIGHBOR_PORT = 'Neighbor_port'
DISTANE = 'Distance'

class Node:

    # Contructor con parámetros
    def __init__(self,address,mascara):
        # Guardamos la información del nodo
        self.address = address
        self.mascara = mascara

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



        # Creamos el validador de rutas
        self.router = Router()
