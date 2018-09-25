from socket import *
TCP_IP = 'localhost'
TCP_PORT = 12000
BUFFER_SIZE = 1024
s = socket(AF_INET, SOCK_STREAM)
sentence = input('Input lowercase sentence:')
s.connect((TCP_IP, TCP_PORT))
s.send(sentence.encode('utf-8'))
data = s.recv(BUFFER_SIZE)
s.close()
print ("received data:", data)
