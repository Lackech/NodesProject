from fase2.messageGenerator import *
from fase2.nodeUDP import *
from fase2.interface import *
from fase2.router import *

class Application:

    # Application's constructor
    def __init__(self):
        self.interface = Interface()
        self.router = Router()
        self.messageGenerator = MessageGenerator()
        self.node = None

        self.greetingMessage = ("Welcome to our Face 2 application!!"
                                "\tLets proceed and create your UDP node...")

        self.ipMessage = "\tWrite the Node's Ip: "
        self.portMessage = "\tWrite Node's Port: "
        self.mascaraMessage = "\tWrite Node's Mascara: "

        self.warningMessage = "\tWARNING -- \""
        self.invalidIpMessage = "\" -- is not a valid IP"
        self.invalidPortMessage = "\" -- is not a valid Port"
        self.invalidMascaraMessage = "\" -- is not a valid Mascara"
        self.invalidOptionMessage = "\" -- is not a valid Option"
        self.invalidNodeMessage = "\" -- is not reachable in this moment try again later"

        self.nodeOptionMessage = ("Please write the number of the one you want to do:\n"
                            "\t1. Start connection\n"
                            "\t2. Send a trial message\n"
                            "\t3. Close a connection\n"
                            "\t4. Close all connection\n"
                            "\t5. Show the log history\n"
                            "\tWrite your option here --> ")

        self.createConnectionMessage = "Greate!! Lets create this new connection..."
        self.sendTrialMessage = "Ok, lets send a random message"
        self.closeConnectionMessage = "Well, if you want to close a connection, lets do it"
        self.closeConnectionMessage = "Closing all connections..."

        self.listOfConnectionMessage = "Please choose one of the following connections:\n"





    def execute(self):
        self.nodeCreation()
        self.nodeExecution()



    def nodeCreation(self):
        self.interface.showMessage(self.greetingMessage)

        nodeIp,nodePort = self.getNodeInformation()
        self.node = NodeUdp(nodeIp,nodePort)



    def nodeExecution(self):
        while self.node.alive:

            nodeOption = self.interface.getInput(self.nodeOptionMessage)
            while self.isValid(nodeOption, 5) is False:
                self.interface.showMessage(self.warningMessage + nodeOption + self.invalidOptionMessage)
                nodeOption = self.interface.getInput(self.nodeOptionMessage)

            nodeOption = int(nodeOption)
            if nodeOption is 1:
            # El nodo va a iniciar una conexion
                self.interface.showMessage(self.createConnectionMessage)

                otherIp,otherPort = self.getNodeInformation()
                while self.node.startConnection(otherIp,otherPort) is False:
                    self.interface.showMessage(self.warningMessage + "(" + otherIp + "," + str(otherPort) + ")" + self.invalidNodeMessage)
                    otherIp, otherPort = self.getNodeInformation()

            else:
                if nodeOption is 2:
                # El nodo va a enviar un mensaje aleatorio a una de sus conexiones
                    self.interface.showMessage(self.sendTrialMessage)

                    connectingOption = self.interface.getInput(
                        self.listOfConnectionMessage + self.node.getConnectionList)

                    while self.isValid(connectingOption,self.node.numOpenConnections) is False:
                        self.interface.showMessage(self.warningMessage + connectingOption + self.invalidOptionMessage)
                        connectingOption = self.interface.getInput(
                            self.listOfConnectionMessage + self.node.getConnectionList)

                    message = self.messageGenerator.randomMessage()
                    self.node.send(connectingOption,message)

                else:
                    if nodeOption is 3:
                    # El nodo va a cerrar una de sus conexiones
                        self.interface.showMessage(self.closeConnectionMessage)

                        connectingOption = self.interface.getInput(
                            self.listOfConnectionMessage + self.node.getConnectionList)

                        while self.isValid(connectingOption, self.node.numOpenConnections) is False:
                            self.interface.showMessage(self.warningMessage + connectingOption + self.invalidOptionMessage)
                            connectingOption = self.interface.getInput(
                                self.listOfConnectionMessage + self.node.getConnectionList)

                        self.node.closeConnection(connectingOption)

                    else:
                        if nodeOption is 4:
                        # Cierra todas las conexiones
                            self.node.alive = 0
                            self.node.closeAllConnection()

                        else:
                        # Muestra la informacion que hay en el log
                            self.interface.showMessage(self.node.getLogHistory())



    def isValid(self, argument, numberOfOptions):
        valid = True

        try:
            if int(argument) <= 0 and int(argument) > numberOfOptions:
                valid = False
        except:
            valid = False

        return valid



    def optainNodeIp(self):
        nodeIp = ""
        while self.router.validIp(nodeIp)[0] is False:
            nodeIp = self.interface.getInput(self.ipMessage)
            if self.router.validIp(nodeIp)[0] is False:
                self.interface.showMessage(self.warningMessage + nodeIp + self.invalidIpMessage)

        return nodeIp

    def optainNodePort(self):
        nodePort = self.interface.getInput(self.portMessage)
        while self.router.validPort(nodePort) is False:
            self.interface.showMessage(self.warningMessage + nodePort + self.invalidPortMessage)
            nodePort = self.interface.getInput(self.portMessage)

        return int(nodePort)

    def optainNodeMascara(self,tipoRed):
        nodeMascara = -1
        while self.router.validMascara(nodeMascara,tipoRed) is False:
            nodeMascara = self.interface.getInput(self.mascaraMessage)

            if self.router.validMascara(nodeMascara,tipoRed) is False:
                self.interface.showMessage(self.warningMessage + nodeMascara + self.invalidMascaraMessage)

        return int(nodeMascara)

    def getNodeInformation(self):
        nodeIp = self.optainNodeIp()
        nodePort = self.optainNodePort()
        return nodeIp,nodePort



    def optainSendingMessage(self):
        string = "holamundo"
