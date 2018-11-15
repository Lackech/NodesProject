from fase3.NodeUDP import *
import sys

if __name__ == '__main__':
    nodeUDP = NodeUDP((sys.argv[1],int(sys.argv[2])),int(sys.argv[3]))