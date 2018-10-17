listaA = []
listaB = []

listaA.append('a')
listaA.append('b')
listaA.append('c')
listaB.append('a')
listaB.append('b')
listaB.append('c')
listaA.extend(listaB)

for i in listaA:
    print(i)




