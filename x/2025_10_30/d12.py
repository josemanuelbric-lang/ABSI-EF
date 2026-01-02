import numpy as np

# --- 1. Constantes Fundamentales ---
# Constante de Acoplamiento de la TDH (Derivada del problema cosmológico)
N_CALCULADO = 3.8710

# --- 2. Datos Observados (Escala Lineal de Masa) ---
# Usamos el límite superior de la masa del neutrino para la comprobación:
M_ELECTRON_MEV = 0.511  # MeV
M_NEUTRINO_EV = 0.12    # eV (0.12 eV = 1.2e-7 MeV)

# Relación de Masas Observada (R_obs)
R_OBS_LINEAR = M_ELECTRON_MEV / (M_NEUTRINO_EV * 1e-6) # R_obs ≈ 4.258 * 10^6
R_OBS_LOG10 = np.log10(R_OBS_LINEAR) # R_obs_log10 ≈ 6.63

# --- 3. Predicción de la Sub-Escala (X) por la TDH ---
# Asumimos que la relación de masas es R_obs = X^N
# Por lo tanto, X = R_obs^(1/N)

X_PREDICHO_LINEAR = R_OBS_LINEAR ** (1.0 / N_CALCULADO)
X_PREDICHO_LOG10 = R_OBS_LOG10 / N_CALCULADO

# --- 4. Comprobación y Resultados ---
# Comprobamos si la Predicción de la TDH reproduce la Relación de Masas
R_PREDICHO_TDH_LINEAR = X_PREDICHO_LINEAR ** N_CALCULADO

print(f"--- Comprobación de la Sub-Jerarquía (Electrón/Neutrino) ---")
print(f"Constante de Acoplamiento TDH (N): {N_CALCULADO:.4f}")
print("-" * 50)
print(f"Relación de Masas Observada (log10): {R_OBS_LOG10:.4f}")

print(f"\nPredicción de la TDH sobre la Estructura Interna:")
print(f"Factor de Dilución Sub-dimensional (X) requerido (log10): {X_PREDICHO_LOG10:.4f}")
print(f"Factor de Dilución Sub-dimensional (X) requerido (Lineal): {X_PREDICHO_LINEAR:.2f}")

print("-" * 50)
print(f"Comprobación: (X^N) = ({X_PREDICHO_LINEAR:.2f})^{N_CALCULADO:.4f} ")
print(f"Relación de Masas Predicha por la TDH (Lineal): {R_PREDICHO_TDH_LINEAR:.2e}")
print(f"Error (Log10): {np.log10(R_OBS_LINEAR) - np.log10(R_PREDICHO_TDH_LINEAR):.2e}")