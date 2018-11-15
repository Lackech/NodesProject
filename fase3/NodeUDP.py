from socket import *
from fase3.Node import *

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





    # Se encarga de analizar el paquete y dependiendo de las banderas que vienen activadas varía lo que hace
    def analysMessage(self,sourceIp,sourcePort,ps,rs,sa,saAck,act,actAck,type,tv,data):
        # Ve cuales son las banderas que están activadas, y dependiendo de esto hace algo diferente
        if rs == 1:
            # Entramos en el caso de que el servidor le haya devuelto una respuesta con la información de los vecinos
            pass
        elif sa == 1:
            # Entramos en el caso donde el despachador esta verificando sí el nodo está despierto o no
            if self.send((sourceIp,sourcePort),0,0,0,1,0,0,0,0,"empty") == False:
                # Algo ocurrió en el proceso que no permitió enviar el mensaje correctamente
                pass
        elif act == 1:
            # Entramos en el caso donde el mensaje recibido es una actualización de la tabla de alcanzabilidad
            pass
        elif type == 1:
            # Entramos en el caso donde lo recibido es un mensaje de datos
            pass





    # Se encarga de construir y enviar el mensaje al nodo que debe
    def send(self, otherAddress, ps, rs, sa, saAck, act, actAck, type, tv, data):
        success = False
        # Crea la conexión con el servidor
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # Envía un mensaje codificado
        encryptedMessage = self.bitnator.encrypt(
            addressOrigen=self.address,
            ps=ps,
            rs=rs,
            sa=sa,
            saAck=saAck,
            act=act,
            actAck=actAck,
            type=type,
            tv=tv,
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





    # Se encarga de actualizar una distancia en la lista de los vecinos
    def updateDistance(self):
        self.enlistNeighbours()
        answer = input(self.neighborOptionMessage)

        try:
            intAnswer = int(answer)
            if intAnswer > 0 and intAnswer <= len(self.neighborTable):
                neighbourInformation = self.getNeighbour(intAnswer)

                newDistance = input(self.changeDistanceMessage)
                intNewDistance = int(newDistance)

                if intNewDistance > 20 and intNewDistance <= 100:
                    self.reachabilityTable[neighbourInformation] = intNewDistance
                    self.neighborTable[neighbourInformation] = intNewDistance
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            else:
                print(self.warningMessage + answer + self.invalidOptionMessage)
        except:
            print(self.warningMessage + answer + self.invalidOptionMessage)





    # Se encarga de retornar la información con la que se identifica el nodo seleccionado
    def getNeighbour(self,option):
        i = 1
        neighbourInformation = 0
        for neighbour in self.neighborTable:
            if i == option:
                neighbourInformation = neighbour
                break

        return neighbourInformation





    # Imprime una lista con los vecinos del nodo
    def enlistNeighbours(self):
        i = 1
        for neighbour in self.neighborTable:
            print(str(i) + ". (" + neighbour[0][IP] + " , " + str(neighbour[0][PORT]) + ") - " + str(neighbour[1]))
            ++i





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
                    self.enlistNeighbours()
                elif intAnswer == 4:
                    self.alive = False
                else:
                    print(self.warningMessage + answer + self.invalidOptionMessage)
            except:
                print(self.warningMessage + answer + self.invalidOptionMessage)
