#print("ola")
#m1 = [0,0,0,0,0,0,0]
#m2 = [0,0,0,0,0,0,0]
#m3 = [0,0,0,0,0,0,0]
#m4 = [0,0,0,0,0,0,0]
#m5 = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
#print(m5)

#print(m2)
#print(m3)
#print(m4)

#print(len(m1))
#x=0
#for j in range(len(m1)):
    #x =x+1
    #print(j)

Matriz = []

#almacenar valores a mi matriz
for fila in range(4):
    matrizAux = []
    for columna in range(1,8):
        #matrizAux.append(columna)
        matrizAux.append(0)
    Matriz.append(matrizAux)

#recorrer la matriz
for fila in range(4):
    for columna in range(7):
        print(Matriz[fila][columna],end=" ")
    print()


