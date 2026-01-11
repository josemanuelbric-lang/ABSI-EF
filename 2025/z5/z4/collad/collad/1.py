def collatz(n):
    if n % 2 == 0:
        return n // 2, "R"
    else:
        return (n * 3) + 1, "L"

def generar_arbol_multiple(lista_inicio, niveles):
    # El primer nivel es un diccionario donde la clave es la ruta vacía ""
    arbol = [{"": lista_inicio}]
    
    for q1 in range(niveles):
        nodos_actuales = arbol[-1]
        proximo_nivel = {}
        
        for ruta, semillas in nodos_actuales.items():
            # Creamos dos nuevas rutas basadas en la anterior
            ruta_r = ruta + "R"
            ruta_l = ruta + "L"
            
            grupo_r = []
            grupo_l = []
            
            for s in semillas:
                nuevo_val, b = collatz(s)
                if b == "R":
                    grupo_r.append(nuevo_val)
                else:
                    grupo_l.append(nuevo_val)
            
            # Solo agregamos la ruta si tiene semillas
            if grupo_r: proximo_nivel[ruta_r] = grupo_r
            if grupo_l: proximo_nivel[ruta_l] = grupo_l
            
        arbol.append(proximo_nivel)
    return arbol

myrange=1048576
semillas = list(range(1, myrange+1))
niveles_simulacion = 16
resultado = generar_arbol_multiple(semillas, niveles_simulacion)

# Visualización
for i, nivel in enumerate(resultado):
    print(f"\nNIVEL {i}")
    for ruta, valores in sorted(nivel.items()):
        id_ruta = ruta if ruta != "" else "INICIO"
        print(f"{id_ruta:5} | Len:{len(valores):2} | {valores[:10]}...")