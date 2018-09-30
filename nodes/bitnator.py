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
    def bitEncript(self):
        numberOfElements = int(input("Select the number of elements:"))
        bytestring = '{0:016b}'.format(numberOfElements)

        for i in range(0, numberOfElements):
            ipAdress = input("Write the Ip adress:")
            stringIp = ipAdress.split('.')
            for s in stringIp:
                bytestring += '{0:08b}'.format(int(s))

            bytestring += '{0:08b}'.format(int(input("Write the Mascara adress:")))
            bytestring += '{0:024b}'.format(int(input("Write the Cost:")))

        return bytestring
