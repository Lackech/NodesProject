from nodes.node import *
class Bitnator:

    def __init__(self, node):
        self.node = node

    def bitDecrypt(self, packetMessage, senderAddress):
        # Optenemos la cantidad de mensajes recibidos
        numberOfElements = packetMessage[0]*256 + packetMessage[1]

        for i in range(0, numberOfElements):
            # Optenemos el Ip
            num1 = packetMessage[i*8+2]
            num2 = packetMessage[i*8+3]
            num3 = packetMessage[i*8+4]
            num4 = packetMessage[i*8+5]

            address = str(num1) + "." + str(num2) + "." + str(num3) + "." + str(num4)

            # Optenemos la máscara
            mask = packetMessage[i*8+6]

            # Optenemos el costo
            cost = packetMessage[i*8+7]*65536 + packetMessage[i*8+8]*256 + packetMessage[i*8+9]

            # Guardamos en la tabla de alcanzabilidad
            self.node.saveDataTable(address,mask,cost,senderAddress)



    # Método para codificar mensaje
    def bitEncript(self,messageList):
        numberOfElements = messageList.pop(0)
        encriptedMessage = bytearray()
        encriptedMessage += numberOfElements.to_bytes(2,'big')

        for i in range(0, numberOfElements):
            message = messageList.pop()
            ipAdress = message[0]
            ipParts = ipAdress.split('.')
            for s in ipParts:
                encriptedMessage += int(s).to_bytes(1,'big')

            encriptedMessage += message[1].to_bytes(1,'big')
            encriptedMessage += message[2].to_bytes(3,'big')

        return encriptedMessage
