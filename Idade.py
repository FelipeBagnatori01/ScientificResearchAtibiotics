import numpy as np
lista = []

for i in range(0, 10):
    aux = []
    for j in range(0, 10):
        aux.append(str(i) + " " + str(j))
    lista.append(aux)
print(np.array(lista))