from nodes.nodeTCP import *
from nodes.nodeUDP import *
from nodes.interface import *
from nodes.router import *

class Application:

    # Application's constructor
    def __init__(self):
        self.interface = Interface()
        self.router = Router()
        self.node = None

        self.mainMessage = "Please choose a type of connection:\n "

        self.connectionTypeMessage = "\tWrite pseudoBGP(TCP) or intAS(UDP):\n"
        self.TcpMessage = "Great!! You choosed to create a TCP node\n"
        self.UdpMessage = "Interesting...You choosed to create a UDP node\n"

        self.nodeIpMessage = "\tWrite the Node's IP:\n"
        self.nodePortMessage = "\tWrite the Node's Port:\n"
        self.nodeMascaraMessage = "\tWrite the Node's Mascara:\n"

        self.nodeMessage = ("Please write the number of the one you want to do:\n"
                            "\t1. Send message\n"
                            "\t2. Show table\n"
                            "\t3. Kill node\n"
                            "\t4. Create a catastrophe(Exit)\n")

        self.errorMessage = "WARNING -- Be sure to choose a valid option"



    def execute(self):
        self.nodesCreation()
        self.nodeExecution()



    def nodeCreation(self):
        self.interface.showMessage(self.mainMessage)
        nodeType = 0

        while nodeType is 0:
            nodeType = self.isValid(self.interface.getInput(self.connectionTypeMessage), ["pseudoBGP", "intAS"])

            if nodeType is 0:
                self.interface.showMessage(self.errorMessage)

        if nodeType is 1:
            self.interface.showMessage(self.TcpMessage)
            nodeAddress = self.getNodeInformation()
            self.node = NodeTcp(nodeAddress)

        else:
            if nodeType is 2:
                self.interface.showMessage(self.UdpMessage)
                nodeAddress = self.getNodeInformation()
                self.node = NodeUdp(nodeAddress)



    def nodeExecution(self):
        while self.node.alive:
            nodeOption = 0
            while nodeOption is 0:
                nodeOption = self.isValid(self.interface.getInput(self.connectionTypeMessage), ["1", "2", "3", "4", "5"])

                if nodeOption is 0:
                    self.interface.showMessage(self.errorMessage)

            if nodeOption is 1:

            else:
                if nodeOption is 2:

                else:
                    if nodeOption is 3:

                    else:
                        if nodeOption is 4:







    def isValid(self, argument, posibleOptions):
        valid = 0
        i = 1
        for option in posibleOptions:
            if argument is option:
                valid = i
                break
            ++i

        return valid



    def getNodeInformation(self):
        nodeIp = ""
        while self.router.validIp(nodeIp) is False:
            nodeIp = self.interface.getInput(self.nodeIpMessage)
            if self.router.validIp(nodeIp) is False:
                self.interface.showMessage(self.errorMessage)

        nodePort = -1
        while self.router.validPort(nodePort) is False:
            nodePort = self.interface.getInput(self.nodeIpMessage)
            if self.router.validIp(nodePort) is False:
                self.interface.showMessage(self.errorMessage)

        return (nodeIp,nodePort)
