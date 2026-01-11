import matplotlib.pyplot as plt
import numpy as np

# Definición de la función de Collatz
def collatz_step(n):
    # Usamos int() para asegurar que el resultado de la división par sea un entero
    # Esto es crucial para la consistencia de la recursión en Collatz
    if n % 2 == 0:
        return n / 2
    else:
        return 3 * n + 1

# --- Configuración ---
NUM_ITERATIONS = 4	  # Generar hasta A^(10) y B^(10)
K_MAX = 16          # Generar series hasta k=100
k_values = np.arange(1, K_MAX + 1)

# Diccionario para almacenar todas las series de A y B
series_A = {}
series_B = {}

# --- SERIES BASE ---
# A: Ascenso (6k - 2)
A_base = 6 * k_values - 2
series_A[0] = A_base
# B: Naturales (k)
B_base = k_values
series_B[0] = B_base

# --- GENERACIÓN ITERATIVA DE PRIMAS ---

# 1. Generación de A', A'', A'''... hasta A^(10)
current_A = A_base
for i in range(1, NUM_ITERATIONS + 1):
    # La primera iteración (A') es N/2, ya que A_base es todo par.
    # El resto de las iteraciones usan la regla de Collatz completa.
    if i == 1:
        next_A = current_A / 2  # A'
    else:
        next_A = [collatz_step(n) for n in current_A]

    series_A[i] = next_A
    current_A = next_A # Actualizamos la serie para la próxima iteración

# 2. Generación de B', B'', B'''... hasta B^(10)
current_B = B_base
for i in range(1, NUM_ITERATIONS + 1):
    # Todas las iteraciones de B usan la regla de Collatz completa
    next_B = [collatz_step(n) for n in current_B]
    series_B[i] = next_B
    current_B = next_B # Actualizamos la serie para la próxima iteración

# --- GRAFICAR ---

# Creamos la figura con 1 fila y 2 columnas
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Definir una paleta de colores para diferenciar las 11 líneas
colors = plt.cm.plasma(np.linspace(0, 1, NUM_ITERATIONS + 1))
linestyles = ['-', '--', ':', '-.'] * 3 # Alternar estilos si los colores no son suficientes

# --- Subgráfico 1: Serie A (hasta A^(10)) ---
for i in range(NUM_ITERATIONS + 1):
    label = f"A{i * '′'}" if i > 0 else "A (6k - 2)" # A', A'', A'''...
    axes[0].plot(k_values, series_A[i], label=label, color=colors[i], linestyle=linestyles[i % len(linestyles)], linewidth=1.5 if i < 3 else 0.8)

axes[0].set_title(f"🚀 Serie A: Transformación del Ascenso (hasta A¹⁰)", fontsize=14)
axes[0].set_xlabel("Índice k", fontsize=12)
axes[0].set_ylabel("Valor de la Secuencia", fontsize=12)
axes[0].legend(loc='upper left', ncol=2, fontsize=8)
axes[0].grid(True, linestyle='--')


# --- Subgráfico 2: Serie B (hasta B^(10)) ---
for i in range(NUM_ITERATIONS + 1):
    label = f"B{i * '′'}" if i > 0 else "B (k = Naturales)"
    axes[1].plot(k_values, series_B[i], label=label, color=colors[i], linestyle=linestyles[i % len(linestyles)], linewidth=1.5 if i < 3 else 0.8)

axes[1].set_title(f"🌌 Serie B: Transformación de la Secuencia General (hasta B¹⁰)", fontsize=14)
axes[1].set_xlabel("Índice k", fontsize=12)
axes[1].set_ylabel("Valor de la Secuencia", fontsize=12)
axes[1].legend(loc='upper left', ncol=2, fontsize=8)
axes[1].grid(True, linestyle='--')


# Ajuste general del gráfico
plt.suptitle(f"Análisis de {NUM_ITERATIONS} Iteraciones de Collatz para Series A y B (hasta k={K_MAX})", fontsize=16, y=1.03)
plt.tight_layout(rect=[0, 0, 1, 0.98]) # Ajuste para que el título superior no se corte
plt.show()