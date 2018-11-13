from fase3.Router import *
from fase3.Bitnator import *
import threading
from socket import *

# La dirección predeterminada del activador de nodos
NODE_AWAKENER_ADDRESS = ('localhost',12000)
NODE_AWAKENER_MASCARA = 2

# La dirección predeterminada del nodo con la información de los vecinos
NEIGHBOR_SERVER_ADDRESS = ('localhost',2000)
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
SERVER_REQUEST = 2
SERVER_ACK = 3
HELLO = 4
HELLO_ACK = 5
UPDATE = 6
UPDATE_ACK = 7
TYPE = 8
MESSAGE = 9

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




