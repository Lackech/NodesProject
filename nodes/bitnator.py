from nodes.node import *
class Bitnator:

    def __init__(self, node):
        self.node = node

    def bitDecrypt(self, packetMessage, senderAddress):
        # Optenemos la cantidad de mensajes recibidos
        num = packetMessage.split()[0][:16]
        n = int(num, 2)
        print(n)
        for i in range(0, n):
            # Optenemos el Ip
            num1 = packetMessage[(i * 64) + 8 * 2:(i * 64) + 8 * 3]
            n1 = int(num1, 2)
            num2 = packetMessage[(i * 64) + 8 * 3:(i * 64) + 8 * 4]
            n2 = int(num2, 2)
            num3 = packetMessage[(i * 64) + 8 * 4:(i * 64) + 8 * 5]
            n3 = int(num3, 2)
            num4 = packetMessage[(i * 64) + 8 * 5:(i * 64) + 8 * 6]
            n4 = int(num4, 2)

            address = str(n1) + "." + str(n2) + "." + str(n3) + "." + str(n4)
            print(address)

            # Optenemos la máscara
            mask = packetMessage[(i * 64) + 8 * 6:(i * 64) + 8 * 7]
            maskNum = int(mask, 2)
            print(maskNum)

            # Optenemos el costo
            cost = packetMessage[(i * 64) + 8 * 7:(i * 64) + 8 * 10]
            costNum = int(cost, 2)
            print(costNum)

            # Guardamos en la tabla de alcanzabilidad
            self.node.saveDataTable(address,maskNum,costNum,senderAddress)
            #self.saveDataTable(address, maskNum, costNum, senderAddress)

    # Método para codificar mensaje
    def bitEncript(self,messageList):
        numberOfElements = messageList.pop(0)
        bytestring = numberOfElements.to_bytes(2,'big')

        for i in range(0, numberOfElements):
            message = messageList.pop()
            ipAdress = message[0]
            ipParts = ipAdress.split('.')
            for s in ipParts:
                bytestring += int(s).to_bytes(1,'big')

            bytestring += message[1].to_bytes(1,'big')
            bytestring += message[2].to_bytes(3,'big')

        print(bytestring)
        return bytestring
