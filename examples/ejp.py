from os import *
import sys
'''
s = bytearray()
for i in range(0,15):
    s += i.to_bytes(1,'big')
    print(len(s))

print(s)

for i in range(0,15):
    print(s.pop())
'''




if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("First time")
        system("start python ejp.py 1 2 3")
    else:
        print(sys.argv)
        while True:
            pass

