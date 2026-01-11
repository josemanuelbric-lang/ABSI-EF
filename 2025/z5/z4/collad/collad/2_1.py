def collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return (n * 3) + 1

def medir_profundidad_universo(semillas_iniciales, niveles_interes):
    total = len(semillas_iniciales)
    estado_semillas = {s: False for s in semillas_iniciales}
    if 1 in estado_semillas: estado_semillas[1] = True
    
    valores_actuales = list(semillas_iniciales)
    nivel = 0
    rezagados = list(semillas_iniciales) # Para rastrear quiénes faltan

    print(f"Iniciando búsqueda con {total} semillas...")
    print("-" * 60)

    while not all(estado_semillas.values()):
        nivel += 1
        nuevos_valores = []
        
        for i in range(total):
            # Solo procesamos si la semilla original no ha llegado al 1
            if not estado_semillas[semillas_iniciales[i]]:
                val = collatz(valores_actuales[i])
                valores_actuales[i] = val
                
                if val == 1:
                    estado_semillas[semillas_iniciales[i]] = True
            
        llegaron = sum(estado_semillas.values())
        porcentaje = (llegaron / total) * 100

        # FILTRO: Solo imprime si el nivel está en tu lista o si es el final
        if nivel in niveles_interes or llegaron == total:
            print(f"HIT -> Nivel {nivel:3} | Semillas en '1': {llegaron:5}/{total} ({porcentaje:6.2f}%)")
            
        # Si falta solo uno, guardamos quién es para el reporte final
        if llegaron == total - 1:
            for s, finalizado in estado_semillas.items():
                if not finalizado:
                    ultimo_numero = s

    return nivel, ultimo_numero

MypowRange=18
myrange = pow(2, MypowRange)
niveles_hitos = [1, 2, 3, 6, 10, 17, 28, 46, 76, 125, 205, 335, 549, 896, 1461, 2385]
semillas = list(range(1, myrange + 1))

profundidad, culpable = medir_profundidad_universo(semillas, niveles_hitos)

print("-" * 60)
print(f"LA PROFUNDIDAD DEL UNIVERSO (1-{myrange}) ES: {profundidad} NIVELES")
print(f"La última semilla en colapsar fue la: {culpable}")