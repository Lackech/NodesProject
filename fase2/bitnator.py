from fase2.nodeUDP import *

FLAG = 3

class Bitnator:

    def __init__(self, node):
        self.node = node

    def encryptConnectPacket(self,myAddress,otherAddress,SYN,ACK):
        packet = bytearray()

        packet += self.encryptAddress(myAddress)
        packet += self.encryptAddress(otherAddress)

        packet += int(0).to_bytes(1, 'big')

        packet += SYN.to_bytes(1, 'big')
        packet += ACK.to_bytes(1, 'big')


    def encryptAddress(self,addres):
        encriptedAddres = bytearray()

        #Encripta el Ip
        ipParts = addres[0].split('.')
        for s in ipParts:
            encriptedAddres += int(s).to_bytes(1, 'big')

        #Encripta el Puerto
        encriptedAddres += addres[1].to_bytes(2, 'big')

        return encriptedAddres

    def decryptPacket(self, packet):
        packetParts = []

        #Decodifica la parte del header
        packetParts.extend(self.decryptHeader(packet))

        #Decodifica la bandera
        packetParts.append(packet[13])

        packetParts.append(packet[14])
        packetParts.append(packet[15])

    def decryptHeader(self,packet):
        headerParts = []

        for i in range(0,2):
            num1 = packet[i*6]
            num2 = packet[i*6+1]
            num3 = packet[i*6+2]
            num4 = packet[i*6+3]

            addressIp = str(num1) + "." + str(num2) + "." + str(num3) + "." + str(num4)

            addressPort = packet[i*6+4]*256 + packet[i*6+5]

            headerParts.append((addressIp,addressPort))

        return headerParts
