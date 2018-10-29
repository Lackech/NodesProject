from fase2.nodeUDP import *

FLAG = 3

class Bitnator:

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
        encriptedMessage += message.encode('utf-8')

        # Retornamos el mensaje encriptado
        return encriptedMessage



    def encryptIp(self,ip):
        encriptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encriptedIp += int(s).to_bytes(1, 'big')

        return encriptedIp


    def decrypt(self, a,b,c,d,e,f,g,h,i,j,k,l,m,n):
        # Obtenmos el dato enviado ya en su forma desencriptada
        message = chr(n)

        # Obtenemos el conjunto de banderas que viene en un byte del mensaje
        flags = m
        # Nos desasemos de los bits de relleno
        flags = int(flags / 2)
        flags = int(flags / 2)
        flags = int(flags / 2)
        # Ahora con el módulo empezamos a preguntar si el valor de cada bandera es 1 o 0
        fin = int(flags % 2)
        flags = int(flags / 2)
        ack = int(flags % 2)
        flags = int(flags / 2)
        sn = int(flags % 2)
        flags = int(flags / 2)
        rn = int(flags % 2)
        flags = int(flags / 2)
        syn = int(flags % 2)


        # Obtenemos la dirección de la dirección destino
        destinationPort = l + k * 256
        # Como a la hora de realizar por se optinene primero el número de más a la derecha, se creo un método que acomodaba el Ip de la forma correcta
        destinationIp = str(g) + '.' + str(h) + '.' + str(i) + '.' + str(j)

        # Obtenemos la dirección de la dirección origen
        origenPort = f + e * 256
        # Como a la hora de realizar por se optinene primero el número de más a la derecha, se creo un método que acomodaba el Ip de la forma correcta
        origenIp = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

        return (origenIp,origenPort,destinationIp,destinationPort,syn,rn,sn,ack,fin,message)



    def acomodateIp(self,num4,num3,num2,num1):
        decriptedIp = num1 + '.' + num2 + '.' + num3 + '.' + num4
        return decriptedIp
