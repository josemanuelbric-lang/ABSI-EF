def generar_triangulo_pascal(N: int) -> list[list[int]]:
    triangulo_pascal: list[list[int]] = []
    if N >= 0:
        triangulo_pascal.append([1])
    for i in range(1, N + 1):
        fila_anterior = triangulo_pascal[-1]
        nueva_fila = [1]
        for j in range(1, i):
            valor = fila_anterior[j - 1] + fila_anterior[j]
            nueva_fila.append(valor)
        nueva_fila.append(1)
        triangulo_pascal.append(nueva_fila)
    return triangulo_pascal

def generar_triangulo_pascal_multiplicado(Nlist: list[list[int]]) -> list[list[int]]:
    triangulo_multiplicado: list[list[int]] = []
    for i in range(len(Nlist)): 
        fila_original = Nlist[i]
        fila_multiplicada = []
        for j in range(len(fila_original)):
            valor_multiplicado = (6*i)-2*fila_original[j]
            fila_multiplicada.append(valor_multiplicado)
        triangulo_multiplicado.append(fila_multiplicada)
    return triangulo_multiplicado

N_MAX = 20
z1 = generar_triangulo_pascal(N_MAX)
z2 = generar_triangulo_pascal_multiplicado(z1)

for i, fila in enumerate(z1):
    print(f"array[{i}] = {' '.join(map(str, fila))}")
for i in range(0, len(z2), 2):
    valier = 0
for i in range(0, len(z2), 2):
    valier = 0
    for j in range(0, len(z2[i])):
        if j == 0:
            valier += z2[i][j]
        elif j % 2 != 0:
            valier += z2[i][j]
        else:
            valier -= z2[i][j]
    print(f"array[{i}] = {' '.join(map(str, z2[i]))} ::{valier}")