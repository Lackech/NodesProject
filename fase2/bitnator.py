from fase2.nodeUDP import *

FLAG = 3

class Bitnator:

    #E BItnator debe ser capaz de codificar headers, mensajes, banderas y los demás bits que nos permiten saber que
    #que tipo de mensaje es

    #También debe poder decodificar todo lo que mencionamos anteriormente

    def __init__(self, node):
        self.node = node

    def encrypt(self,origenIp,origenPort,destinationIp,destinationPort,syn,rn,sn,ack,message):
        packet = bytearray()

        packet += self.encryptAddress(myAddress)
        packet += self.encryptAddress(otherAddress)

        packet += int(0).to_bytes(1, 'big')

        packet += data1.to_bytes(1, 'big')

        try:
            packet += data1.to_bytes(1, 'big')
        except:
            packet += ord(data1).to_bytes(1, 'big')

        return packet



    def decrypt(self, packet):
        packetParts = []

        #Decodifica la parte del header
        packetParts.extend(self.decryptHeader(packet))

        #Decodifica la bandera
        packetParts.append(packet[13])

        packetParts.append(packet[14])
        packetParts.append(packet[15])