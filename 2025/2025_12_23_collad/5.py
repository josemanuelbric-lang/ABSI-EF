class NodoCollatz:
    def __init__(self, inicio, salto, ruta, nivel):
        self.desplazamiento = inicio        # El "desplazamiento" (primer número de la serie)
        self.progresión = salto          # La "progresión" (distancia entre números)
        self.ruta = ruta            # ID único (ej: "LRRL")
        self.nivel = nivel          # Profundidad en el árbol
        # Atributos calculados útiles para análisis:
        self.es_duplicado = False
        self.referencia_original = None

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

MypowRange = 20
semillas = list(range(1, pow(2, MypowRange) + 1))
niveles_simulacion = 5
resultado = generar_arbol(semillas, niveles_simulacion)

historial_patrones = {}

for i, nivel in enumerate(resultado):
    print(f"\nNIVEL {i}")
    
    rutas_imprimir = []
    rutas_simetria_R = []

    for ruta in sorted(nivel.keys()):
        valores = nivel[ruta]
        patron = detectar_patron(valores[:100])
        if patron in historial_patrones and patron != "!!!!!!!":
            marca = "*"
        else:
            marca = "#"
            if patron != "!!!!!!!":
                historial_patrones[patron] = ruta
        linea = f"{ruta:12} | Len:{len(valores):7} | {patron}{marca}"
        if ruta.startswith("R"):
            rutas_simetria_R.append(linea)
        else:
            rutas_imprimir.append(linea)
    for r in rutas_imprimir:
        print(r)
    if rutas_simetria_R:
        print(f"NIVEL {i}-1 (Simetría R) Rutas: {len(rutas_simetria_R)}")	