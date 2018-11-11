# La dirección predeterminada del activador de nodos
NODE_AWAKENER_ADDRESS = ('localhost',12000)
NODE_AWAKENER_MASCARA = 2

# La dirección predeterminada del nodo con la información de los vecinos
NEIGHBOUR_LOCALIZER_ADDRESS = ('localhost',2000)
NEIGHBOUR_LOCALIZER_MASCARA = 2

# Lista con los nombres para localizar la información en el diccionario creado por el lector de archivos
NODE_IP = 'Node_ip'
NODE_MASCARA = 'Node_mascara'
NODE_PORT = 'Node_port'
NEIGHBOUR_IP = 'Neighbour_ip'
NEIGHBOUR_MASCARA = 'Neighbour_mascara'
NEIGHBOUR_PORT = 'Neighbour_port'
DISTANE = 'Distance'

class Node:

    # Contructor con parámetros
    def __init__(self,address,mascara):
        self.address = address
        self.mascara = mascara