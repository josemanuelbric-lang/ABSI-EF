import numpy as np

N = 3.8710
D = 4.0
F = 3.0

# Factor de Tensión Geométrica (F_TG)
F_TG = 1 / np.log(N)

# Constante de Estructura Fina (alpha^-1)
alpha_inversa_predicha = (D * F)**D * F_TG * np.log(D * F)

alpha_inversa_observada = 137.036

print(f"--- Solución al Problema de Estructura Fina ---")
print(f"alpha^-1 Predicho (TDH): {alpha_inversa_predicha:.3f}")
print(f"alpha^-1 Observado: {alpha_inversa_observada:.3f}")
print(f"Error de Predicción: {abs(alpha_inversa_predicha - alpha_inversa_observada):.2e}")