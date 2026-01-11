#jose Manuel Briceno Mendoza
import time
import random

# Definimos la estructura del objeto para el Espacio Funcional (EF)
class ObjetoEF:
    def __init__(self, peso, valor):
        self.p = peso
        self.v = valor
        # La densidad es el "Orden" que permite la convergencia
        self.densidad = valor / peso 

def resolver_mochila_absi_pro(pesos_items, valores_items, capacidad):
    # 2. Convertimos esas listas en nuestros "Objetos EF"
    objetos_para_estudio = []
    for i in range(cantidadN):
        nuevo_obj = ObjetoEF(pesos_items[i], valores_items[i])
        objetos_para_estudio.append(nuevo_obj)
	
    # Paso 1: Aplicar Teoria del Buen Orden (Densidad de mayor a menor)
    objetos_para_estudio.sort(key=lambda x: x.densidad, reverse=True)
    
    mejor_valor = 0
    nodos_activos = [(0, 0, "N")] # (peso_acumulado, valor_acumulado, ruta)
    
    for obj in objetos_para_estudio:
        proximos = []
        for peso_act, valor_act, ruta in nodos_activos:
            # RUTA R: El sistema intenta incluir el objeto (Convergencia)
            if peso_act + obj.p <= capacidad:
                nv = valor_act + obj.v
                proximos.append((peso_act + obj.p, nv, ruta + "R"))
                if nv > mejor_valor: 
                    mejor_valor = nv
            
            # RUTA L: El sistema excluye el objeto (Divergencia/Exclusión)
            proximos.append((peso_act, valor_act, ruta + "L"))
        
        nodos_activos = proximos
        
        # Poda ABSI: Limitamos el crecimiento para mantener la eficiencia polinomial
        if len(nodos_activos) > 1000:
            nodos_activos.sort(key=lambda x: x[1], reverse=True)
            nodos_activos = nodos_activos[:500]
            
    return mejor_valor

random.seed(42)
cantidadN = 4096
capacidad_maxima = 12 

valores_items = [random.randint(1, 1000) for _ in range(cantidadN)]
pesos_items = [random.randint(1, 1000) for _ in range(cantidadN)]

print(f"Iniciando ABSI-EF con {cantidadN} objetos (Problema NP-Hard)...")

start = time.perf_counter()
resultado = resolver_mochila_absi_pro(pesos_items, valores_items, capacidad_maxima)
end = time.perf_counter()

print(f"\n--- RESULTADOS ---")
print(f"Valor Máximo Encontrado: {resultado}")
print(f"Tiempo de ejecución: {end - start:.6f} segundos")
