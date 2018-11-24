
# Diseño del paquete:
    ######################################################################################
    #           #               #            #                #      #         #         #
    # IP Origen # Puerto Origen # IP Destino # Puerto Destino # Tipo #    N    #  Datos  #
    #           #               #            #                #      #         #         #
    ######################################################################################
    #           #               #            #                #      #         #         #
    # 4 Bytes   #   2 Bytes     #  4 Bytes   #    2 Bytes     # Byte # 2 Bytes # N Bytes #
    #           #               #            #                #      #         #         #
    ######################################################################################

# Variables para accesar al ip y puerto en ls variables tipo address
IP = 0
PORT = 1

# Tipos de mensajes
ACTUALIZATION = 1
ALIVE = 2
YES_ALIVE = 3
FLOODING = 4
DATA = 5
COST = 6
DEATH = 7
DISPATCHER = 255
SERVER = 254

class Bitnator:

    # Encripción de paquetes que solo contienen el tipo [Muerte - Vivo/Respuesta - Pedir/Devolver]
    def encryptTypePacket(self,type):
        return type.to_bytes(1,'big')





    # Encripción de paquetes de tipo actualización
    def encryptActualizationPacket(self,n,reachabilityTable):
        encryptedPacket = bytearray()

        # Encriptamos el tipo
        encryptedPacket += ACTUALIZATION.to_bytes(1,'big')

        # Encriptamos el n
        encryptedPacket += n.to_bytes(2,'big')

        # Encriptamos la tabla de alcanzabilidad
        encryptedPacket += self.encryptReachabilityTable(reachabilityTable)

        return encryptedPacket





    # Se encarga de encriptar la lista de vecinos
    def encryptReachabilityTable(self, reachabilityTable):
        encryptedReachabilityTable = bytearray()

        for entrada in reachabilityTable:
            IP_split = entrada[0]
            port_split = entrada[1]
            mask_split = entrada[2]
            cost_split = entrada[3]
            IP_bit = self.encryptIp(IP_split)
            port_bit = int(port_split).to_bytes(2, 'big')
            mask_bit = int(mask_split).to_bytes(1, 'big')
            cost_bit = int(cost_split).to_bytes(3, 'big')

            encryptedReachabilityTable += IP_bit
            encryptedReachabilityTable += port_bit
            encryptedReachabilityTable += mask_bit
            encryptedReachabilityTable += cost_bit

        return encryptedReachabilityTable





    # Encripción de paquetes de inundación
    def encryptInundationPacket(self,jumps):
        encryptedPacket = bytearray()

        # Encriptamos el tipo
        encryptedPacket += FLOODING.to_bytes(1, 'big')

        # Encriptamos el número de saltos
        encryptedPacket += jumps.to_bytes(1, 'big')

        return encryptedPacket






    # Encripción de paquetes de datos
    def encryptDataPacket(self,originAddress,destinyAddress,n,data):
        encryptedPacket = bytearray()

        # Encriptamos el tipo
        encryptedPacket += DATA.to_bytes(1, 'big')

        # Encriptamos la dirección de salida
        encryptedPacket += self.encryptIp(originAddress[IP])
        encryptedPacket += originAddress[PORT].to_bytes(2,'big')

        # Encriptamos la dirección de llegada
        encryptedPacket += self.encryptIp(destinyAddress[IP])
        encryptedPacket += destinyAddress[PORT].to_bytes(2, 'big')

        # Encriptamos el número e datos enviados
        encryptedPacket += n.to_bytes(1, 'big')

        # Encriptamos los datos
        encryptedPacket += data.encode('utf-8')

        return encryptedPacket





    # Encripta el ip que recibe por parámetro
    def encryptIp(self, ip):
        encryptedIp = bytearray()

        if ip == "localhost":
            ip = "127.0.0.1"

        ipParts = ip.split('.')
        for s in ipParts:
            encryptedIp += int(s).to_bytes(1, 'big')

        return encryptedIp





    # Encripción de paquetes de costo
    def encryptCostPacket(self,type,cost):
        encryptedPacket = bytearray()

        # Encriptamos el tipo
        encryptedPacket += COST.to_bytes(1, 'big')

        # Encriptamos el costo
        encryptedPacket += cost.to_bytes(1, 'big')

        return encryptedPacket





    # Desencriptación de un paquete
    def decryptPacket(self,encryptedPacket):
        information = 0

        # Desencriptamos el tipo de paquete
        type = encryptedPacket[0]

        if type == ACTUALIZATION:
            n = encryptedPacket[1]*256 + encryptedPacket[2]
            list = self.decryptNeighbors(n,encryptedPacket[3:])

            information = (type,n,list)

        elif type == FLOODING:
            jumps = encryptedPacket[1]

            information = (type,jumps)

        elif type == DATA:
            # Obtenemos la dirección de quien está enviando el mensaje
            originIp = str(encryptedPacket[1]) + "." + str(encryptedPacket[2]) + "." + str(
                encryptedPacket[3]) + "." + str(encryptedPacket[4])
            originPort = encryptedPacket[5] * 256 + encryptedPacket[6]
            # Obtenemo l dirección de a quién se le está enviando el mensaje
            destinyIp = str(encryptedPacket[7]) + "." + str(encryptedPacket[8]) + "." + str(
                encryptedPacket[9]) + "." + str(encryptedPacket[10])
            destinyPort = encryptedPacket[11] * 256 + encryptedPacket[12]

            n = encryptedPacket[13]*256 + encryptedPacket[14]

            message = ""
            for i in range(15, n):
                # Concatenamos cada letra al mensaje
                message += str(encryptedPacket[i])

            information = (type,originIp,originPort,destinyIp,destinyPort,n,message)

        elif type == COST:
            cost = encryptedPacket[1]*65536 + encryptedPacket[2]*256 + encryptedPacket[3]

            information = (type,cost)

        else:
            information = (type)

        return information





    def decryptNeighbors(self,n,data):
        try:
            lista = []

            for i in range(0, n):

                # Optenemos el Ip
                num1 = data[i * 8 + 0]
                num2 = data[i * 8 + 1]
                num3 = data[i * 8 + 2]
                num4 = data[i * 8 + 3]

                address = str(num1) + "." + str(num2) + "." + str(num3) + "." + str(num4)

                port = data[i * 8 + 4] * 256 + data[i * 8 + 5]

                mask = data[i * 8 + 6]

                cost = data[i * 8 + 7] * 65536 + data[i * 8 + 8] * 256 + data[i * 8 + 9]

                lista.append((str(address),int(port),int(mask),int(cost)))


        except:
            pass

        return lista
