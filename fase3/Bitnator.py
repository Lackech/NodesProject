
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

class Bitnator:

    '''
        addressOrigen :param, contien tanto el ip como el puerto de la dircción origen
        addressDestino :param, contiene tanto el ip como el puesto de la dirección destino
        type :param, indica que tipo de paquete se está enviando
        N :param, sí el mensaje es de datos indica la cantidad que se está enviando, sí es de alcanzabilidad dice la cantidad de filas
        data :param, la información que contiene el paquete
    '''

    def encrypt(self,addressOrigen,addressDestiny,type,data):
        encryptedMessage = bytearray()

        # Encriptamos la dirección de quien está enviando el paquete
        encryptedMessage += self.encryptIp(addressOrigen[IP])
        encryptedMessage += addressOrigen[PORT].to_bytes(2,'big')
        # Encriptamos la dirección de a queién se le está enviando el paquete
        encryptedMessage += self.encryptIp(addressDestiny[IP])
        encryptedMessage += addressDestiny[PORT].to_bytes(2, 'big')

        # Encriptamos el byte de banderas
        encryptedMessage += type.to_bytes(1,'big')

        # Encriptamos los datos que vienen en el mensaje, primero tenemos que ver que información se va a enviar
        # puede ser un mensaje normal, o la lista de vecinos, para eso verificamos si la bandera rs o act están
        # encendidas
        if type == 1 or type == 4 or type == 5:
            # Encritamos el byte que dice la cantidad de datos enviados
            if type == 1 or type == 4:
                # Quiere decir que en los datos viene una lista de vecinos, por lo que tiene un proceso de
                # encriptación diferente
                encryptedMessage += int(len(data)/4).to_bytes(2, 'big')
                encodedData = self.encryptNeighbours(data)
            else:
                encodedData = data.encode('utf-8')
                encryptedMessage += len(encodedData).to_bytes(2, 'big')

            # Conccatenamos los datos encriptados
            encryptedMessage += encodedData

        # Retornamos el mensaje encriptado
        return encryptedMessage



    # Se encarga de encriptar la lista de vecinos
    def encryptNeighbours(self,data):
        try:

            mensaje = bytearray()
            for entrada in data:
                IP_split = entrada[0]
                port_split = entrada[1]
                mask_split = entrada[2]
                cost_split = entrada[3]
                IP_bit = self.encryptIp(IP_split)
                port_bit = int(port_split).to_bytes(2,'big')
                mask_bit = int(mask_split).to_bytes(1,'big')
                cost_bit = int(cost_split).to_bytes(3,'big')

                mensaje += IP_bit
                mensaje += port_bit
                mensaje += mask_bit
                mensaje += cost_bit

        except:
            pass


        return mensaje



    def decryptNeighbors(self,n,data):
        try:
            lista = []
            j = 0
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

    # Encripta el ip que recibe por parámetro
    def encryptIp(self,ip):
        encryptedIp = bytearray()

        if ip == "localhost":
            ip = "127.0.0.1"

        ipParts = ip.split('.')
        for s in ipParts:
            encryptedIp += int(s).to_bytes(1, 'big')

        return encryptedIp





    def decrypt(self, encryptedMessage):
        information = 0

        # Obtenemos la dirección de quien está enviando el mensaje
        sourceIp = str(encryptedMessage[0]) + "." + str(encryptedMessage[1]) + "." + str(encryptedMessage[2]) + "." + str(encryptedMessage[3])
        sourcePort = encryptedMessage[4]*256 + encryptedMessage[5]
        # Obtenemo l dirección de a quién se le está enviando el mensaje
        destinyIp = str(encryptedMessage[6]) + "." + str(encryptedMessage[7]) + "." + str(encryptedMessage[8]) + "." + str(encryptedMessage[9])
        destinyPort = encryptedMessage[10]*256 + encryptedMessage[11]

        # Obtenemos el tipo de mensaje que se recibió
        type = encryptedMessage[12]

        # Preguntamos que tipo de mensaje es, dependiendo de esto varía la forma de decodificar los datos
        if type == 1 or type == 4 or type == 5:
            # Obtenemos el byte que contiene el número de vecinos
            n = encryptedMessage[13]*256 + encryptedMessage[14]

            if type == 1 or type == 4:
                # Quiere decir que es un mensaje con una Tbla de alcanzabilidad o vecinos
                message = self.decryptNeighbors(n,encryptedMessage[15:])
            else:
                message = ""
                for i in range(15, n):
                    # Concatenamos cada letra al mensaje
                    message += str(encryptedMessage[i])

            information = (sourceIp, sourcePort, destinyIp, destinyPort, type, n, message)

        else:
            information = (sourceIp, sourcePort, destinyIp, destinyPort, type)

        return information
