import time
import random

# --- TU LÓGICA ABSI-EF ---
class ObjetoEF:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.densidad = v / p

def resolver_mochila_absi_pro(objetos, capacidad):
    objetos.sort(key=lambda x: x.densidad, reverse=True)
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

# --- LÓGICA DE FUERZA BRUTA (Exponencial) ---
def fuerza_bruta_recursiva(objetos, capacidad, n):
    # Caso base: no quedan objetos o capacidad agotada
    if n == 0 or capacidad == 0:
        return 0
    # Si el objeto pesa más que la capacidad, se excluye (Ruta L forzada)
    if objetos[n-1].p > capacidad:
        return fuerza_bruta_recursiva(objetos, capacidad, n-1)
    else:
        # Probamos todas las combinaciones: Meter (R) y No Meter (L)
        return max(
            objetos[n-1].v + fuerza_bruta_recursiva(objetos, capacidad - objetos[n-1].p, n-1),
            fuerza_bruta_recursiva(objetos, capacidad, n-1)
        )

# --- PRUEBA DE COMPARACIÓN ---
random.seed(42)
n_objetos = 22 # Reducimos a 22 para que la fuerza bruta no se congele
objetos_prueba = [ObjetoEF(random.randint(1, 20), random.randint(10, 100)) for _ in range(n_objetos)]
capacidad_prueba = 100

print(f"Comparando {n_objetos} objetos...\n")

# Ejecución ABSI-EF
start = time.perf_counter()
res_absi = resolver_mochila_absi_pro(objetos_prueba, capacidad_prueba)
t_absi = time.perf_counter() - start

# Ejecución Fuerza Bruta
start = time.perf_counter()
res_fb = fuerza_bruta_recursiva(objetos_prueba, capacidad_prueba, n_objetos)
t_fb = time.perf_counter() - start

print(f"--- RESULTADOS ---")
print(f"ABSI-EF:      Valor {res_absi} | Tiempo: {t_absi:.6f} seg")
print(f"Fuerza Bruta: Valor {res_fb} | Tiempo: {t_fb:.6f} seg")
print(f"Diferencia de velocidad: {t_fb / t_absi:.2f} veces más rápido el ABSI-EF")
