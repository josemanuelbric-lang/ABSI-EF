import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de Parámetros ---
# El valor actual de alpha es esencialmente constante: alpha_actual = 1/137.036

# Definimos el tamaño de la entrada de prueba
N_INPUT = 12 # Un n pequeño para evitar desbordamiento en 2^n, pero suficiente para ver el colapso

# Corrimientos al rojo (z) que representan diferentes épocas cósmicas
# z=1090 es la Recombinación (CMB); z=1 es Galaxias Distantes; z=0 es el Presente.
Z_EPOCAS = [1090, 5, 1, 0] 
TITULOS = ["Recombinación (Fundamental)", "Universo Joven", "Universo Maduro", "Presente (Observable)"]

# Valores hipótetizados/observados de la variación relativa de alpha (Delta_alpha / alpha)
# Nota: Los datos de Quasares sugieren que este valor está muy cerca de cero, 
# pero aquí simulamos los límites teóricos según la TDH.
# Hipótesis TDH: En z=1090, la estructura es casi perfecta (N~4, Delta_alpha~0).
DELTA_ALPHA_ALPHA = [1e-10, 1e-6, 1e-4, 3.225e-2] # 3.225e-2 es el epsilon de TDH (0.03225)


# --- 2. Función de Simulación del Colapso NP ---
def simular_colapso_np(delta_alpha_alpha):
    # En la TDH, el error estructural epsilon es proporcional al Delta_alpha/alpha
    epsilon = delta_alpha_alpha
    PROB_EXITO_POR_PASO = 1 - epsilon

    # Pasos requeridos para la búsqueda NP (2^n)
    pasos_np = 2**N_INPUT 

    # Probabilidad de Éxito Total para resolver el problema NP
    probabilidad_exito_total = PROB_EXITO_POR_PASO ** pasos_np
    
    return probabilidad_exito_total, pasos_np

# --- 3. Ejecución y Visualización ---

resultados_np = []
for daa in DELTA_ALPHA_ALPHA:
    prob, pasos = simular_colapso_np(daa)
    resultados_np.append(prob)

# Crear el gráfico para visualizar la hipótesis TDH
plt.figure(figsize=(10, 6))
plt.plot(Z_EPOCAS, resultados_np, marker='o', linestyle='-', color='blue', label=f'Probabilidad de Éxito NP (n={N_INPUT})')

# Ejes
plt.xlabel('Corrimiento al Rojo (z) - Tiempo Cósmico')
plt.ylabel('Probabilidad de Éxito Total de Algoritmo NP')
plt.title('Colapso de P=NP por la Tensión Estructural (TDH)')
plt.xticks(Z_EPOCAS, [f'z={z}\n{titulo}' for z, titulo in zip(Z_EPOCAS, TITULOS)])
plt.yscale('log') # Usamos escala logarítmica para ver los pequeños cambios
plt.grid(True, which="both", ls="--")
plt.axhline(y=1e-5, color='red', linestyle='--', label='Umbral Físicamente Aceptable')
plt.legend()
plt.show()

# --- 4. Interpretación de Resultados ---
print("\n--- Resultados de la Simulación ---")
for z, titulo, prob in zip(Z_EPOCAS, TITULOS, resultados_np):
    print(f"Época: {titulo} (z={z})")
    print(f"  Error Estructural (epsilon): {DELTA_ALPHA_ALPHA[Z_EPOCAS.index(z)]:.6e}")
    print(f"  P(Éxito NP): {prob:.10f}")

print("\nConclusión: La probabilidad colapsa a medida que el universo se materializa.")