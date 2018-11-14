
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
        encriptedMessage = bytearray()

        # Encriptamos la dirección de quien está enviando el mensaje
        encriptedMessage += self.encryptIp(addressOrigen[IP])
        encriptedMessage += addressOrigen[PORT].to_bytes(2,'big')

        # Encriptamos el byte de banderas
        represetntativeValue = ps*128 + rs*64 + sa*32 + saAck*16 + act*8 + actAck*4 + type*2
        encriptedMessage += represetntativeValue.to_bytes(1,'big')

        # Encritamos el byte que contiene el tamaño de vecinos
        encriptedMessage += tv.to_bytes(1, 'big')

        # Encriptamos los datos que vienen en el mensaje, primero tenemos que ver que información se va a enviar
        # puede ser un mensaje normal, o la lista de vecinos, para eso verificamos si la bandera rs o act están
        # encendidas
        if rs == True or act == True:
            # Quiere decir que en los datos viene una lista de vecinos, por lo que tiene un proceso de
            # encriptación diferente
            self.encryptNeighbours(tv,data)
        else:
            # Quiere decir que los datos son de tipo mensaje normal
            encriptedMessage += data.encode('utf-8')

        # Retornamos el mensaje encriptado
        return encriptedMessage



    # Se encarga de encriptar la lista de vecinos
    def encryptNeighbours(self,tv,data):
        # Aquí es donde se encripta la lista de vecinos
        pass




    # Encripta el ip que recibe por parámetro
    def encryptIp(self,ip):
        encriptedIp = bytearray()

        ipParts = ip.split('.')
        for s in ipParts:
            encriptedIp += int(s).to_bytes(1, 'big')

        return encriptedIp





    def decrypt(self, encryptedMessage):
        # Obtenemos la dirección de quien está enviando el mensaje
        origenIp = str(encryptedMessage[0]) + "." + str(encryptedMessage[1]) + "." + str(encryptedMessage[2]) + "." + str(encryptedMessage[3])
        origenPort = encryptedMessage[4]*256 + encryptedMessage[5]

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

        # Falta la parte de desencriptar el mensaje o vecinos
