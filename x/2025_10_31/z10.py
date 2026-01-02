import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de Parámetros de la TDH ---
D = 4.0             # Dimensión Teórica
N_OBSERVABLE = 3.8710 
N_PERFECCION = 4.0  # Tensión Maestra sin error

N_INPUT = 12        # Tamaño del input para el problema NP (SAT)
PASOS_NP = 2**N_INPUT # Número de pasos de cómputo (4096)

# --- 2. Condición 1: CON ERROR (P != NP) ---
# Se calcula el Error Estructural observable (epsilon > 0)
EPSILON_CON_ERROR = (D - N_OBSERVABLE) / D 
# EPSILON_CON_ERROR es aprox. 0.03225

# Probabilidad de éxito de UN solo paso
P_PASO_CON_ERROR = 1 - EPSILON_CON_ERROR

# Probabilidad de éxito TOTAL para 4096 pasos
P_EXITO_CON_ERROR = P_PASO_CON_ERROR ** PASOS_NP

# --- 3. Condición 2: SIN ERROR (P = NP) ---
# Se calcula el Error Estructural en la perfección (epsilon = 0)
EPSILON_SIN_ERROR = (D - N_PERFECCION) / D 
# EPSILON_SIN_ERROR es 0.0

# Probabilidad de éxito de UN solo paso
P_PASO_SIN_ERROR = 1 - EPSILON_SIN_ERROR # Será 1.0

# Probabilidad de éxito TOTAL para 4096 pasos
P_EXITO_SIN_ERROR = P_PASO_SIN_ERROR ** PASOS_NP

# --- 4. Generación del Gráfico de Prueba ---

etiquetas = ['TDH con Error\n($\mathbf{N < 4}$, $\mathbf{P \neq NP}$)', 
            'TDH sin Error\n($\mathbf{N = 4}$, $\mathbf{P = NP}$)']
probabilidades = [P_EXITO_CON_ERROR, P_EXITO_SIN_ERROR]

plt.figure(figsize=(9, 6))
barras = plt.bar(etiquetas, probabilidades, color=['red', 'green'], log=True)

# Añadir valor de probabilidad como texto
plt.text(barras[0].get_x() + barras[0].get_width()/2, 1e-15, 
         f'{P_EXITO_CON_ERROR:.2e}', ha='center', color='black', fontsize=12)
plt.text(barras[1].get_x() + barras[1].get_width()/2, 1e-1, 
         f'{P_EXITO_SIN_ERROR:.2f}', ha='center', color='black', fontsize=12)


plt.ylabel('Probabilidad de Éxito Total (Escala Logarítmica)')
plt.title(f'Prueba TDH: Colapso de P(Éxito NP) para n={N_INPUT} ({PASOS_NP} pasos)')
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.ylim(1e-20, 1.1)
plt.tight_layout()
plt.show()

# --- 5. Conclusiones ---
print("-" * 50)
print(f"Resultado TDH (Observable, P != NP):")
print(f"  Error Estructural (epsilon): {EPSILON_CON_ERROR:.6f}")
print(f"  Probabilidad de Éxito Total: {P_EXITO_CON_ERROR:.2e}")
print("\nResultado TDH (Abstracto, P = NP):")
print(f"  Error Estructural (epsilon): {EPSILON_SIN_ERROR:.6f}")
print(f"  Probabilidad de Éxito Total: {P_EXITO_SIN_ERROR:.2f}")