from fase3.Router import *
from fase3.Bitnator import *
import threading
from socket import *

# La dirección predeterminada del activador de nodos
NODE_AWAKENER_ADDRESS = ('localhost',12000)
NODE_AWAKENER_MASCARA = 2

# La dirección predeterminada del nodo con la información de los vecinos
NEIGHBOR_SERVER_ADDRESS = ('127.0.0.1',2000)
NEIGHBOR_SERVER_MASCARA = 2

# Variables para accesar al ip y puerto en ls variables tipo address
IP = 0
PORT = 1

# Lista con los nombres para localizar la información en el diccionario creado por el lector de archivos
NODE_IP = 'Node_ip'
NODE_MASCARA = 'Node_mascara'
NODE_PORT = 'Node_port'
NEIGHBOR_IP = 'Neighbor_ip'
NEIGHBOR_MASCARA = 'Neighbor_mascara'
NEIGHBOR_PORT = 'Neighbor_port'
DISTANE = 'Distance'

# Variables de flag del paquete
SOURCE_IP = 0
SOURCE_PORT = 1
DESTINY_IP = 2
DESTINY_PORT = 3
TYPE = 4
N = 5
DATA = 6

# Diseño del paquete:
    ########################################################################################################################
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    # IP Origen # Puerto Origen #  P.S  #  R.S  #  S.A  #  ACK  #  Act  #  ACK   #  Tipo  #  Relleno  #  T.V  #   Datos   ##
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    ########################################################################################################################
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    # 4 Bytes   #   2 Bytes     #  bit  #  bit  #  bit  #  bit  #  bit  #  bit   #  bit   #    bit    # byte  # 512 bytes ##
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    ########################################################################################################################


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
