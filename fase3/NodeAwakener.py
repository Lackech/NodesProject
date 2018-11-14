from socket import *
from fase3.Node import *
from fase3.NodeUDP import *
import csv



class NodeAwakener(Node):

    # Constructor por omisión
    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(NODE_AWAKENER_ADDRESS,NODE_AWAKENER_MASCARA)

        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.bind(NODE_AWAKENER_ADDRESS)





    # Se encarga de despertar todos los nodos que viene en el archivo que se recibió como parámetro
    def awakeNodesInFile(self,fileName):
        success = True

        # Aquí se va intentar abrir el archivo y comenzar a levantar los nodos, en caso de que haya un
        try:
            fileNameLength = len(fileName)

            # Preguntamos si el nombre es más largo que 4 => ".csv"
            if fileNameLength > 4:
                # Preguntamos si los 4 caracteres finales son los que nos indican que es un archivo tipo ".csv"
                if fileName[fileNameLength-4] == '.' and fileName[fileNameLength-3] == 'c' and fileName[fileNameLength-2] == 's' and fileName[fileNameLength-1] == 'v':
                    with open(fileName) as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            nodeAddress = (row[NODE_IP],row[NODE_PORT])
                            nodeMascara = row[NODE_MASCARA]
                            self.awakeNode(nodeAddress,nodeMascara)
                else:
                    success = False
            else:
                success = False
        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success





    # Se encarga de levantar un nodo, y verificar si se activó correctamente
    def awakeNode(self,nodeAddress,nodeMascara):
        success = True

        # Verificamos que el ip este bien
        information = self.router.validIp(nodeAddress[0])
        if information[0] == True:
            # Verificamos que tanto el puesto como la mascara sean validos
            if self.router.validPort(nodeAddress[1]) and self.router.validMascara(nodeMascara,information[1]):
                # Creamos el nodo
                NewNode = NodeUDP(nodeAddress,nodeMascara)

                # Verificamos si el nodo se creó correctamente
                success = self.verifyExistence(nodeAddress)
            else:
                success = False
        else:
            success = False

        return success





    # Se encarga de esperar la respuesta de los nodos que despertó
    def listenForAnswers(self,checkingAddress):
        success = False
        try:
            #Esperamos el paquete
            packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

            # Desencriptamos el mensaje
            decryptedMessage = self.bitnator.decrypt(packetMessage)

            # Verificamos si el mensaje es una respuesta
            if decryptedMessage[SOURCE_IP] == checkingAddress[IP] and decryptedMessage[SOURCE_PORT] == checkingAddress[
                PORT] and decryptedMessage[HELLO_ACK] == 1:

                success = True
        except:
            # Si ocurre un erro no hacemos nada
            pass

        return success





    # Se encarga de verificar sí el nodo se despertó correctamente
    def verifyExistence(self,otherAddress):
        success = False
        #Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        #Envía un mensaje codificado
        encryptedMessage = self.bitnator.encrypt(
            addressOrigen = otherAddress,
            ps = 0,
            rs = 0,
            sa = 1,
            saAck = 0,
            act = 0,
            actAck = 0,
            type = 0,
            tv = 0,
            data = "empty"
        )

        try:
            # Tratamos de enviar el mensaje
            clientSocket.sendto(encryptedMessage,otherAddress)

            # Esperamos una respuesta del nodo
            success = self.listenForAnswers(otherAddress)

        except:
            # No hacemo nada
            pass

        # Cerramos la conexión
        clientSocket.close()

        return success