from fase3.NodeAwakener import *
from fase3.NeighborServer import  *

if __name__ == '__main__':
    intAnswer = 0
    # server = NeighborServer()
    nodeAwakener = NodeAwakener()

    print("Welcome to our nodes creator!!")
    while intAnswer != 4:
        answer = input("Choose one of the following options:\n"
              "\t1. Load predefined \"csv\" files\n"
              "\t2. Load the \"csv\" files of your choice\n"
              "\t3. Create a new UDP Node\n"
              "\t4. Exit\n"
              "\tYour answer --> ")

        # Convertimos la respuesta a un int
        intAnswer = 4
        try:
            intAnswer = int(answer)
        except:
            intAnswer = 4

        if intAnswer == 1:
            # Cargamos los datos predefinidos
            #server.uploadNeighborsTable("vecinos.csv")
            nodeAwakener.awakeNodesInFile("ListaNodos.csv")
        elif intAnswer == 2:
            # Cargamos los datos seleccionados por el usuario
            nodes = input("\nWrite the \"csv\" file from which the nodes will created --> ")
            neighbours = input("\nWrite the \"csv\" file from where the neighbours will be obtained --> ")

            #server.uploadNeighborsTable(neighbours)
            nodeAwakener.awakeNodesInFile(nodes)
        elif intAnswer == 3:
            # Creamos un nuevo nodo nada mas
            pass





