from nodes.nodeTCP import *


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

        if opcionMenu == "node-pseudoBGP IP port":
            str = opcionMenu.split(" ")
            serverIp = str[1]
            serverPort = int(str[2])
            node = nodeTCP(serverIp, serverPort)
            print("")
            input("Creating a TCP node\nPress any key to continue")
            node.nodeMenu()


        elif opcionMenu == "node-intAS IP port":
            str = opcionMenu.split(" ")
            serverIp = str[1]
            serverPort = int(str[2])
            node = nodeTCP(serverIp, serverPort)
            print("")
            input("Create an UDP node\nPress any key to continue")
            node.nodeMenu()

        elif opcionMenu == "0":
            sys.exit()

        else:
            print("")
            input("Its not that hard, just pick the right number\nPress any key to continue")
