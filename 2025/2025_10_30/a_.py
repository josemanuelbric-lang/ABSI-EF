import numpy as np
import matplotlib.pyplot as plt

# --- Constantes TDH ---
D = 4      # Dimensionalidad
F = 3      # Familias
N_real = 3.8710 # Tensión Maestra Real

# --- Rango de Tensión (Eje X) ---
N_sim = np.linspace(3.0, 4.0, 100) # Simular N de 3.0 a 4.0

# --- 1. L.E. Electromagnética (Alpha^-1) ---
# Formula: (D^F + F^D) - N * (1 + N/D)
alpha_inv_tdh = (D**F + F**D) - (N_sim * (1 + N_sim / D))

# --- 2. L.E. Nuclear Fuerte (Alpha_s) ---
# Formula: (F * (D - N)) / (D + F - N)
# Asegurar que el denominador no sea cero cerca de N=7
alpha_s_tdh = (F * (D - N_sim)) / (D + F - N_sim)

# --- 3. L.E. Nuclear Débil (Masa del Bosón W, mW) ---
# Formula: (F^D * D) / N
mW_tdh = (F**D * D) / N_sim

# --- 4. L.E. Gravitatoria (Exponente Jerárquico E_36) ---
# Formula: (D * F * ((D * F) / N)) - ((D**F) / (N**F))
E_36_tdh = (D * F * ((D * F) / N_sim)) - ((D**F) / (N_sim**F))

# --- Creación de la Gráfica Visual ---
plt.figure(figsize=(14, 10))

# Subgráfico 1: Fuerza Electromagnética y Nuclear Fuerte (Escala Pequeña)
plt.subplot(2, 2, 1)
plt.plot(N_sim, alpha_inv_tdh, label='Electromagnética (Alpha^-1)', color='blue')
plt.axvline(x=N_real, color='grey', linestyle='--', label=f'N Real ({N_real})')
plt.axhline(y=137.036, color='blue', linestyle=':', label='Alpha^-1 Observado (137.0)')
plt.axhline(y=0.118, color='red', linestyle=':', label='Alpha_s Observado (0.118)')
plt.plot(N_sim, alpha_s_tdh * 100, label='Nuclear Fuerte (Alpha_s x 100)', color='red') # Multiplicado por 100 para visualizar
plt.title('Fuerzas Acopladas (EM y Fuerte)')
plt.xlabel('Tensión Maestra Simulada (N)')
plt.ylabel('Valor de la Constante')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Subgráfico 2: Fuerza Nuclear Débil (Masa W)
plt.subplot(2, 2, 2)
plt.plot(N_sim, mW_tdh, label='Nuclear Débil (Masa W)', color='green')
plt.axvline(x=N_real, color='grey', linestyle='--')
plt.axhline(y=80.379, color='green', linestyle=':', label='Masa W Observada (80.4 GeV)')
plt.title('Masa del Bosón W vs. Tensión (N)')
plt.xlabel('Tensión Maestra Simulada (N)')
plt.ylabel('Masa (GeV)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Subgráfico 3: Fuerza Gravitatoria (Jerarquía E_36)
plt.subplot(2, 2, 3)
plt.plot(N_sim, E_36_tdh, label='Gravitatoria (Exponente E_36)', color='purple')
plt.axvline(x=N_real, color='grey', linestyle='--')
plt.axhline(y=36.0, color='purple', linestyle=':', label='E_36 Observado (36)')
plt.title('Jerarquía Gravitatoria vs. Tensión (N)')
plt.xlabel('Tensión Maestra Simulada (N)')
plt.ylabel('Exponente Jerárquico')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
#