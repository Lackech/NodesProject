from socket import *
from fase3.Node import *
import queue
from time import sleep
import time

MAX_SIZE = 10

class NodeUDP(Node):

    def __init__(self,address,mascara):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(self,address, mascara) # Ver como manejamos las direcciones aca

        # Candados
        self.lockReach = threading.Lock()
        self.lockLog = threading.Lock()
        self.lockNeighbor = threading.Lock()
        self.lockSaluto = threading.Lock()

        self.waitingQueue = queue.Queue(1)
        self.packetsQueue = queue.Queue(MAX_SIZE)

        # Tablas
        self.reachabilityTable = {}
        self.neighborTable = {}
        self.salutoTable = {}
        self.salutoCont = {}

        # Variabes que sirven para comunicarse con el usuario
        self.greetingMessage = "Welcome to the Node UDP...\n\n"
        self.MrMeeseeks = "Im "
        self.optionMessage = ("Please select one of the following options:\n"
                              "\t1. Change a link's distance\n"
                              "\t2. Send a message\n"
                              "\t3. Kill myself\n"
                              "\t4. Print reachability table\n"
                              "\t5. Print neighbour table\n"
                              "\t6. Exit\n"
                              "\tYour answer --> ")

        self.neighborOptionMessage = "Please write the number of the Node to modify --> "
        self.changeDistanceMessage = "Please write the new distance --> "

        self.reachableNodeOptionMessage = "Please write the number of the Node to whom you want to send a message --> "
        self.writeMessageMessage = "Please write the message you want to send to the other Node --> "
        self.recievedMessageMessage = "\n\nYou recieved the following message --> "

        # Creamos el socket servido del nodo
        self.socketServer = socket(AF_INET, SOCK_DGRAM)
        self.socketServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketServer.bind(self.address)

        self.listener = threading.Thread(name='daemon', target=self.listen)
        self.listener.setDaemon(True)
        self.listener.start()

        sleep(1)

        thread_hello = threading.Thread(name='Saludador', target=self.helloThere)
        thread_hello.daemon = True
        thread_hello.start()


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


    # Metodillo para manejar catastrofes
    def helloThere(self):
        while self.alive is True:
            self.lockNeighbor.acquire()

            for neighborKey, neighborValue in self.neighborTable.items():
                self.lockSaluto.acquire()
                self.salutoTable[neighborKey] = False
                self.lockSaluto.release()
                thread_saluto = threading.Thread(target= self.waazzzuuuupp, args=(neighborKey,neighborValue))
                thread_saluto.daemon = True
                thread_saluto.start()
            self.lockNeighbor.release()
            sleep(TIMEOUT_SALUTO)






    def waazzzuuuupp(self, neighborKey, neighborValue):

        for i in range(0,5):
            if self.salutoTable[neighborKey] is False:
                encryptedPacket = self.bitnator.encryptTypePacket(ALIVE)
                self.send(neighborKey, encryptedPacket)
                sleep(0.5)

        if self.salutoTable[neighborKey] is False and self.neighborTable[neighborKey][POS_DESPIERTO_VEC]:
            print("Catastrofe!!!!")
            self.lockReach.acquire()
            self.lockNeighbor.acquire()
            # Guardar primero que el vecino no esta activo en la tabla de vecinos
            self.neighborTable[neighborKey] = (neighborValue[0],neighborValue[1],False)
            # Resetear la tabla que se tiene y avisar a los vecinos que alguien se murio
            self.resetTable()
            self.sendFlooding(HOPS)
            self.lockNeighbor.release()
            self.lockReach.release()







    # Se encarga de analizar los paquetes que solo tienen un dato
    def analyzeMessage(self):
        stabilizationCounter = 0

        while self.alive:
            information = self.packetsQueue.get()
            decrytedMessage = information[0]
            clientAddress = information[1]

            if decrytedMessage[TYPE] == ACTUALIZATION:

                if stabilizationCounter == 0 or stabilizationCounter[1] == 3:
                    try:
                        self.lockReach.acquire()
                        self.lockNeighbor.acquire()

                        for i in range(0, decrytedMessage[N_ACT]):
                            # Guardamos el nodo en la tabla de alcanzabilidad
                            if self.reachabilityTable.get(decrytedMessage[REACHEABILITY_TABLE][i][0:2]) is None or self.reachabilityTable[decrytedMessage[REACHEABILITY_TABLE][i][0:2]][0] > decrytedMessage[REACHEABILITY_TABLE][i][3] + self.neighborTable[clientAddress][1]:
                                #print("Despues del if")

                                self.reachabilityTable[decrytedMessage[REACHEABILITY_TABLE][i][0:2]] = (
                                    decrytedMessage[REACHEABILITY_TABLE][i][3] + self.neighborTable[clientAddress][1],
                                    decrytedMessage[REACHEABILITY_TABLE][i][2],clientAddress[IP],clientAddress[PORT])

                    finally:
                        stabilizationCounter = 0
                        self.lockNeighbor.release()
                        self.lockReach.release()

                elif stabilizationCounter != 0:
                    if stabilizationCounter[0] == clientAddress:
                        stabilizationCounter = (clientAddress,stabilizationCounter[1]+1)


            elif decrytedMessage[TYPE] == ALIVE or decrytedMessage[TYPE] == YES_ALIVE:
                # Un nodo vecino nos confirmó que sí está vivo
                self.neighborTable[clientAddress] = (
                self.neighborTable[clientAddress][0], self.neighborTable[clientAddress][1], True)

                # Lo guardamos en la tabla de alcanzabilidad
                self.reachabilityTable[clientAddress] = (
                    self.neighborTable[clientAddress][1], self.neighborTable[clientAddress][0], clientAddress[IP], clientAddress[PORT])

                if decrytedMessage[TYPE] == ALIVE:
                    # Le contestamos al nodo que nos envío el paquete con una confirmación
                    encryptedPaket = self.bitnator.encryptTypePacket(YES_ALIVE)
                    self.send(clientAddress, encryptedPaket)
                else:
                    self.lockSaluto.acquire()
                    self.salutoTable[clientAddress] = True
                    self.lockSaluto.release()



            elif decrytedMessage[TYPE] == FLOODING:
                # Comenzamos con el proceso de estabilizacion
                stabilizationCounter = (self.getFirstAliveNode(),0)

                #Se nesecita esperar a que termine cualquier actualizacion y luego bloquear las entrantes
                self.lockNeighbor.acquire()
                self.lockReach.acquire()
                self.resetTable()
                self.lockReach.release()
                self.lockNeighbor.release()

                self.sendFlooding(decrytedMessage[JUMPS])

            elif decrytedMessage[TYPE] == DATA:
                # Preguntamos por el destino del paquete
                if self.address[IP] == decrytedMessage[DESTINY_IP] and self.address[PORT] == decrytedMessage[DESTINY_PORT]:
                    # El paquete es para este nodo
                    print(self.recievedMessageMessage + decrytedMessage[MESSAGE] + '\n')
                else:
                    # El paquete debe seguir su trayectoria
                    encryptedPacket = self.bitnator.encryptDataPacket((decrytedMessage[ORIGIN_IP],decrytedMessage[ORIGIN_PORT]),(decrytedMessage[DESTINY_IP],decrytedMessage[DESTINY_PORT]),decrytedMessage[N_DATA],decrytedMessage[MESSAGE])

                    # Obtenemos el vecino por el que se llega a ese nodo
                    reachableNodeKey = (decrytedMessage[DESTINY_IP],decrytedMessage[DESTINY_PORT])
                    routeNeighbour = (self.reachabilityTable[reachableNodeKey][2],
                                      self.reachabilityTable[reachableNodeKey][3])

                    self.send(routeNeighbour,encryptedPacket)


            elif decrytedMessage[TYPE] == COST:
                # Vemos si el costo es menor o no, pues depende de esto si hacemos flooding o no
                if decrytedMessage[PRICE] < self.neighborTable[clientAddress][1]:
                    # El costo es menor por lo tanto no hay problema
                    self.neighborTable[clientAddress] = (
                        self.neighborTable[clientAddress][0], decrytedMessage[PRICE], True)

                    # Lo cambiamos en la tabla de alcanzabilidad
                    self.reachabilityTable[clientAddress] = (decrytedMessage[PRICE],self.neighborTable[clientAddress][0],clientAddress[IP],clientAddress[PORT])
                else:
                    # Comenzamos con el proceso de estabilizacion
                    stabilizationCounter = (self.getFirstAliveNode(), 0)

                    self.neighborTable[clientAddress] = (
                        self.neighborTable[clientAddress][0], decrytedMessage[PRICE], True)
                    # EL costo es mayor por lo tanto tenemos que realizar inundación #REvisar
                    self.lockNeighbor.acquire()
                    self.lockReach.acquire()
                    self.resetTable()
                    self.lockReach.release()
                    self.lockNeighbor.release()

                    self.sendFlooding(HOPS)


            elif decrytedMessage[TYPE] == DEATH:
                # Hacemos que el vecino este en modo muerto
                self.neighborTable[clientAddress] = (
                    self.neighborTable[clientAddress][0], self.neighborTable[clientAddress][1], False)

                # Comenzamos con el proceso de estabilizacion
                stabilizationCounter = (self.getFirstAliveNode(), 0)

                # Lo eliminamos de la tabla de alcanzabilidad
                self.reachabilityTable.pop(clientAddress)

                # Realizamos la inundación #Revisar
                self.lockNeighbor.acquire()
                self.lockReach.acquire()
                self.resetTable()
                self.lockReach.release()
                self.lockNeighbor.release()

                self.sendFlooding(HOPS)


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

                for neighborKey, neighborValue in self.neighborTable.items():
                    self.lockSaluto.acquire()
                    self.salutoCont[neighborKey] = 5
                    self.lockSaluto.release()






    # Se encarga de construir y enviar el mensaje al nodo que debe
    def send(self, otherAddress,encryptedPaket):
        # Tratamos de enviar el mensaje, con la respuesta
        self.socketServer.sendto(encryptedPaket, otherAddress)





    def sendFlooding(self, hops):

        if hops - 1 > 0:
            next_hops = hops - 1

            for vecino in self.neighborTable.keys():
                encryptedPaket = self.bitnator.encryptInundationPacket(next_hops)
                self.send((vecino[0],vecino[1]), encryptedPaket)






    def resetTable(self):

        del self.reachabilityTable
        self.reachabilityTable = {}
        # Agrego a los vecinos

        for neighborKey, neighborValue in self.neighborTable.items():
            if neighborValue[POS_DESPIERTO_VEC]:
                self.reachabilityTable[neighborKey] = (neighborValue[1],neighborValue[0], neighborKey[0],neighborKey[1])





    # Método para borrar un nodo
    def kill(self):
        # Enviamos el mensaje a los nodos vecinos
        for neighbour in self.neighborTable:
            if self.neighborTable[neighbour][2] == True:
                encryptedPacket = self.bitnator.encryptTypePacket(DEATH)
                self.send(neighbour,encryptedPacket)

        # Apagamos el servidor
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
                    self.lockReach.acquire()
                    self.lockNeighbor.acquire()

                    for neighbourAddress in self.neighborTable:
                        # Este loop se encarga de meter lo que hay en la tabla de alcanzabilidad
                        for reachableNode in self.reachabilityTable:
                            if reachableNode != neighbourAddress:
                                list.append((reachableNode[0],reachableNode[1],self.reachabilityTable[reachableNode][1],self.reachabilityTable[reachableNode][0]))

                        encryptedPacket = self.bitnator.encryptActualizationPacket(len(list),list)
                        self.send(neighbourAddress,encryptedPacket)

                        list = []
                finally:
                    self.lockNeighbor.release()
                    self.lockReach.release()





    # Se encarga de actualizar una distancia en la lista de los vecinos
    def updateDistance(self):
        try:
            self.lockReach.acquire()
            self.lockNeighbor.acquire()

            self.enlistNeighbours()
            answer = input(self.neighborOptionMessage)

            intAnswer = int(answer)
            if intAnswer > 0 and intAnswer <= len(self.neighborTable):
                neighbourInformation = self.getNeighbour(intAnswer)

                newDistance = input(self.changeDistanceMessage)
                intNewDistance = int(newDistance)

                if intNewDistance >= 20 and intNewDistance <= 100:

                    # Cambiamos la información en la tabla de vecinos
                    self.neighborTable[neighbourInformation] = (
                    self.neighborTable[neighbourInformation][0], intNewDistance,
                    self.neighborTable[neighbourInformation][2])

                    # Vemos sí es necesario cambiar la información en la tabla de alcanzabilidad
                    if self.reachabilityTable[neighbourInformation][2] == neighbourInformation[IP] and self.reachabilityTable[neighbourInformation][3] == neighbourInformation[PORT]:
                        self.reachabilityTable[neighbourInformation] = (intNewDistance,
                            self.neighborTable[neighbourInformation][0],neighbourInformation[IP], neighbourInformation[PORT])

                    # Enviamos el mensaje de cambio de costo
                    encryptedPacket = self.bitnator.encryptCostPacket(intNewDistance)
                    self.send(neighbourInformation,encryptedPacket)

                else:
                    pass
            else:
                pass
        except:
            pass
        finally:
            self.lockNeighbor.release()
            self.lockReach.release()





    # Se encarga de enviar un mensaje con datos a uno de los vecinos que está en la tabla de alcanzabilidad
    def sendData(self):
        try:
            self.lockReach.acquire()
            self.lockNeighbor.acquire()

            self.enlitsReachabilityTable()
            answer = input(self.reachableNodeOptionMessage)

            intAnswer = int(answer)
            if intAnswer > 0 and intAnswer <= len(self.reachabilityTable):

                # Obtenemos la informacion necesaria para enviar el mensaje
                reachableNodeInformation = self.getReachableNode(intAnswer)
                routeNeighbour = (self.reachabilityTable[reachableNodeInformation][2],self.reachabilityTable[reachableNodeInformation][3])

                # Le pedimos el mensaje al usuario
                message = input(self.writeMessageMessage)

                encryptedPacket = self.bitnator.encryptDataPacket(self.address,reachableNodeInformation,len(message),message)
                self.send(routeNeighbour,encryptedPacket)

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
            if self.neighborTable[neighbour][2] == True:
                print(str(i) + "." , neighbour)
            i = i + 1





    # Imprime una lista con los vecinos del nodo
    def enlistNeighboursExtended(self):
        i = 1

        for neighbour in self.neighborTable:
            if self.neighborTable[neighbour][2] == True:
                print(str(i) + ".", neighbour,"-",self.neighborTable[neighbour])
            i = i + 1





    # Me devulve el primer nodo que este vivo en la tabla de vecinos
    def getFirstAliveNode(self):
        neighbourInformation = 0
        for neighbour in self.neighborTable:
            if self.neighborTable[neighbour][2] == True:
                neighbourInformation = neighbour

        return neighbourInformation





    # Retorna el nodo seleccionado de la tabla de alcanzabilidad
    def getReachableNode(self,option):
        i = 1
        reachableNodeInformation = 0

        for reachableNode in self.reachabilityTable:
            if i == option:
                reachableNodeInformation = reachableNode
                break
            else:
                i = i + 1

        return reachableNodeInformation





    # Se encarga de imprimir la taba de alcanzabilidad
    def enlitsReachabilityTable(self):
        i = 1

        for reachableNode in self.reachabilityTable:
            print(str(i) + ".", reachableNode)
            i = i + 1





    # Se encarga de imprimir la taba de alcanzabilidad
    def enlitsReachabilityTableExtended(self):
        i = 1

        for reachableNode in self.reachabilityTable:
            print(str(i) + "." , reachableNode , "-" , self.reachabilityTable[reachableNode])
            i = i + 1





    # Menú del nodo UDP
    def nodeUDPMenu(self):
        print(self.greetingMessage + "I am " ,self.address)
        while self.alive:
            try:
                answer = input(self.optionMessage)

                intAnswer = int(answer)
                if intAnswer == 1:
                    self.updateDistance()
                elif intAnswer == 2:
                    self.sendData()
                elif intAnswer == 3:
                    # Hay que avisarle a los vecinos
                    self.kill()
                elif intAnswer == 4:
                    self.enlitsReachabilityTableExtended()
                elif intAnswer == 5:
                    self.enlistNeighboursExtended()
                elif intAnswer == 6:
                    self.alive = False
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            except:
                pass


    def writeLog(self,IP_ORIGEN,PUERTO_ORIGEN,ACCION, lock):
        lock.acquire()
        file = open("log.txt","a+")
        file.write(str(IP_ORIGEN) + "--" + str(PUERTO_ORIGEN) + "--" + str(ACCION) + "\n")
        file.close()
        lock.release()
