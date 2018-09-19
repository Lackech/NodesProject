from nodes.nodeTCP import *
from nodes.nodeUDP import *


def menu():
    os.system('cls')
    print("To create a node you need to write this command:")
    print("\tnode-<X> IP port")
    print("\t<X> can be: pseudoBGP or intAs")
    print("Else write 0 to exit.")


if __name__ == '__main__':

        # sys.exit(1 if sys.byteorder=='big' else 0)



        menu()
        opcionMenu = input("Now choose: ")
        str = opcionMenu.split(" ")
        if str[0] == "node-pseudoBGP":
            serverIp = str[1]
            serverPort = int(str[2])
            node = nodeTCP(serverIp, serverPort)
            print("")
            input("Creating a TCP node\nPress any key to continue")
            node.nodeMenu()


        elif str[0] == "node-intAS":
            str = opcionMenu.split(" ")
            serverIp = str[1]
            serverPort = int(str[2])
            node = nodeUDP(serverIp, serverPort)
            print("")
            input("Create an UDP node\nPress any key to continue")
            node.nodeMenu()

        elif opcionMenu == "0":
            sys.exit()

        else:
            print("")
            input("Its not that hard, just pick the right number\nPress any key to continue")
