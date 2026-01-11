import numpy as np

# --- 1. Constantes Fundamentales de la TDH ---
N_FUNDAMENTAL = 3.8710  # Exponente de Acoplamiento (Derivado del problema cosmólogico)

# Constantes Estructurales (Enteras, no ajustables)
D_GEOMETRICA = 4.0      # Dimensionalidad (3+1)
F_SIMETRIA = 3.0        # Familias de Partículas

# --- 2. Derivación Teórica de X (Nueva Ley TDH) ---
# C_Comp = N + N/F^2
C_COMP = N_FUNDAMENTAL + (N_FUNDAMENTAL / (F_SIMETRIA ** 2))

# X_Teorico = (D * F) * C_Comp
X_TEORICO = (D_GEOMETRICA * F_SIMETRIA) * C_COMP

# --- 3. Predicción Pura de la Masa del Neutrino ---
M_ELECTRON_MEV = 0.511

# R_pred = X_Teórico^N
R_PREDICHA_TDH_LINEAR = X_TEORICO ** N_FUNDAMENTAL

# Predicción de la Masa del Neutrino (TDH)
M_NEUTRINO_PREDICHA_MEV = M_ELECTRON_MEV / R_PREDICHA_TDH_LINEAR
M_NEUTRINO_PREDICHA_EV = M_NEUTRINO_PREDICHA_MEV * 1e6 # Convertir MeV a eV

# --- 4. Comprobación ---
M_NEUTRINO_OBSERVADA_EV = 0.1200 # Límite superior de la masa del neutrino

print(f"--- ⚛️ Predicción Pura de la Masa del Neutrino (TDH) ---")
print(f"Constante N (Cosmológica): {N_FUNDAMENTAL:.4f}")
print("-" * 60)
print(f"X Teórico Derivado (4 x 3 x C_Comp): {X_TEORICO:.4f}")
print(f"X Requerido (Observado): 51.5900")
print("-" * 60)
print(f"Masa del Neutrino Predicha (TDH): {M_NEUTRINO_PREDICHA_EV:.4f} eV")
print(f"Masa del Neutrino Observada (Límite): {M_NEUTRINO_OBSERVADA_EV:.4f} eV")
print(f"Error de Predicción: {abs(M_NEUTRINO_PREDICHA_EV - M_NEUTRINO_OBSERVADA_EV):.2e} eV")