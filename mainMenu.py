import os
from nodes.nodeTCP import *



def menu():
    os.system('cls')

    print("Our communication system")
    print("\t1 - Create a TCP node")
    print("\t2 - Create a UDP node")
    print("\t9 - Exit")


if __name__ == '__main__':

        menu()
        opcionMenu = input("Pick a number: ")

        if opcionMenu == "1":
            ipNode = input("\nGive me the IP: ")
            portNode = int(input("\nGive me the port: "))
            nodeTCP(ipNode, portNode)
            print("")
            input("Creating a TCP node\nPress any key to continue")

        elif opcionMenu == "2":
            print("")
            input("Create an UDP node\nPress any key to continue")

        elif opcionMenu == "9":
            sys.exit()

        else:
            print("")
            input("Its not that hard, just pick the right number\nPress any key to continue")
