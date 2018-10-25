from fase2.nodeUDP import *

FLAG = 3

class Bitnator:

    #E BItnator debe ser capaz de codificar headers, mensajes, banderas y los demás bits que nos permiten saber que
    #que tipo de mensaje es

    #También debe poder decodificar todo lo que mencionamos anteriormente

    def __init__(self, node):
        self.node = node

    def encrypt(self,origenIp,origenPort,destinationIp,destinationPort,syn,rn,sn,ack,fin,message):
        encriptedMessage = bytearray()

        # Encriptamos las direcciones de origen y destino
        encriptedMessage += self.encryptIp(origenIp)
        encriptedMessage += origenPort.to_bytes(2,'big')
        encriptedMessage += self.encryptIp(destinationIp)
        encriptedMessage += destinationPort.to_bytes(2, 'big')

        # Encriptamos el bit de banders
        represetntativeValue = syn*128 + rn*64 + sn*32 + ack*16 + fin*8
        encriptedMessage += represetntativeValue.to_bytes(1,'big')

        # Encriptamos el dato que va a evniar el mensaje
        represetntativeValue += int(ord(message)).to_bytes(1,'big')

        # Retornamos el mensaje encriptado
        return encriptedMessage



    def encryptIp(self,ip):
        encriptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encriptedIp += int(s).to_bytes(1, 'big')

        return encriptedIp


    def decrypt(self, packet):
        # Obtenmos el dato enviado ya en su forma desencriptada
        message = chr(packet.pop())

        # Obtenemos el conjunto de banderas que viene en un byte del mensaje
        flags = packet.pop()
        # Nos desasemos de los bits de relleno
        flags = flags / 2
        flags = flags / 2
        flags = flags / 2
        # Ahora con el módulo empezamos a preguntar si el valor de cada bandera es 1 o 0
        syn = flags % 2
        flags = flags / 2
        rn = flags % 2
        flags = flags / 2
        sn = flags % 2
        flags = flags / 2
        ack = flags % 2
        flags = flags / 2
        fin = flags % 2

        # Obtenmos las direcciones correspondientes que se recibieron en el paquete
        destinationPort = packet.pop() * 256 + packet.pop()
        destinationIp = str(packet.pop()) + '.' + str(packet.pop()) + '.' + str(packet.pop()) + '.' + str(packet.pop())
        origenPort = packet.pop() * 256 + packet.pop()
        origenIp = str(packet.pop()) + '.' + str(packet.pop()) + '.' + str(packet.pop()) + '.' + str(packet.pop())

        return (origenIp,origenPort,destinationIp,destinationPort,syn,rn,sn,fin,message)
