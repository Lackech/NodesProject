
from fase3 import *
from fase3.NeighborServer import *
from fase3.Node import *
from fase3.NodeUDP import *
from fase3.NodeAwakener import *

if __name__ == '__main__':


    server = NeighborServer()

    NodeUDP(('127.0.0.1',45000),24)

    server.uploadNeighborsTable('vecinos.csv')



