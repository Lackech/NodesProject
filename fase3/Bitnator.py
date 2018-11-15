
# Diseño del paquete:
    ########################################################################################################################
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    # IP Origen # Puerto Origen #  P.S  #  R.S  #  S.A  #  ACK  #  Act  #  ACK   #  Tipo  #  Relleno  #  T.V  #   Datos   ##
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    ########################################################################################################################
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    # 4 Bytes   #   2 Bytes     #  bit  #  bit  #  bit  #  bit  #  bit  #  bit   #  bit   #    bit    # byte  # 512 bytes ##
    #           #               #       #       #       #       #       #        #        #           #       #           ##
    ########################################################################################################################

# Variables para accesar al ip y puerto en ls variables tipo address
IP = 0
PORT = 1

class Bitnator:

    '''
        addressOrigen :param, contien tanto el ip como el puerto de la dircción origen
        ps :param, bandera - petición al servidor
        rs :param, bandera - respuesta del servidor
        sa :param, bandera - saludo Awekener
        saAck :param, bandera - ack Awekener
        act :param, bandera - actualización
        actAck :param, badera - ack actualización
        type :param, bandera - dice sí es de tipo mensaje normal, o sí es una actualización
        tv :param, tamaño de vecinos, número de vecinos que vienen en la sección de datos
        data :param, los datos, pueden se un mensaje o la lista con los vecinos
    '''

    def encrypt(self,addressOrigen,ps,rs,sa,saAck,act,actAck,type,tv,data):
        encryptedMessage = bytearray()

        # Encriptamos la dirección de quien está enviando el mensaje
        encryptedMessage += self.encryptIp(addressOrigen[IP])
        encryptedMessage += addressOrigen[PORT].to_bytes(2,'big')

        # Encriptamos el byte de banderas
        represetntativeValue = ps*128 + rs*64 + sa*32 + saAck*16 + act*8 + actAck*4 + type*2
        encryptedMessage += represetntativeValue.to_bytes(1,'big')

        # Encriptamos los datos que vienen en el mensaje, primero tenemos que ver que información se va a enviar
        # puede ser un mensaje normal, o la lista de vecinos, para eso verificamos si la bandera rs o act están
        # encendidas
        if rs == 1 or act == 1:
            # Quiere decir que en los datos viene una lista de vecinos, por lo que tiene un proceso de
            # encriptación diferente
            neighborMessage = self.encryptNeighbours(tv,data)



            # Encritamos el byte que dice la cantidad de datos enviados
            encryptedMessage += tv.to_bytes(1, 'big')

            # Conccatenamos los datos encriptados
            encryptedMessage += neighborMessage
            freeSpace = 255 - (tv * 8)
            hole = bytearray(freeSpace)
            # Encritamos el byte que dice la cantidad de datos enviados
            encryptedMessage += hole




        else:
            # Quiere decir que los datos son de tipo mensaje normal
            encodedData = data.encode('utf-8')
            freeSpace = 255 - len(encodedData)

            # Encritamos el byte que dice la cantidad de datos enviados
            encryptedMessage += freeSpace.to_bytes(1, 'big')

            # Conccatenamos los datos encriptados
            encryptedMessage += encodedData

        # Retornamos el mensaje encriptado
        return encryptedMessage



    # Se encarga de encriptar la lista de vecinos
    def encryptNeighbours(self,tv,data):
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
                cost_bit = int(cost_split).to_bytes(1,'big')

                mensaje += IP_bit
                mensaje += port_bit
                mensaje += mask_bit
                mensaje += cost_bit

        except:
            pass


        return mensaje



    def decryptNeighbors(self,tv,data):
        try:
            lista = []
            j = 0
            for i in range(0, tv):

                # Optenemos el Ip
                num1 = data[i * 8 + 0]
                num2 = data[i * 8 + 1]
                num3 = data[i * 8 + 2]
                num4 = data[i * 8 + 3]

                address = str(num1) + "." + str(num2) + "." + str(num3) + "." + str(num4)

                port = data[i * 8 + 4] * 256 + data[i * 8 + 5]

                mask = data[i * 8 + 6]

                cost = data[i * 8 + 7]

                lista.append((str(address),int(port),int(mask),int(cost)))


        except:
            pass

        return lista

    # Encripta el ip que recibe por parámetro
    def encryptIp(self,ip):
        encryptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encryptedIp += int(s).to_bytes(1, 'big')

        return encryptedIp





    def decrypt(self, encryptedMessage):
        # Obtenemos la dirección de quien está enviando el mensaje
        sourceIp = str(encryptedMessage[0]) + "." + str(encryptedMessage[1]) + "." + str(encryptedMessage[2]) + "." + str(encryptedMessage[3])
        sourcePort = encryptedMessage[4]*256 + encryptedMessage[5]

        # Obtenemos el conjunto de banderas que viene en un byte del mensaje
        flags = encryptedMessage[6]
        # Nos desasemos de los bits de relleno
        flags = int(flags / 2)
        # Ahora con el módulo empezamos a preguntar si el valor de cada bandera es 1 o 0
        type = int(flags % 2)
        flags = int(flags / 2)
        actAck = int(flags % 2)
        flags = int(flags / 2)
        act = int(flags % 2)
        flags = int(flags / 2)
        saAck = int(flags % 2)
        flags = int(flags / 2)
        sa = int(flags % 2)
        flags = int(flags / 2)
        rs = int(flags % 2)
        flags = int(flags / 2)
        ps = int(flags % 2)

        # Obtenemos el byte que contiene el número de vecinos
        tv = encryptedMessage[7]

        # Creamos un mensaje vació, que solo en caso de que venga información de vecinos o datos es que se llena
        message = 0

        # Preguntamos que tipo de mensaje es, dependiendo de esto varía la forma de decodificar los datos
        if rs == 1 or act == 1:
            # Quiere decir que es un mensaje con una Tbla de alcanzabilidad o vecinos
            message = self.decryptNeighbors(tv,encryptedMessage[8:])
        elif type == 1:
            # Quire decir que es un mensaje que contiene datos
            for i in range(8,tv):
                # Concatenamos cada letra al mensaje
                message += str(encryptedMessage[i])

        return (sourceIp,sourcePort,ps,rs,sa,saAck,act,actAck,type,tv,message)
