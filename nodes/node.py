import os
import sys

class Node:

    #Constructor de la clase nodo
    def __init__(self, serverIp, serverPort):
        self.serverIp = serverIp
        self.serverPort = serverPort

    def listen(self):
        #Debe ser sobreescrito por el método del nodo hijo
        pass

    def send(self):
        # Debe ser sobreescrito por el método del nodo hijo
        pass

    #Método para borrar un nodo
    def kill(self):
        self.alive = False
        pass

    def saveDataTable(self, reachabilityTable, address, mask, cost, senderAddress):
        key = (address, mask)
        value = (cost, senderAddress)
        d1 = {key: value}
        if reachabilityTable.get(key) != None:
            row = reachabilityTable.get(key)
            if row[0] > cost:
                reachabilityTable.update(d1)
                print("Data updated")
        else:
            reachabilityTable.update(d1)
            print("Data inserted")

    def decrypt(self, packetMessage, reachabilityTable, senderAddress):
        pass
    
    #Método para codificar mensaje
    def encode(self):
        numberOfElements = int(input("Select the number of elements:"))
        bytestring = '{0:016b}'.format(numberOfElements)

        for i in range(0,numberOfElements):
            ipAdress = input("Write the Ip adress:")
            stringIp = ipAdress.split('.')
            for s in stringIp:
                bytestring += '{0:08b}'.format(int(s))

            bytestring += '{0:08b}'.format(int(input("Write the Mascara adress:")))
            bytestring += '{0:024b}'.format(int(input("Write the Cost:")))

        return bytestring

    def menu(self):
        os.system('cls')
        print("What you gonna do????")
        print("\t1 - Say something to some bruhh")
        print("\t2 - Kill myself")
        print("\t3 - Just give a sh#$t and go away")

    def nodeMenu(self):
        while self.alive:
            self.menu()
            opcionMenu = int(input("Pick a number: "))

            if opcionMenu == 1:

                self.send()
                print("")
                input("Sending a message...\nPress any key to continue")

            elif opcionMenu == 2:
                self.kill()
                print("")
                input("Shit, dying was forever...\nPress any key to continue")

            elif opcionMenu == 3:
                sys.exit()
                self.alive = False
                break

            else:
                print("")
                input("Its not that hard, just pick the right number\nPress any key to continue")

