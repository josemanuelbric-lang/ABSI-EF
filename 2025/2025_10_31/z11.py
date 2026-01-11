import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de Constantes de la TDH ---
D = 4.0             # Dimensión Teórica
N_OBSERVABLE = 3.8710 
# Error Estructural (epsilon) en el universo observable
EPSILON = (D - N_OBSERVABLE) / D 

# Límite de Complejidad TDH (pasos confiables antes del 63.2% de probabilidad de error)
# L_MAX = -1 / np.log(1 - EPSILON) 
L_MAX = 30.56 

# --- 2. Parámetros de la Simulación ---
N_PROBLEMA = 15     # Variables para el problema NP (SAT)
PASOS_REQUERIDOS = 2**N_PROBLEMA # Total de ~32,768 pasos
N_SIMULACIONES = 1000 # Número de veces que se "ejecuta" el algoritmo

# --- 3. Simulación de Monte Carlo ---
pasos_de_fallo = []

for _ in range(N_SIMULACIONES):
    pasos_ejecutados = 0
    falla_en_curso = False
    
    # Simular la ejecución de la búsqueda NP (2^n pasos)
    for paso in range(1, PASOS_REQUERIDOS + 1):
        
        # Simular el Error Estructural TDH:
        # Generar un número aleatorio entre 0 y 1. Si cae dentro de la región de error (0 a epsilon), el paso falla.
        if np.random.rand() < EPSILON:
            pasos_de_fallo.append(paso)
            falla_en_curso = True
            break
            
        pasos_ejecutados = paso
        
    if not falla_en_curso:
        # Esto solo ocurre si PASOS_REQUERIDOS es muy pequeño o el epsilon es 0.
        pasos_de_fallo.append(PASOS_REQUERIDOS)

# --- 4. Análisis y Gráfico de Resultados ---
# Calcula el punto de colapso promedio
PUNTO_COLAPSO_PROMEDIO = np.mean(pasos_de_fallo)

plt.figure(figsize=(10, 6))
plt.hist(pasos_de_fallo, bins=50, color='salmon', edgecolor='black', alpha=0.7, density=True)

# Línea del Límite Estructural Teórico
plt.axvline(L_MAX, color='blue', linestyle='--', linewidth=2, label=f'Límite Teórico $L_{{MAX}}$ ({L_MAX:.2f} pasos)')

# Línea del Colapso Promedio
plt.axvline(PUNTO_COLAPSO_PROMEDIO, color='red', linestyle='-', linewidth=2, label=f'Colapso Promedio ({PUNTO_COLAPSO_PROMEDIO:.2f} pasos)')

plt.xlabel('Pasos de Cómputo Ejecutados Antes de Fallo')
plt.ylabel('Frecuencia Normalizada')
plt.title(f'Colapso de Proceso NP por Error Estructural ($\mathbf{{\\epsilon}} = {EPSILON:.5f}$)')
plt.xlim(0, 100) # Mostrar solo los primeros 100 pasos para visualización

plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

# --- 5. Conclusiones
print("-" * 50)
print(f"Parámetros TDH:")
print(f"  Error Estructural (epsilon): {EPSILON:.5f}")
print(f"  Pasos requeridos por NP (n={N_PROBLEMA}): {PASOS_REQUERIDOS}")
print(f"  Límite Teórico de Complejidad (L_MAX): {L_MAX:.2f} pasos")
print("-" * 50)
print(f"Resultado de la Simulación:")
print(f"  Punto de Colapso Promedio: {PUNTO_COLAPSO_PROMEDIO:.2f} pasos")
print("\nConclusión:")
if PUNTO_COLAPSO_PROMEDIO < L_MAX * 1.5:
    print(f"La simulación confirma que la búsqueda exponencial colapsa en {PUNTO_COLAPSO_PROMEDIO:.2f} pasos, lo cual está extremadamente cerca del límite teórico L_MAX de {L_MAX:.2f} pasos. El problema NP ($2^{15} = 32768$ pasos) FALLE en el primer segundo de ejecución.")