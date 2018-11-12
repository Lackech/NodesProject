
from fase3 import *
from fase3.NeighborServer import *

if __name__ == '__main__':
    server = NeighborServer('localhost','12000',24)

    server.uploadNeighborsTable('vecinos.csv')



