from socket import *
from fase3.Node import *
import queue

class NodeUDP(Node):

    def __init__(self,address,mascara):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,address, mascara) # Ver como manejamos las direcciones aca

        # Creamos el socket servido del nodo
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(self.address)

        self.listener = threading.Thread(name='daemon', target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()

        # Creamos el hilo que se va a encargar de enviar la tabla cada 30 segundos
        thread = threading.Thread(name='Analizador', target=self.sendReacheabilityTable)
        thread.setDaemon(True)
        thread.start()

        self.waitingQueue = queue.Queue(1)

        # Tablas
        self.reachabilityTable = {}
        self.neighborTable = {}

        # Candados
        self.lockReach = threading.Lock()
        self.lockLog = threading.Lock()
        self.lockNeighbor = threading.Lock()

        # Variabes que sirven para comunicarse con el usuario
        self.greetingMessage = "Welcome to the Node UDP...\n\n"
        self.optionMessage = ("Please select one of the following options:\n"
                              "\t1. Change a link's distance\n"
                              "\t2. Kill myself\n"
                              "\t3. Print reachability table\n"
                              "\t4. Exit\n"
                              "\tYour answer --> ")

        self.neighborOptionMessage = "Please write the number of the Node to modify --> "
        self.changeDistanceMessage = "Please write the new distance --> "

        self.failedUpdate = "Sorry something went updating the Node distance"

        self.nodeUDPMenu()





    # Metodo que se encarga de recibir todos los mensajes que le llegan al nodo
    def listen(self):

        try:
            self.send(NEIGHBOR_SERVER_ADDRESS,1,"empty")
            while self.alive:
                # Recibimos el paquete
                packetMessage, clientAddress = self.serverSocket.recvfrom(2048)

                # Desencrptamos el paquete
                decrytedMessage = self.bitnator.decrypt(packetMessage)

                # Creamo un hilo que analiza el paquete
                thread = threading.Thread(name='Analizador', target=self.analysMessage, args=decrytedMessage)
                thread.setDaemon(True)
                thread.start()

            self.serverSocket.close()


        except:
            pass






    # Se encarga de analizar el paquete y dependiendo de las banderas que vienen activadas varía lo que hace
    def analysMessage(self,sourceIp,sourcePort,destinyIp,destinyPort,type,n,data):
        # Ve cuales son las banderas que están activadas, y dependiendo de esto hace algo diferente
        if type == 1:
            # Entramos en el caso de que el servidor le haya devuelto una respuesta con la información de los vecinos
            for row in data:
                self.neighborTable[row[0:3]] = row[3]

        elif type == 2:
            # Entramos en el caso donde el despachador esta verificando sí el nodo está despierto o no
            if self.send((sourceIp,sourcePort),3,"empty") == False:
                # Algo ocurrió en el proceso que no permitió enviar el mensaje correctamente
                pass
        elif type == 1:
            try:
                self.lockReach.acquire()
                self.lockNeighbor.acquire()
                # Entramos en el caso donde el mensaje recibido es una actualización de la tabla de alcanzabilidad
                for row in data:
                    # Preguntamos sí el está o no en la tabla de alcanzabilidad
                    if row[0] == self.address[IP] and row[1] == self.address[PORT] and row[2] == self.mascara and self.neighborTable.get((sourceIp,sourcePort,sourceMask)) is not None:
                        self.neighborTable[(sourceIp,sourcePort,sourceMask)] = row[3]

                    elif (self.neighborTable.get(row[0:3]) is None and (self.reachabilityTable.get(row[0:3]) is None or self.reachabilityTable[row[0:3]][0] > row[3])):
                        self.reachabilityTable[row[0:3]] = (row[3] + self.neighborTable[(sourceIp, sourcePort, sourceMask)],sourceIp,sourcePort,sourceMask)
            finally:
                self.lockNeighbor.release()
                self.lockReach.release()

            if self.send((sourceIp,sourcePort),0,0,0,0,0,1,0,0,"empty") == False:
                # Algo ocurrió en el proceso que no permitió enviar el mensaje correctamente
                pass
        elif type == 1:
            # Entramos en el caso donde lo recibido es un mensaje de datos
            pass





    # Se encarga de construir y enviar el mensaje al nodo que debe
    def send(self, otherAddress,type,data):
        success = False
        # Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # Envía un mensaje codificado
        encryptedMessage = self.bitnator.encrypt(
            addressOrigen=self.address,
            addressDestiny=otherAddress,
            type=type,
            data=data
        )

        try:
            # Tratamos de enviar el mensaje, con la respuesta
            clientSocket.sendto(encryptedMessage, otherAddress)

        except:
            # No hacemo nada

            pass

        # Cerramos la conexión
        clientSocket.close()

        return success





    # Método para borrar un nodo
    def kill(self):
        #Matamos el servidor
        self.alive = False





    # Se encarga de enviar la tabla de alcanzabilidad a los vecinos cada 30 segundos
    def sendReacheabilityTable(self):
        list = []
        while self.alive:
            # Esperamos 30 segundos para enviar la tabla de alcanzabilidad
            try:
                self.waitingQueue.get(timeout=15)
            except:
                # Continuamos con el método
                pass

            # Verificamos que el nodo siga vivo
            if self.alive:
                try:
                    self.lockNeighbor.acquire()
                    self.lockReach.acquire()
                    for neighbourAddress in self.neighborTable:
                        # El primer loop mete dentro de la lista los vecinos cercanos del nodo
                        for neighbourToSend in self.neighborTable:
                            list.append((neighbourToSend[0], neighbourToSend[1], neighbourToSend[2],
                                self.neighborTable[neighbourToSend]))

                        # Este loop se encarga de meter lo que hay en la tabla de alcanzabilidad
                        for reachableNode in self.reachabilityTable:
                            list.append((reachableNode[0],reachableNode[1],reachableNode[2],self.reachabilityTable[reachableNode][0]))

                        if self.send((neighbourAddress[0],neighbourAddress[1]),1,list) == False:
                            # Algo salió mal en el proceso
                            pass
                finally:
                    self.lockNeighbor.release()
                    self.lockReach.release()
                    list = []





    # Se encarga de actualizar una distancia en la lista de los vecinos
    def updateDistance(self):
        try:
            self.lockNeighbor.acquire()
            self.lockReach.acquire()

            self.enlistNeighbours()
            answer = input(self.neighborOptionMessage)

            intAnswer = int(answer)
            if intAnswer > 0 and intAnswer <= len(self.neighborTable):
                neighbourInformation = self.getNeighbour(intAnswer)

                newDistance = input(self.changeDistanceMessage)
                intNewDistance = int(newDistance)

                if intNewDistance > 20 and intNewDistance <= 100:
                    self.reachabilityTable[neighbourInformation] = ( intNewDistance,
                        self.reachabilityTable[neighbourInformation][1],
                        self.reachabilityTable[neighbourInformation][2],
                        self.reachabilityTable[neighbourInformation][3])

                    self.neighborTable[neighbourInformation] = intNewDistance
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            else:
                print(self.warningMessage + answer + self.invalidOptionMessage)
        except:
            print(self.warningMessage + answer + self.invalidOptionMessage)
        finally:
            self.lockNeighbor.release()
            self.lockReach.release()





    # Se encarga de retornar la información con la que se identifica el nodo seleccionado
    def getNeighbour(self,option):
        i = 1
        neighbourInformation = 0

        for neighbour in self.neighborTable:
            if i == option:
                neighbourInformation = neighbour
                break
            else:
                i = i + 1

        return neighbourInformation





    # Imprime una lista con los vecinos del nodo
    def enlistNeighbours(self):
        i = 1

        for neighbour in self.neighborTable:
            print(str(i) + ". (" + neighbour[0] + " , " + str(neighbour[1]) + " , " + str(neighbour[2]) + ") - " + str(
                self.neighborTable[neighbour]))
            i = i + 1






    # Se encarga de imprimir la taba de alcanzabilidad
    def enlitsReachabilityTable(self):
        i = 1
        try:
            self.lockReach.acquire()
            for reachableNode in self.neighborTable:
                print(str(i) + ". (" + reachableNode[0] + " , " + str(reachableNode[1]) + "," + str(
                    reachableNode[2]) + ") - (" + str(self.neighborTable[reachableNode]) + ")")
                i = i + 1

            for reachableNode in self.reachabilityTable:
                print(str(i) + ". (" + reachableNode[0] + " , " + str(reachableNode[1]) + "," + str(
                    reachableNode[2]) + ") - (" + str(
                    self.reachabilityTable[reachableNode][0]) + "," + self.reachabilityTable[reachableNode][1] + "," + str(
                    self.reachabilityTable[reachableNode][2]) + "," + str(self.reachabilityTable[reachableNode][3]) + ")")
                i = i + 1
        finally:
            self.lockReach.release()




    # Menú del nodo UDP
    def nodeUDPMenu(self):
        print(self.greetingMessage)
        while self.alive:
            answer = input(self.optionMessage)

            try:
                intAnswer = int(answer)
                if intAnswer == 1:
                    self.updateDistance()
                elif intAnswer == 2:
                    # Hay que avisarle a los vecinos
                    self.alive = False
                elif intAnswer == 3:
                    self.enlitsReachabilityTable()
                elif intAnswer == 4:
                    self.alive = False
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            except:
                print(self.warningMessage + answer + self.invalidOptionMessage)
