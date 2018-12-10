from socket import *
from os import system
from fase3.Node import *
from fase3.NodeUDP import *

import csv
import queue



class NodeAwakener(Node):

    # Constructor por omisión
    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,NODE_AWAKENER_ADDRESS,NODE_AWAKENER_MASCARA)

        self.answerQueue = queue.Queue(1)

        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketServer.bind(NODE_AWAKENER_ADDRESS)

        # Variabes que sirven para comunicarse con el usuario
        self.greetingMessage = "Welcome to the Node Awakener!!\n\n"
        self.optionMessage = ("Please select one of the following options:\n",
                              "\t1. Wake nodes in a CSV file\n",
                              "\t2. Wake an specific node\n",
                              "\t3. Exit\n"
                              "\t Your answer --> ")

        self.invalidFileNameMessage = " -- is not a valid file name"
        self.failedCreatingNodeMessage = "Sorry something went wrong creating the Node: "

        self.fileNameMessage = "Please write the file name -->"





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
                        reader = csv.reader(csvfile,delimiter=',')
                        for row in reader:
                            nodeAddress = (row[NODE_IP],int(row[NODE_PORT]))
                            nodeMascara = int(row[NODE_MASCARA])
                            success = self.awakeNode(nodeAddress,nodeMascara)
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
                system("start python createNodeUDP.py " + nodeAddress[0] + " " + str(nodeAddress[1]) + " " + str(nodeMascara))

                # Creamos la bitacora para el nodo
                self.createLog()


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
            packetMessage, clientAddress = self.socketServer.recvfrom(2048)

            # Desencriptamos el mensaje
            decryptedMessage = self.bitnator.decryptPacket(packetMessage)

            # Verificamos si el mensaje es una respuesta
            if clientAddress[IP] == checkingAddress[IP] and clientAddress[PORT] == checkingAddress[
                PORT] and decryptedMessage[TYPE] == DISPATCHER:
                
                success = True
        except:
            # Si ocurre un erro no hacemos nada
            pass

        return success





    # Se encarga de verificar sí el nodo se despertó correctamente
    def verifyExistence(self,otherAddress):
        success = False

        #Envía un mensaje codificado
        encryptedMessage = self.bitnator.encryptTypePacket(DISPATCHER)

        try:
            # Esperamos a que el nodo se cree, para poder enviar el mensaje
            try:
                self.answerQueue.get(timeout=2)
            except:
                pass

            # Tratamos de enviar el mensaje
            self.socketServer.sendto(encryptedMessage,otherAddress)

            # Esperamos una respuesta del nodo
            success = self.listenForAnswers(otherAddress)

        except:
            # No hacemo nada
            pass

        return success





    # Menú que se encarga de realizar las diferentes acciones que el despachador puede hacer
    def nodeAwakenerMenu(self):
        print(self.greetingMessage)
        while self.alive:
            answer = input(self.optionMessage)

            try:
                intAnswer = int(answer)
                if intAnswer == 1:
                    fileName = input(self.fileNameMessage)
                    if self.awakeNodesInFile(fileName) == False:
                        print(self.warningMessage + fileName + self.invalidFileNameMessage)
                elif intAnswer == 2:
                    nodeAddress,nodeMascara = self.getNodeInformation()
                    if self.awakeNode(nodeAddress,nodeMascara) == False:
                        print(self.warningMessage + self.failedCreatingNodeMessage + nodeAddress[IP] + str(nodeAddress[PORT]))
                elif intAnswer == 3:
                    self.alive = False
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            except:
                print(self.warningMessage + answer + self.invalidOptionMessage)


    def createLog(self):
        file = open("log.txt","w+")
        file.write("DESTINO,ORIGEN,ACCION\n")
        file.close()
