def collatz2(n):
    if n % 2 == 0:
        return n-1, "R"
    else:
        return n+1, "L"
def collatz3(n):
    if n % 2 == 0:
        return n // 2, "R"
    else:
        return n + 1, "L"
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
#semillas = list(range(-RangoDenumeros, 0))
niveles_simulacion = 8
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
import numpy as np
import matplotlib.pyplot as plt

def generar_onda_collatz(resultado):
    # Definimos un eje de tiempo o espacio discreto
    x = np.linspace(0, 16, 32768)
    onda_total = np.zeros_like(x)
    
    plt.figure(figsize=(12, 6))
    
    # Colores para diferenciar niveles
    colores = ['blue', 'green', 'red', 'purple', 'orange']
    
    for i, nivel in enumerate(resultado):
        if i == 0: continue # Saltamos el inicio para ver la ramificación
        
        for ruta, valores in nivel.items():
            if len(valores) < 2: continue
            
            # Extraemos los datos del "patron" (>inicio n salto)
            inicio = valores[0]
            salto = valores[1] - valores[0]
            amplitud = np.log2(len(valores)) # Escala logarítmica para manejar Len:1048576
            
            # Convertimos la ruta L/R en una variación de fase
            # L suma fase, R mantiene o resta
            fase_ruta = ruta.count('L') * (np.pi / 4)
            
            # Generamos la onda individual
            # y = Amplitud * sin(Frecuencia * x + Fase)
            frecuencia = 1 / (salto if salto != 0 else 1) 
            onda_nodo = amplitud * np.sin(2 * np.pi * frecuencia * x + fase_ruta)
            
            onda_total += onda_nodo
            
            # Dibujamos las ondas de los niveles más profundos con transparencia
            plt.plot(x, onda_nodo, alpha=0.3, label=f"Ruta {ruta}" if i < 3 else "")

    plt.title("Interferencia de Ondas basada en Ramificación Collatz (L/R)")
    plt.xlabel("Espacio de Fase")
    plt.ylabel("Amplitud (Log Len)")
    plt.grid(True, alpha=0.3)
    plt.show()

    # Visualización de la "Onda Maestra" (Suma de todas)
    plt.figure(figsize=(12, 4))
    plt.plot(x, onda_total, color='black', linewidth=2)
    plt.title("Onda Resultante (Firma Dinámica del Sistema)")
    plt.show()

# Para ejecutarlo, simplemente añade esta línea al final de tu código:
generar_onda_collatz(resultado)