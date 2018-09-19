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
        num = packetMessage.split()[0][:8]
        n = int(num, 2)
        for i in range(0,n):
            num1 = packetMessage[(i*56)+8:(i*56)+8*2]
            n1 = int(num1, 2)
            num2 = packetMessage[(i*56)+8*2:(i*56)+8*3]
            n2 = int(num2, 2)
            num3 = packetMessage[(i*56)+8*3:(i*56)+8*4]
            n3 = int(num3, 2)
            num4 = packetMessage[(i*56)+8*4:(i*56)+8*5]
            n4 = int(num4, 2)

            address = str(n1) + "." + str(n2) + "." + str(n3) + "." +str(n4)

            print(address)

            mask = packetMessage[(i*56)+8*5:(i*56)+8*6]
            maskNum = int(mask,2)

            cost = packetMessage[(i*56)+8*6:(i*56)+8*9]
            costNum = int(cost,2)

            self.saveDataTable(reachabilityTable,address,maskNum,costNum,senderAddress)







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
