import threading

class Prueba:
    def __init__(self):
        self.lista = []

    def agregarValor(self,valor):
        self.lista.append(valor)

    def imprimirLista(self):
        print("Lista")
        if len(self.lista) is 0:
            print("No tiene nada")
        for dato in self.lista:
            print(dato)


prueba = Prueba()
prueba.imprimirLista()

listener = threading.Thread(name='daemon',target=prueba.agregarValor(1))
listener.setDaemon(True)
listener.start()

listener = threading.Thread(name='daemon',target=prueba.agregarValor(1))
listener.setDaemon(True)
listener.start()

listener = threading.Thread(name='daemon',target=prueba.agregarValor(1))
listener.setDaemon(True)
listener.start()

listener = threading.Thread(name='daemon',target=prueba.agregarValor(1))
listener.setDaemon(True)
listener.start()

listener = threading.Thread(name='daemon',target=prueba.agregarValor(1))
listener.setDaemon(True)
listener.start()

prueba.imprimirLista()




