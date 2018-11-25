from socket import *
from fase3.Node import *
import queue

MAX_SIZE = 10

class NodeUDP(Node):

    def __init__(self,address,mascara):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,address, mascara) # Ver como manejamos las direcciones aca

        # Candados
        self.lockReach = threading.Lock()
        self.lockLog = threading.Lock()
        self.lockNeighbor = threading.Lock()

        self.waitingQueue = queue.Queue(1)
        self.packetsQueue = queue.Queue(MAX_SIZE)

        # Tablas
        self.reachabilityTable = {}
        self.neighborTable = {}

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

        # Creamos el socket servido del nodo
        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketServer.bind(self.address)

        self.listener = threading.Thread(name='daemon', target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()

        self.listener = threading.Thread(name='daemon', target=self.analyzeMessage)
        self.listener.setDaemon(True)
        self.listener.start()

        # Creamos el hilo que se va a encargar de enviar la tabla cada 30 segundos
        thread = threading.Thread(name='Analizador', target=self.sendReacheabilityTable)
        thread.setDaemon(True)
        thread.start()

        self.nodeUDPMenu()





    # Metodo que se encarga de recibir todos los mensajes que le llegan al nodo
    def listen(self):
        self.send(NEIGHBOR_SERVER_ADDRESS,self.bitnator.encryptTypePacket(SERVER))

        while self.alive:
            # Recibimos el paquete
            try:
                packetMessage, clientAddress = self.socketServer.recvfrom(2048)

                # Desencrptamos el paquete
                decrytedMessage = self.bitnator.decryptPacket(packetMessage)
                self.packetsQueue.put_nowait((decrytedMessage,clientAddress))
            except:
                pass

        self.socketServer.close()





    # Se encarga de analizar los paquetes que solo tienen un dato
    def analyzeMessage(self):
        while self.alive:
            information = self.packetsQueue.get()
            decrytedMessage = information[0]
            clientAddress = information[1]

            if decrytedMessage[TYPE] == ACTUALIZATION:
                try:
                    self.lockReach.acquire()
                    self.lockNeighbor.acquire()

                    for i in range(0, decrytedMessage[N_ACT]):
                        # Guardamos el nodo en la tabla de alcanzabilidad
                        if self.reachabilityTable.get(decrytedMessage[REACHEABILITY_TABLE][i][0:3]) is None or self.reachabilityTable[decrytedMessage[REACHEABILITY_TABLE][i][0:3]][0] > decrytedMessage[REACHEABILITY_TABLE][i][3] + self.neighborTable[clientAddress][1]:
                            self.reachabilityTable[decrytedMessage[REACHEABILITY_TABLE][i][0:3]] = (
                                decrytedMessage[REACHEABILITY_TABLE][i][3] + self.neighborTable[clientAddress][1],
                                clientAddress[IP],clientAddress[PORT])

                finally:
                    self.lockNeighbor.release()
                    self.lockReach.release()


            elif decrytedMessage[TYPE] == ALIVE or decrytedMessage[TYPE] == YES_ALIVE:
                # Un nodo vecino nos confirmó que sí está vivo
                self.neighborTable[clientAddress] = (
                self.neighborTable[clientAddress][0], self.neighborTable[clientAddress][1], True)

                # Lo guardamos en la tabla de alcanzabilidad
                self.reachabilityTable[clientAddress[IP], clientAddress[PORT], self.neighborTable[clientAddress][0]] = (
                    self.neighborTable[clientAddress][1], clientAddress[IP], clientAddress[PORT])

                if decrytedMessage[TYPE] == ALIVE:
                    # Le contestamos al nodo que nos envío el paquete con una confirmación
                    encryptedPaket = self.bitnator.encryptTypePacket(YES_ALIVE)
                    self.send(clientAddress, encryptedPaket)


            elif decrytedMessage[TYPE] == FLOODING:
                pass


            elif decrytedMessage[TYPE] == DATA:
                pass


            elif decrytedMessage[TYPE] == COST:
                pass


            elif decrytedMessage[TYPE] == DEATH:
                pass


            elif decrytedMessage[TYPE] == DISPATCHER:
                # Le contestamos al dispatcher que el nodo sí se levantó correctamente
                encryptedPaket = self.bitnator.encryptTypePacket(DISPATCHER)
                self.send(clientAddress, encryptedPaket)


            elif decrytedMessage[TYPE] == NEIGHBOURS:
                for i in range(0,decrytedMessage[N_ACT]):
                    # Guardamos el vecino en la tabla
                    self.neighborTable[decrytedMessage[REACHEABILITY_TABLE][i][0:2]] = (decrytedMessage[REACHEABILITY_TABLE][i][2],decrytedMessage[REACHEABILITY_TABLE][i][3],False)

                    # Preguntamos sí el vecino está vivo
                    encryptedPacket = self.bitnator.encryptTypePacket(ALIVE)
                    self.send(decrytedMessage[REACHEABILITY_TABLE][i][0:2],encryptedPacket)






    # Se encarga de construir y enviar el mensaje al nodo que debe
    def send(self, otherAddress,encryptedPaket):
        # Tratamos de enviar el mensaje, con la respuesta
        self.socketServer.sendto(encryptedPaket, otherAddress)






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
                self.waitingQueue.get(timeout=5)
            except:
                # Continuamos con el método
                pass

            # Verificamos que el nodo siga vivo
            if self.alive:
                try:
                    self.lockNeighbor.acquire()
                    self.lockReach.acquire()
                    for neighbourAddress in self.neighborTable:
                        # Este loop se encarga de meter lo que hay en la tabla de alcanzabilidad
                        for reachableNode in self.reachabilityTable:
                            if reachableNode[0] != neighbourAddress[IP] or reachableNode[1] != neighbourAddress[PORT]:
                                list.append((reachableNode[0],reachableNode[1],reachableNode[2],self.reachabilityTable[reachableNode][0]))

                        encryptedPacket = self.bitnator.encryptActualizationPacket(len(list),list)
                        self.send(neighbourAddress,encryptedPacket)
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
                    self.reachabilityTable[neighbourInformation] = (intNewDistance,
                        self.reachabilityTable[neighbourInformation][1],
                        self.reachabilityTable[neighbourInformation][2])

                    self.neighborTable[neighbourInformation] = (self.neighborTable[neighbourInformation][0],intNewDistance,self.neighborTable[neighbourInformation][2])
                else:
                    pass
            else:
                pass
        except:
            pass
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
            print(str(i) + ". (" + neighbour[0] + " , " + str(neighbour[1]) + ")")
            i = i + 1





    # Se encarga de imprimir la taba de alcanzabilidad
    def enlitsReachabilityTable(self):
        i = 1
        try:
            self.lockReach.acquire()
            for reachableNode in self.reachabilityTable:
                print(str(i) + ". (" + reachableNode[0] + " , " + str(reachableNode[1]) + "," + str(
                    reachableNode[2]) + ") - (" + str(
                    self.reachabilityTable[reachableNode][0]) + "," + self.reachabilityTable[reachableNode][1] + "," + str(
                    self.reachabilityTable[reachableNode][2]) + ")")
                i = i + 1
        finally:
            self.lockReach.release()




    # Menú del nodo UDP
    def nodeUDPMenu(self):
        print(self.greetingMessage)
        while self.alive:
            try:
                answer = input(self.optionMessage)

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
                pass
