from fase3.Router import *
from fase3.Bitnator import *
import threading
from socket import *

# La dirección predeterminada del activador de nodos
NODE_AWAKENER_ADDRESS = ('10.1.137.87',12000)
NODE_AWAKENER_MASCARA = 24

# La dirección predeterminada del nodo con la información de los vecinos
NEIGHBOR_SERVER_ADDRESS = ('10.1.137.87',2000)
NEIGHBOR_SERVER_MASCARA = 24

# Lista con los nombres para localizar la información en el diccionario creado por el lector de archivos
NODE_IP = 0
NODE_MASCARA = 1
NODE_PORT = 2
NEIGHBOR_IP = 3
NEIGHBOR_MASCARA = 4
NEIGHBOR_PORT = 5
DISTANCE = 6

# Posición de cada valor en el paquete ya desencriptado, para cada uno de los diferentes tipos de paquete
# -----GENERAL----- #

TYPE = 0

# -----ACTUALIZACION----- #

N_ACT = 1
REACHEABILITY_TABLE = 2


# -----INUNDACION----- #

JUMPS = 1 #Posicion en el paquete
HOPS = 15
# -----DATOS----- #

ORIGIN_IP = 1
ORIGIN_PORT = 2
DESTINY_IP = 3
DESTINY_PORT = 4
N_DATA = 5
MESSAGE = 6

# -----COSTO----- #
PRICE = 1


# -----Vecinos------#
POS_IP_VEC = 0
POS_PORT_VEC = 1

POS_MASCARA_VEC = 0
POS_COSTO_VEC = 1
POS_DESPIERTO_VEC = 2

#-----Timeout---------#
TIMEOUT_SALUTO = 60

class Node:

    # Contructor con parámetros
    def __init__(self,address,mascara):
        # Guardamos la información del nodo
        self.address = address
        self.mascara = mascara

        # Creamos el validador de rutas
        self.router = Router()

        # Creamos el codificador y decodificador de mensajes
        self.bitnator = Bitnator()

        # Booleano que nos permite saber sí el nodo sigue vivo
        self.alive = True


        # Variabes que sirven para comunicarse con el usuario
        self.ipMessage = "\tWrite the Node's Ip: "
        self.portMessage = "\tWrite Node's Port: "
        self.mascaraMessage = "\tWrite Node's Mascara: "

        self.warningMessage = "\tWARNING -- \""
        self.invalidIpMessage = "\" -- is not a valid IP"
        self.invalidPortMessage = "\" -- is not a valid Port"
        self.invalidMascaraMessage = "\" -- is not a valid Mascara"
        self.invalidOptionMessage = " -- is not a valid option"



    def optainNodeIp(self):
        nodeIp = input(self.ipMessage)
        information = self.router.validIp(nodeIp)
        while information[0] is False:
            print(self.warningMessage + nodeIp + self.invalidIpMessage)
            nodeIp = input(self.ipMessage)
            information = self.router.validIp(nodeIp)

        return nodeIp,information[1]





    def optainNodePort(self):
        nodePort = input(self.portMessage)
        while self.router.validPort(nodePort) is False:
            print(self.warningMessage + nodePort + self.invalidPortMessage)
            nodePort = input(self.portMessage)

        return int(nodePort)





    def optainNodeMascara(self,networkType):
        nodeMascara = input(self.mascaraMessage)
        while self.router.validMascara(nodeMascara,networkType) is False:
            print(self.warningMessage + nodeMascara + self.invalidMascaraMessage)
            nodeMascara = input(self.mascaraMessage)

        return int(nodeMascara)





    def getNodeInformation(self):
        nodeIp,networkType = self.optainNodeIp()
        nodePort = self.optainNodePort()
        nodeMascara = self.optainNodeMascara(networkType)
        return (nodeIp,nodePort),nodeMascara
