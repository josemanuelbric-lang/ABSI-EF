def collatz(n):
    if n % 2 == 0: return n // 2, "R"
    else: return (n * 3) + 1, "L"

def detectar_patron(valores):
    if len(valores) < 3: return ""
    salto = valores[1] - valores[0]
    if all(valores[i+1] - valores[i] == salto for i in range(len(valores)-1)):
        return f"(>{valores[0]}n{salto})"
    return "!!!!!!!"

def generar_arbol(lista_inicio, niveles):
    arbol = [{"": lista_inicio}]
    for _ in range(niveles):
        actual, proximo = arbol[-1], {}
        for ruta, semillas in actual.items():
            r, l = [], []
            for s in semillas:
                v, b = collatz(s)
                if b == "R": r.append(v)
                else: l.append(v)
            if r: proximo[ruta + "R"] = r
            if l: proximo[ruta + "L"] = l
        arbol.append(proximo)
    return arbol

# Configuración
MypowRange = 20
semillas = list(range(1, pow(2, MypowRange) + 1))
niveles_simulacion = 16
resultado = generar_arbol(semillas, niveles_simulacion)

historial_huellas = {}

for i, nivel in enumerate(resultado):
    print(f"\nNIVEL {i}")
    rutas_nuevas = []
    rutas_repetidas = []

    for ruta in sorted(nivel.keys()):
        valores = nivel[ruta]
        huella = tuple(valores[:16])
        patron = detectar_patron(valores[:])
        
        if huella in historial_huellas:
            rutas_repetidas.append(f"{ruta:12} | Len:{len(valores):7} | {patron}*")
        else:
            historial_huellas[huella] = ruta
            rutas_nuevas.append(f"{ruta:12} | Len:{len(valores):7} | {patron}#")
    for r in rutas_nuevas:
    	print(r)
    	
    if rutas_repetidas:
        print(f"NIVEL {i}-1 (Simetría: {len(rutas_repetidas)} rutas repetidas)")