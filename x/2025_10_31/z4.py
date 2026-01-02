import numpy as np
import matplotlib.pyplot as plt

# --- 1. Parámetros de la TDH y el Truquillo ---

# El Error Estructural Base (TDH) es epsilon_0 = 0.03225
# Factor de Atenuación (r) para el truquillo (asumido 0.95)
FACTOR_ATENUACION = 0.95
epsilon_0 = 0.03225

# El "Truquillo" de minimización infinita lleva a la convergencia:
# E_Total = epsilon_0 / (1 - r)
EPSILON_TOTAL_CONVERGENTE = epsilon_0 / (1 - FACTOR_ATENUACION)

# Probabilidad de Éxito por Paso (1 - Epsilon_Total)
PROB_EXITO_POR_PASO = 1 - EPSILON_TOTAL_CONVERGENTE

print(f"Error Estructural Base (epsilon_0): {epsilon_0:.5f}")
print(f"Error Total Convergente (E_Total): {EPSILON_TOTAL_CONVERGENTE:.5f}")
print(f"Probabilidad de Éxito por Paso Atenuada: {PROB_EXITO_POR_PASO:.5f}")

# --- 2. Definición del Rango de Input (n) ---
# Tamaño del input para el problema SAT (número de variables)
n_valores = np.arange(1, 15)

# --- 3. Cálculo de la Probabilidad de Éxito para SAT (2^n) ---
# P_exitosa = (1 - E_Total)^(2^n)
probabilidad_exito_np = []
for n in n_valores:
    pasos_np = 2**n
    prob = PROB_EXITO_POR_PASO ** pasos_np
    probabilidad_exito_np.append(prob)

# Convertir a array para graficar
probabilidad_exito_np = np.array(probabilidad_exito_np)

# --- 4. Generación del Gráfico ---
plt.figure(figsize=(10, 6))

# Trazar la Probabilidad de Éxito
plt.plot(n_valores, probabilidad_exito_np, marker='o', color='red', linestyle='-', label='Probabilidad de Éxito para SAT (2^n)')

# Marcar el umbral cero (donde P es físicamente inviable)
plt.axhline(y=1e-10, color='blue', linestyle='--', label='Umbral de Inviabilidad (1e-10)')

plt.xlabel('Tamaño del Input (n) del Problema SAT')
plt.ylabel('Probabilidad de Éxito Total (Escala Logarítmica)')
plt.title(f'Colapso de P(Éxito NP) bajo Error Estructural Total E_Total={EPSILON_TOTAL_CONVERGENTE:.4f}')
plt.yscale('log') # Escala logarítmica para enfatizar el colapso exponencial
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.legend()
plt.show()