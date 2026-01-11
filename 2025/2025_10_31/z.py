import numpy as np
import matplotlib.pyplot as plt

# --- 1. Constantes de la TDH ---
D = 4.0
F = 3.0
N = 3.8710

# --- 2. Cálculo del Límite Estructural de Complejidad (L_max) ---
D_deficit = D - N
L_max_TDH = F / D_deficit

print(f"Déficit Dimensional (D - N): {D_deficit:.4f}")
print(f"Límite de Complejidad TDH (L_max): {L_max_TDH:.2f}")
print("-" * 50)

# --- 3. Modelado de Tiempos de Ejecución ---
# N_size: Tamaño del Input del problema (e.g., número de variables)
N_size = np.arange(1, 15)

# Tiempo Polinomial (P): n^2
T_P = N_size**2 

# Tiempo No Polinomial (NP): 2^n (Ejemplo de NP-Completo, como el problema del vendedor viajero)
T_NP = 2**N_size 

# --- 4. Visualización ---
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(N_size, T_P, label=r'Tiempo Polinomial ($n^2$)', marker='o', color='green')
ax.plot(N_size, T_NP, label=r'Tiempo No Polinomial ($2^n$)', marker='x', color='red')

# Línea del Límite Estructural TDH (L_max)
ax.axhline(L_max_TDH, color='blue', linestyle='--', linewidth=2, 
           label=f'Límite de Complejidad TDH ($\mathbf{{L_{{max}}}} \\approx {L_max_TDH:.2f}$)')

ax.set_yscale('log') # Usamos escala logarítmica para ver la diferencia de crecimiento
ax.set_xlabel('Tamaño del Input ($n$)')
ax.set_ylabel('Tiempo de Ejecución (Escala Logarítmica)')
ax.set_title('Modelado de P vs. NP y Límite de Complejidad Estructural (TDH)')
ax.legend()
ax.grid(True, linestyle='dotted')
plt.show()
#