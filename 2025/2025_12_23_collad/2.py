def collatz(n):
    if n % 2 == 0:
        return n // 2, "R"
    else:
        return (n * 3) + 1, "L"
  
def medir_profundidad_universo(semillas_iniciales):
    estado_semillas = {s: False for s in semillas_iniciales}
    if 1 in estado_semillas: estado_semillas[1] = True
    valores_actuales = list(semillas_iniciales)
    nivel = 0
    total = len(semillas_iniciales)
    print(f"Iniciando búsqueda con {total} semillas...")
    print("-" * 50)
    while not all(estado_semillas.values()):
        nivel += 1
        nuevos_valores = []
        for i in range(total):
            val, ruta = collatz(valores_actuales[i])
            nuevos_valores.append(val)
            
            if val == 1:
                estado_semillas[semillas_iniciales[i]] = True
        valores_actuales = nuevos_valores
        llegaron = sum(estado_semillas.values())
        porcentaje = (llegaron / total) * 100
        if nivel % 10 == 0 or llegaron == total:
            print(f"Nivel {nivel:3} | Semillas en el '1': {llegaron:4}/{total} ({porcentaje:6.2f}%)")
    return nivel

myrange=32768
semillas = list(range(1, myrange+1))
profundidad_final = medir_profundidad_universo(semillas)

print("-" * 50)
print(f"LA PROFUNDIDAD DEL UNIVERSO (1-{myrange+1}) ES: {profundidad_final} NIVELES")