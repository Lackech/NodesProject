from socket import *

class nodeTCP:

    #constructor del nodo
    def __init__(self, ip, port):
        #ip del nodo creado
        self.ip = ip
        #puerto habilitado del nodo
        self.port = port

