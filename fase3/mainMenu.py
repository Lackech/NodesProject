from fase3.NodeAwakener import *
from fase3.NeighborServer import  *

if __name__ == '__main__':
    intAnswer = 0
    server = NeighborServer()
    nodeAwakener = NodeAwakener()

    print("Welcome to our nodes creator!!")
    while intAnswer != 5:
        answer = input("Choose one of the following options:\n"
              "\t1. Load predefined \"csv\" files\n"
              "\t2. Load a \"csv\" file with the server's neighbours list\n"
              "\t3. Load a \"csv\" file with the list of nodes to awake\n"
              "\t4. Create a new UDP Node\n"
              "\t5. Exit\n"
              "\tYour answer --> ")

        # Convertimos la respuesta a un int
        intAnswer = 4
        try:
            intAnswer = int(answer)
        except:
            intAnswer = 5

        if intAnswer == 1:
            # Cargamos los datos predefinidos
            server.uploadNeighborsTable("vecinos.csv")
            nodeAwakener.awakeNodesInFile("ListaNodos.csv")

        elif intAnswer == 2:
            # Cargamos el archivo de vecinos seleccionado por el usuario
            neighbours = input("\nWrite the \"csv\" file from where the neighbours will be obtained --> ")
            nodeAwakener.awakeNodesInFile(nodes)

        elif intAnswer == 3:
            # Cargamos el archivo con los nodos que se deben levantar
            nodes = input("\nWrite the \"csv\" file from which the nodes will created --> ")
            server.uploadNeighborsTable(neighbours)

        elif intAnswer == 4:
            # Creamos un nuevo nodo nada mas
            pass





