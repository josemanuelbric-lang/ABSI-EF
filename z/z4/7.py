import time
import io
import sys

class NodoCollatz:
    def __init__(self, xdesplazamiento, xprogresion, xruta, xnivel, xisduplicate):
        self.desplazamiento: int = xdesplazamiento
        self.progresion: int = xprogresion
        self.ruta: str = xruta
        self.nivel: int = xnivel
        self.es_duplicado : bool = xisduplicate
    def __repr__(self) -> str:
        mystr: str = ""
        if(self.es_duplicado):
            mystr ="#"
        else:
            mystr ="*"
        return f"{self.ruta:32}(>{self.desplazamiento}N{self.progresion}{mystr})"
    def GenerateList(self, xrange : int) -> list[int]:
        mylist : list[int]=[]
        for q1 in range(xrange):
            mylist.append((self.progresion * q1) + self.desplazamiento)
        return mylist
    def mytuple(self) -> tuple[int, int]:
        return (self.desplazamiento, self.progresion)

def collatz(n) -> tuple[int, str]:
    if n % 2 == 0: return n // 2, "R"
    else: return (n * 3) + 1, "L"

def detectar_patron(valores: list[int]) -> tuple[int, int]:
    if len(valores) < int(cantidadDeSemillas / 2):
        raise ValueError("muyCorto")
    salto:int = valores[1] - valores[0]
    if all(valores[i+1] - valores[i] == salto for i in range(len(valores)-1)):
        return (valores[0], salto)
    raise ValueError("NoSimple")

def generar_arbol(nodo_de_Inicio : NodoCollatz, niveles : int) -> list[dict[str, NodoCollatz]]:
    arbol: list[dict[str, NodoCollatz]] = [{"N": nodo_de_Inicio}]
    historial_patrones: dict[tuple[int, int], bool] = {}
    historial_de_resultados: dict[tuple[int,int], tuple[tuple[int,int],tuple[int,int]]] = {}
    for q1 in range(niveles):
        actual: dict[str, NodoCollatz] = arbol[-1]
        proximo: dict[str, NodoCollatz] = {}
        for ruta, q2NodoCollatzx in actual.items():
            llave_nodo: tuple[int, int] = (q2NodoCollatzx.desplazamiento, q2NodoCollatzx.progresion)
            if llave_nodo in historial_de_resultados:
                tupleV: tuple[tuple[int, int], tuple[int, int]] = historial_de_resultados[llave_nodo]
                tupleR: tuple[int, int] = tupleV[0]
                tupleL: tuple[int, int] = tupleV[1]
                if tupleR != (-1, -1):
                    isDup: bool = tupleR in historial_patrones
                    if(isDup == False):
                        historial_patrones[tupleR] = True
                    proximo[ruta + "R"] = NodoCollatz(tupleR[0], tupleR[1], ruta + "R", q1+1, isDup)
                if tupleL != (-1, -1):
                    isDup: bool = tupleL in historial_patrones
                    if(isDup == False):
                        historial_patrones[tupleL] = True
                    proximo[ruta + "L"] = NodoCollatz(tupleL[0], tupleL[1], ruta + "L", q1+1, isDup)
                continue
            r_vals: list[int] = []
            l_vals: list[int] = []
            semillas: list[int] = q2NodoCollatzx.GenerateList(cantidadDeSemillas)
            for s in semillas:
                v, b = collatz(s)
                if b == "R":
                    r_vals.append(v)
                else:
                    l_vals.append(v)
            res_R: tuple[int, int] = (-1, -1)
            res_L: tuple[int, int] = (-1, -1)
            if len(r_vals) > 1:
                myr : tuple[int, int] = detectar_patron(r_vals)
                res_R: tuple[int, int] = myr
                isDuplicate: bool = myr in historial_patrones
                if(isDuplicate == False):
                    historial_patrones[myr] = True
                proximo[ruta + "R"] = NodoCollatz(myr[0], myr[1], ruta + "R", q1+1, isDuplicate)
            if len(l_vals) > 1:
                myl: tuple[int, int] = detectar_patron(l_vals)
                res_L: tuple[int, int] = myl
                isDuplicate: bool = myl in historial_patrones
                if(isDuplicate == False):
                    historial_patrones[myl] = True
                proximo[ruta + "L"] = NodoCollatz(myl[0], myl[1], ruta + "L", q1+1, isDuplicate)
            historial_de_resultados[llave_nodo] = (res_R, res_L)
        arbol.append(proximo)
    return arbol

if __name__ == "__main__":
    niveles = 18
    cantidadDeSemillas = 32
    nuevo_nodo: NodoCollatz = NodoCollatz(1, 1, "N", 0, False)
    for q1 in range(1, 33):
        inicio = time.perf_counter()
        resultado: list[dict[str, NodoCollatz]] = generar_arbol(nuevo_nodo, q1)
        print(f"{q1} {time.perf_counter() - inicio}")
    exit(0)
    sb = []
    for q1 in range(len(resultado)):
        sb.append(f"{q1}" + "=" * 50)
        for q2key, q2value in resultado[q1].items():
            sb.append(str(q2value))
    print("\n".join(sb))
    milistalen: list[str] =[]
    for i, nivel in enumerate(resultado):
        print(f"\nNIVEL {i}")
        rutas_imprimir: list[str] = []
        rutas_simetria_R: list[str] = []
        for ruta in sorted(nivel.keys()):
            valores: NodoCollatz = nivel[ruta]
            linea: str = f"{valores}"
            if ruta.startswith("NR"):
                rutas_simetria_R.append(linea)
            else:
                rutas_imprimir.append(linea)
        for r in rutas_imprimir:
            print(r)
        if rutas_simetria_R:
            milistalen.append(f"NIVEL{i} {len(rutas_simetria_R):16}")
            print(f"NIVEL {i}-1 (Simetría R) Rutas: {len(rutas_simetria_R)}")	
    for q1 in milistalen:
        print(f"{q1}")