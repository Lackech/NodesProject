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

# Variables de flag del paquete
SOURCE_IP = 1
SOURCE_PORT = 2
SERVER_REQUEST = 3
SERVER_ACK = 4
HELLO = 5
HELLO_ACK = 6
UPDATE = 7
UPDATE_ACK = 8
TYPE = 9
MESSAGE = 10




class Node:

    # Contructor con parámetros
    def __init__(self,address,mascara):
        # Guardamos la información del nodo
        self.address = address
        self.mascara = mascara

        # Creamos el validador de rutas
        self.router = Router()


    def encrypt(self):
        encriptedMessage = bytearray()


        # Retornamos el mensaje encriptado
        return encriptedMessage



    def encryptIp(self,ip):
        encriptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encriptedIp += int(s).to_bytes(1, 'big')

        return encriptedIp


    def decrypt(self, packet):


        return (origenIp,origenPort,serverRequest,serverACK,hello,helloACK,update,updateACK,type,message)


    def acomodateIp(self,num4,num3,num2,num1):
        decriptedIp = num1 + '.' + num2 + '.' + num3 + '.' + num4
        return decriptedIp

