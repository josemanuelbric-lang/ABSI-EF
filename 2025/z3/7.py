#jose manuel Briceno Mendoza
class NodoABSI:
    def __init__(self, nivel, peso_actual, valor_actual, ruta):
        self.nivel = nivel
        self.peso = peso_actual
        self.valor = valor_actual
        self.ruta = ruta  # Ejemplo: "RRL" (R=Meter objeto, L=No meter)

def resolver_mochila_absi(pesos, valores, capacidad):
    # Iniciamos el bloque inicial (Nivel 0)
    mejor_valor = 0
    mejor_ruta = ""
    
    # El árbol comienza con un nodo vacío
    nodos_activos = [NodoABSI(0, 0, 0, "N")]
    
    for i in range(len(pesos)):
        proximo_nivel = []
        for nodo in nodos_activos:
            # RUTA R: Intentamos incluir el objeto (Contracción hacia la solución)
            nuevo_peso = nodo.peso + pesos[i]
            if nuevo_peso <= capacidad:
                nuevo_valor = nodo.valor + valores[i]
                ruta_r = nodo.ruta + "R"
                proximo_nivel.append(NodoABSI(i + 1, nuevo_peso, nuevo_valor, ruta_r))
                
                # Actualizamos si encontramos una mejor "Convergencia"
                if nuevo_valor > mejor_valor:
                    mejor_valor = nuevo_valor
                    mejor_ruta = ruta_r
            
            # RUTA L: No incluimos el objeto (Exclusión)
            ruta_l = nodo.ruta + "L"
            proximo_nivel.append(NodoABSI(i + 1, nodo.peso, nodo.valor, ruta_l))
        
        nodos_activos = proximo_nivel
        print(f"Nivel {i}: Procesadas {len(nodos_activos)} rutas | Mejor Valor actual: {mejor_valor}")

    return mejor_valor, mejor_ruta

# DATOS DE PRUEBA
valores_p = [60, 100, 120]
pesos_p = [10, 20, 30]
capacidad_m = 50

res_valor, res_ruta = resolver_mochila_absi(pesos_p, valores_p, capacidad_m)
print(f"\nRESULTADO FINAL ABSI-EF:")
print(f"Ruta Ganadora: {res_ruta} | Valor Máximo: {res_valor}")
