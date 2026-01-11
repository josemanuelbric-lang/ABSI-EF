def collatz(n):
    if n % 2 == 0:
        return n // 2, "R"
    else:
        return (n * 3) + 1, "L"

def detectar_patron(valores):
    if len(valores) < 3: 
        return "" # No hay suficientes datos para asegurar un patrón
    
    # Calculamos el salto esperado (B) entre los dos primeros elementos
    salto = valores[1] - valores[0]
    
    # Verificamos si TODA la muestra sigue ese mismo salto
    es_aritmetica = True
    for i in range(len(valores) - 1):
        if valores[i+1] - valores[i] != salto:
            es_aritmetica = False
            break
    
    if es_aritmetica:
        inicio = valores[0]
        return f"(>{inicio}n{salto})"
    else:
        # ¡ALERTA! La serie ha dejado de ser una progresión aritmética simple
        return "!!!!!!!" 

def generar_arbol_con_marcas(lista_inicio, niveles):
    arbol = [{"": lista_inicio}]
    for q1 in range(niveles):
        nodos_actuales = arbol[-1]
        proximo_nivel = {}
        for ruta, semillas in nodos_actuales.items():
            ruta_r, ruta_l = ruta + "R", ruta + "L"
            grupo_r, grupo_l = [], []
            for s in semillas:
                nuevo_val, b = collatz(s)
                if b == "R": grupo_r.append(nuevo_val)
                else: grupo_l.append(nuevo_val)
            if grupo_r: proximo_nivel[ruta_r] = grupo_r
            if grupo_l: proximo_nivel[ruta_l] = grupo_l
        arbol.append(proximo_nivel)
    return arbol

MypowRange=20
RangoDenumeros = pow(2, MypowRange)
semillas = list(range(1, RangoDenumeros + 1))
niveles_simulacion = 4
resultado = generar_arbol_con_marcas(semillas, niveles_simulacion)

historial_valores = {}

for i, nivel in enumerate(resultado):
    print(f"\nNIVEL {i}")
    for ruta, valores in sorted(nivel.items()):
        id_ruta = ruta if ruta != "" else "INICIO"
        
        huella = tuple(valores[:5])
        if huella in historial_valores:
            marca = "*"
        else:
            marca = "#"
            historial_valores[huella] = ruta
            
        patron = detectar_patron(valores[:100]) # Analizamos los primeros 100 para estar seguros
        
        print(f"{id_ruta:12} | Len:{len(valores)} | {patron}{marca}")
        #print(f"{id_ruta:12} | Len:{len(valores):7} | {patron}{marca} | {valores[:0]}...")