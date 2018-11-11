from socket import *
from fase3.Node import *
import csv

#

class NodeAwakener(Node):

    # Constructor por omisión
    def __init__(self):
        # Llamamos al constructor del padre, para guardar el address del activador del nodo
        Node.__init__(NODE_AWAKENER_ADDRESS,NODE_AWAKENER_MASCARA)





    # Se encarga de despertar todos los nodos que viene en el archivo que se recibió como parámetro
    def awakeNodesInFile(self,fileName):
        success = True

        # Aquí se va intentar abrir el archivo y comenzar a levantar los nodos, en caso de que haya un
        try:
            fileNameLength = len(fileName)

            # Preguntamos si el nombre es más largo que 4 => ".csv"
            if fileNameLength > 4:
                # Preguntamos si los 4 caracteres finales son los que nos indican que es un archivo tipo ".csv"
                if fileName[fileNameLength-4] == '.' and fileName[fileNameLength-3] == 'c' and fileName[fileNameLength-2] == 's' and fileName[fileNameLength-1] == 'v':
                    with open(fileName) as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            nodeAddress = (row[NODE_IP],row[NODE_PORT])
                            nodeMascara = row[NODE_MASCARA]
                            self.awakeNode(nodeAddress,nodeMascara)
                else:
                    success = False
            else:
                success = False
        except:
            # Quiere decir que en el proceso hubo algún error por lo que no se puedo leer correctamente el archivo
            success = False

        return success





    # Se encarga de levantar un nodo, y verificar si se activó correctamente
    def awakeNode(self,nodeAddress,nodeMascara):
        success = True

        information = self.router.validIp(nodeAddress[0])
        if information[0] == True:
            if self.router.validPort(nodeAddress[1]) and self.router.validMascara(nodeMascara,information[1]):
                # Creamos el nodo
            else:
                success = False
        else:
            success = False

        return success
