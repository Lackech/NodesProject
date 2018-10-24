import threading

def l():
    return "hola"

listener = threading.Thread(name='daemon',target=l)
listener.setDaemon(True)


jaja = listener.start()
print(jaja)




