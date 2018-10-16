from fase2.nodeUDP import *
from fase2.interface import *
from fase2.router import *

class Application:

    # Application's constructor
    def __init__(self):
        self.interface = Interface()
        self.router = Router()
        self.node = None

        self.greetingMessage = ("Welcome to our Face 2 application!!"
                                "\tLets proceed and create your UDP node...")

        self.nodeIpMessage = "\tWrite your Node's IP: "

        self.nodePortMessage = "\tWrite your Node's Port: "
        self.nodePortMessage = "\tWrite your Node's Port: "
        self.nodeMascaraMessage = "\tWrite your Node's Mascara: "

        self.connectingPortMessage = "\tWrite the new connection Node's Port: "
        self.connectingPortMessage = "\tWrite new connection Node's Port: "
        self.connectingMascaraMessage = "\tWrite new connection Node's Mascara: "

        self.warningMessage = "\tWARNING -- \""
        self.invalidIpMessage = "\" -- is not a valid IP"
        self.invalidPortMessage = "\" -- is not a valid Port"
        self.invalidMascarMessage = "\" -- is not a valid Mascara"

        self.nodeMessage = ("Please write the number of the one you want to do:\n"
                            "\t1. Send message\n"
                            "\t2. Show table\n"
                            "\t3. Kill node\n"
                            "\t4. Create a catastrophe(Exit)\n"
                            "\tWrite your option here --> ")




    def execute(self):
        self.nodeCreation()
        self.nodeExecution()



    def nodeCreation(self):
        self.interface.showMessage(self.greetingMessage)

        nodeAddress = self.getNodeInformation()
        self.node = NodeUdp(nodeAddress)




    def nodeExecution(self):
        while self.node.alive:
            nodeOption = 0
            while nodeOption is 0:
                nodeOption = self.isValid(self.interface.getInput(self.nodeMessage), ["1", "2", "3", "4"])

                if nodeOption is 0:
                    self.interface.showMessage(self.errorMessage)

            if nodeOption is 1:
            # El nodo va a enviar un mensaje
                messageList = self.optainSendingMessage()
                successful = False

                self.interface.showMessage(self.creatingConnectionMessage)
                while successful is False:
                    otherAddress = self.getNodeInformation()
                    successful = self.node.send(otherAddress, messageList)

                    if successful is False:
                        self.interface.showMessage(self.unsuccessfulConnectionMessage)

            else:
                if nodeOption is 2:
                # El nodo va a mostrar la table de alcanzabilidad
                    for network in self.node.reachabilityTable:
                        print(network, self.node.reachabilityTable[network])

                else:
                    if nodeOption is 3:
                    # El nodo va a morir
                        self.node.kill()

                    else:
                        if nodeOption is 4:
                        # Finaliza todo de golpe
                            self.node.alive = 0



    def isValid(self, argument, posibleOptions):
        valid = 0
        i = 1
        for option in posibleOptions:
            if argument == option:
                valid = i
                break
            i += 1

        return valid



    def optainNodeIp(self):
        nodeIp = ""
        while self.router.validIp(nodeIp)[0] is False:
            nodeIp = self.interface.getInput(self.nodeIpMessage)
            if self.router.validIp(nodeIp)[0] is False:
                self.interface.showMessage(self.errorMessage)

        return nodeIp

    def optainNodePort(self):
        nodePort = -1
        while self.router.validPort(nodePort) is False:
            nodePort = self.interface.getInput(self.nodePortMessage)

            if self.router.validPort(nodePort) is False:
                self.interface.showMessage(self.warningMessage + nodePort + self.invalidPortMessage)

        return nodePort

    def optainNodeMascara(self,tipoRed):
        nodeMascara = -1
        while self.router.validMascara(nodeMascara,tipoRed) is False:
            nodeMascara = self.interface.getInput(self.nodeMascaraMessage)

            if self.router.validMascara(nodeMascara,tipoRed) is False:
                self.interface.showMessage(self.warningMessage + nodeMascara + self.invalidMascaraMessage)

        return int(nodeMascara)

    def getNodeInformation(self):
        nodeIp = self.optainNodeIp()
        nodePort = self.optainNodePort()
        nodeAddress = (nodeIp,nodePort)
        return nodeAddress



    def optainSendingMessage(self):
        string = "holamundo"
