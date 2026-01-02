#jose manuel Briceno Mendoza
import time
import random

# --- TU LÓGICA ABSI-EF ---
class ObjetoEF:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.densidad = v / p

def resolver_mochila_absi_pro(v, p, capacidad):
    items = sorted(zip(v, p), key=lambda x: x[0]/x[1], reverse=True)
    mejor_valor = 0
    nodos_activos = [(0, 0, "N")]
    for obj in objetos:
        proximos = []
        for peso_act, valor_act, ruta in nodos_activos:
            if peso_act + obj.p <= capacidad:
                nv = valor_act + obj.v
                proximos.append((peso_act + obj.p, nv, ruta + "R"))
                if nv > mejor_valor: mejor_valor = nv
            proximos.append((peso_act, valor_act, ruta + "L"))
        nodos_activos = proximos
        if len(nodos_activos) > 1000:
            nodos_activos.sort(key=lambda x: x[1], reverse=True)
            nodos_activos = nodos_activos[:500]
    return mejor_valor

cantidadN = 10
capacidad_maxima = 50
valores = [random.randint(10, 100) for _ in range(cantidadN)]
pesos = [random.randint(1, 20) for _ in range(cantidadN)]

print(f"Comparando {cantidadN} objetos...\n")


start = time.perf_counter()
res_absi = resolver_mochila_absi_pro(valores, pesos, capacidad_maxima)
t_absi = time.perf_counter() - start

print(f"ABSI-EF:  Valor {res_absi} | Tiempo: {t_absi:.6f} seg")
