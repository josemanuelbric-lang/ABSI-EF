import numpy as np
import matplotlib.pyplot as plt

# --- LÓGICA DE PROCESAMIENTO ---

def collatz(n):
    if n % 2 == 0:
        return n // 2, "R"
    else:
        return (n * 3) + 1, "L"

def detectar_patron(valores):
    if len(valores) < 3: return ""
    salto = valores[1] - valores[0]
    es_aritmetica = all(valores[i+1] - valores[i] == salto for i in range(len(valores) - 1))
    
    if es_aritmetica:
        inicio = valores[0]
        return f"(>{inicio}n{salto})"
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

# --- SIMULACIÓN NEGATIVA ---
MypowRange = 20
RangoDenumeros = pow(2, MypowRange)
# Semillas negativas: de -1048576 a -1
semillas = list(range(-RangoDenumeros, 0)) 
niveles_simulacion = 4
resultado = generar_arbol_con_marcas(semillas, niveles_simulacion)

# --- VISUALIZACIÓN ADAPTADA A NEGATIVOS ---

def generar_onda_collatz_negativa(resultado):
    # Aumentamos x para ver la expansión de los saltos n3, n6, n18...
    x = np.linspace(0, 20 * np.pi, 32768)
    onda_total = np.zeros_like(x)
    
    plt.figure(figsize=(12, 6))
    
    for i, nivel in enumerate(resultado):
        if i == 0: continue 
        
        for ruta, valores in nivel.items():
            if len(valores) < 2: continue
            
            salto = valores[1] - valores[0]
            # Amplitud negativa para representar el "espejo" del universo negativo
            amplitud = np.log2(len(valores)) * -1 
            
            # La fase L/R en negativos suele mostrar una rotación inversa
            fase_ruta = ruta.count('L') * (np.pi / 4)
            
            # Frecuencia basada en la densidad de los saltos negativos (n3, n6...)
            # Si salto es negativo, usamos su valor absoluto para la frecuencia física
            frecuencia = 1 / abs(salto if salto != 0 else 1) 
            
            onda_nodo = amplitud * np.sin(2 * np.pi * frecuencia * x + fase_ruta)
            onda_total += onda_nodo
            
            # Graficamos con colores tenues para ver la interferencia
            plt.plot(x, onda_nodo, alpha=0.15)

    plt.title("Interferencia de Átomos Dimensionales (Universo Negativo)")
    plt.xlabel("Espacio de Fase (Rotación L/R)")
    plt.ylabel("Amplitud Inversa (Log Len)")
    plt.grid(True, alpha=0.2)
    plt.axhline(0, color='black', lw=1)
    plt.show()

    # Firma Dinámica del Sistema Negativo
    plt.figure(figsize=(12, 4))
    plt.plot(x, onda_total, color='darkred', linewidth=2)
    plt.title("Firma Dinámica Negativa (Onda Maestra)")
    plt.fill_between(x, onda_total, color='red', alpha=0.1)
    plt.grid(True, alpha=0.3)
    plt.show()

# Ejecución
generar_onda_collatz_negativa(resultado)