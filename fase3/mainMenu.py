from fase3.NodeAwakener import *
from fase3.NeighborServer import  *

if __name__ == '__main__':

    server = NeighborServer()

    nodeAwakener = NodeAwakener()
    nodeAwakener.awakeNodesInFile("ListaNodos.csv")
