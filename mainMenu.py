import os


def menu():
    os.system('cls')

    print("Selecciona una opción")
    print("\t1 - Crear un nodo")
    print("\t2 - Borrar un nodo")
    print("\t3 - Tercera opcion")
    print("\t9 - Salir")


if __name__ == '__main__':

    while True:

        menu()
        opcionMenu = input("Digite su eleccion: ")

        if opcionMenu == "1":
            print("")
            input("Creando un nodo...\npulsa una tecla para continuar")

        elif opcionMenu == "2":
            print("")
            input("Borrando un nodo...\npulsa una tecla para continuar")

        elif opcionMenu == "3":
            print("")
            input("...........\npulsa una tecla para continuar")

        elif opcionMenu == "9":
            break

        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
