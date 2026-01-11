from collections import namedtuple
class NodoCollatz:
    def __init__(self, xdesplazamiento, xprogresion, xruta, xnivel):
        self.desplazamiento: int = xdesplazamiento
        self.progresion: int = xprogresion
        self.ruta: str = xruta
        self.nivel: int = xnivel
        # Atributos calculados útiles para análisis:
        self.es_duplicado : bool= False
        self.referencia_original = None
    def __repr__(self) -> str:
        return f"({self.ruta}(>{self.desplazamiento}N{self.progresion}))"
    def GenerateList(self, xrange : int) -> list[int]:
        mylist : list[int]=[]
        for q1 in range(xrange):
            mylist.append((self.progresion * q1) + self.desplazamiento)
        return mylist
def collatz(n):
    if n % 2 == 0: return n // 2, "R"
    else: return (n * 3) + 1, "L"

def detectar_patron(valores: list[int]):
    if len(valores) < 16:
        raise ValueError("muyCorto")
    salto:int = valores[1] - valores[0]
    if all(valores[i+1] - valores[i] == salto for i in range(len(valores)-1)):
        return (valores[0], salto) #(f"(>{valores[0]}n{salto})")
    raise ValueError("NoSimple")
    return "!!!!!!!"

def generar_arbol(nodo_de_Inicio : NodoCollatz, niveles : int):
    arbol = [{"N": nodo_de_Inicio}]
    for q1 in range(niveles):
        actual: dict[str, NodoCollatz]= arbol[-1]
        proximo: dict[str, NodoCollatz] = {}
        for ruta, q2NodoCollatzx in actual.items():
            r: list[int] = []
            l: list[int] = []
            semillas: list[int] = q2NodoCollatzx.GenerateList(32)
            # print(semillas)
            for s in semillas:
                v, b = collatz(s)
                if b == "R":
                    r.append(v)
                else:
                    l.append(v)
            if len(r) > 1:
                myr = detectar_patron(r)
                proximo[ruta + "R"] = NodoCollatz(myr[0], myr[1], ruta + "R", q1+1)
            if len(l) > 1:
                myr = detectar_patron(l)
                proximo[ruta + "L"] = NodoCollatz(myr[0], myr[1], ruta + "L", q1+1)
        arbol.append(proximo)
    return arbol

#MypowRange = 20
#semillas = list(range(1, pow(2, MypowRange) + 1))

nuevo_nodo = NodoCollatz(1, 1, "N", 0)
resultado = generar_arbol(nuevo_nodo, 4)
print(resultado)
# historial_patrones = {}

# for i, nivel in enumerate(resultado):
#     print(f"\nNIVEL {i}")
    
#     rutas_imprimir = []
#     rutas_simetria_R = []

#     for ruta in sorted(nivel.keys()):
#         valores = nivel[ruta]
#         patron = detectar_patron(valores[:100])
#         if patron in historial_patrones and patron != "!!!!!!!":
#             marca = "*"
#         else:
#             marca = "#"
#             if patron != "!!!!!!!":
#                 historial_patrones[patron] = ruta
#         linea = f"{ruta:12} | Len:{len(valores):7} | {patron}{marca}"
#         if ruta.startswith("R"):
#             rutas_simetria_R.append(linea)
#         else:
#             rutas_imprimir.append(linea)
#     for r in rutas_imprimir:
#         print(r)
#     if rutas_simetria_R:
#         print(f"NIVEL {i}-1 (Simetría R) Rutas: {len(rutas_simetria_R)}")	