import numpy as np

# --- 1. Equivalencias y Constantes (Analogía con la RG) ---

# Constantes Físicas Reales (para obtener un valor físico conocido)
G = 6.67408e-11   # Constante Gravitacional (m^3 kg^-1 s^-2)
c = 299792458     # Velocidad de la Luz (m/s)

# Parámetros del Sol
M_sol = 1.989e30  # Masa del Sol (kg)

# --- 2. Parámetros de la Tensión Dimensional (TD) Ajustados ---

# Tensión (sigma) ajustada a la Masa (M)
# (Asumimos sigma = G * M para que la aceleración sea la misma que la Newtoniana)
sigma_sol = G * M_sol

# Constante de Ajuste (alpha)
# (Asumimos alpha = 2 / c^2 para que la dilatación del tiempo coincida con la RG)
ALPHA_TD = 2 / (c**2)

# --- 3. Cálculo del Horizonte de Tensión (r_H) ---

# r_H = alpha * sigma 
r_H = ALPHA_TD * sigma_sol

# Nota: Este cálculo es matemáticamente idéntico al Radio de Schwarzschild (r_s = 2GM/c^2).
r_s_check = (2 * G * M_sol) / (c**2)

print("--- El Fenómeno del Horizonte de Sucesos (Agujero de Tensión) ---")
print(f"1. Tensión de la Fuente (sigma) del Sol (análoga a GM): {sigma_sol:.4e} m^3/s^2")
print(f"2. Constante de Tensión (alpha): {ALPHA_TD:.4e} s^2/m")
print("-" * 50)
print(f"La Distancia del Horizonte de Tensión (r_H) es r_H = alpha * sigma:")
print(f"r_H = {r_H:.10f} metros")
print(f"(Comprobación: Radio de Schwarzschild r_s = {r_s_check:.10f} metros)")