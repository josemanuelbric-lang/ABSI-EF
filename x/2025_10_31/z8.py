import numpy as np
import matplotlib.pyplot as plt

# --- 1. Parámetros Estructurales de la TDH ---
EPSILON = 0.03225
PROB_EXITO_POR_PASO = 1 - EPSILON
N_VALORES = np.arange(1, 10)  # Input (n) hasta 9

# Límite para comparación
L_MAX_CALCULADO = -1 / np.log(1 - EPSILON) # ~30.56

# --- 2. Funciones de Complejidad (Pasos Requeridos) ---

# T(n) para SAT (Peor caso Fuerza Bruta)
def complejidad_sat(n):
    return 2**n

# T(n) para TSP (Peor caso general, el 2^n domina)
def complejidad_tsp(n):
    # n^2 * 2^n (Usamos solo el factor exponencial dominante para el colapso)
    return n**2 * 2**n

# --- 3. Cálculo de la Probabilidad de Éxito Total (P_exitosa = (1 - epsilon)^T) ---

def calcular_colapso(complejidad_func, n_valores):
    probabilidades = []
    for n in n_valores:
        pasos = complejidad_func(n)
        prob = PROB_EXITO_POR_PASO ** pasos
        probabilidades.append(prob)
    return np.array(probabilidades)

prob_sat = calcular_colapso(complejidad_sat, N_VALORES)
prob_tsp = calcular_colapso(complejidad_tsp, N_VALORES)

# --- 4. Generación del Gráfico ---
plt.figure(figsize=(10, 6))

# Curvas de Colapso
plt.plot(N_VALORES, prob_sat, marker='o', color='green', linestyle='-', label='SAT ($2^n$)')
plt.plot(N_VALORES, prob_tsp, marker='x', color='red', linestyle='--', label='TSP ($n^2 \cdot 2^n$)')

# Umbral de Inviabilidad (1e-10)
UMBRAL_INVIABILIDAD = 1e-10
plt.axhline(y=UMBRAL_INVIABILIDAD, color='blue', linestyle='-.', label='Umbral de Inviabilidad (1e-10)')

plt.xlabel('Tamaño del Input ($n$)')
plt.ylabel('Probabilidad de Éxito Total (Escala Logarítmica)')
plt.title(f'Colapso Comparado de Problemas NP-Completos (L_MAX={L_MAX_CALCULADO:.2f})')
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.ylim(1e-180, 1)
plt.legend()
plt.show()

# --- 5. Resultados y Predicción ---
print("\n--- Resultados de la Predicción ---")
for n in N_VALORES:
    p_sat = calcular_colapso(complejidad_sat, [n])[0]
    p_tsp = calcular_colapso(complejidad_tsp, [n])[0]
    
    # La complejidad real del TSP es mayor, por lo tanto, el colapso es más rápido.
    if p_sat > UMBRAL_INVIABILIDAD and p_tsp < UMBRAL_INVIABILIDAD:
        print(f"n={n}: TSP ya colapsó (< 1e-10), SAT aún es viable.")

# El primer valor que cruza L_MAX es n=5.
print(f"\nEl Colapso de P(Éxito) ocurre alrededor de n=5, ya que 2^5 = 32, que supera el L_MAX (~30.56).")