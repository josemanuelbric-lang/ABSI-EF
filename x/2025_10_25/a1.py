import numpy as np
import matplotlib.pyplot as plt

# --- 1. Equivalencias y Constantes (Analogía con la RG) ---
# Define las constantes fundamentales del sistema TD/RG
G = 6.67408e-11   # Constante Gravitacional (m^3 kg^-1 s^-2)
c = 299792458     # Velocidad de la Luz (m/s)

# Parámetros del Sol
M_sol = 1.989e30  # Masa del Sol (kg)

# --- 2. Parámetros de la Tensión Dimensional (TD) Ajustados ---
# Tensión (sigma) ajustada a la Masa (M)
# sigma = G * M
sigma_sol = G * M_sol

# Constante de Ajuste (alpha)
# alpha = 2 / c^2
ALPHA_TD = 2 / (c**2)

# --- 3. Cálculo del Horizonte de Tensión (r_H) ---
# r_H = alpha * sigma 
r_H_actual = ALPHA_TD * sigma_sol

print("--- Horizonte de Sucesos (Agujero de Tensión) ---")
print(f"Radio Calculado r_H: {r_H_actual:.4f} metros (Aprox. 2.95 km)")

# --- 4. Función de Dilatación Temporal (TD) ---

def tasa_tiempo_td(r, sigma, alpha):
    """
    Función de la Tasa de Tiempo Local: dtau/dt = sqrt(1 - alpha * sigma / r).
    """
    # Garantizar que r sea un array si es un escalar
    if np.isscalar(r):
        r = np.array([r])
        
    tasa = np.zeros_like(r, dtype=float)
    
    # El cálculo solo es válido donde r > r_H
    r_H_calc = alpha * sigma
    valid_indices = r > r_H_calc
    
    # Calcula el potencial normalizado y la tasa
    potencial_norm = (alpha * sigma) / r[valid_indices]
    tasa[valid_indices] = np.sqrt(1.0 - potencial_norm)
    
    return tasa

# --- 5. Generación de Datos para el Gráfico ---

# Rango de distancias, comenzando justo después de r_H y yendo hasta 10 veces r_H
r_min = r_H_actual * 1.000000001 # Empezamos infinitesimalmente fuera del Horizonte
r_max = r_H_actual * 10000 

r_valores = np.logspace(np.log10(r_min), np.log10(r_max), 500)

# Calcula la Tasa de Tiempo Local
tasa_valores = tasa_tiempo_td(r_valores, sigma_sol, ALPHA_TD)

# --- 6. Gráfico de Visualización ---

plt.figure(figsize=(10, 6))

# Gráfico de la Tasa de Tiempo Local vs Distancia (logarítmica)
plt.plot(r_valores / r_H_actual, tasa_valores, color='blue', linewidth=3, 
         label=r'Tasa $\Delta\tau/\Delta t$')

# Línea del Horizonte de Sucesos (r = r_H)
plt.axvline(x=1.0, color='red', linestyle='--', 
            label=r'$r = r_H$ ($\Delta\tau/\Delta t = 0$)')

# Línea del Tiempo Plano (lejos)
plt.axhline(y=1.0, color='gray', linestyle=':', label='Tiempo Plano (1.0)')

plt.title('Colapso de la Coordenada Temporal cerca del Horizonte de Tensión')
plt.xlabel(r'Distancia Normalizada ($r / r_H$)')
# Nota: Usar r'Tasa $\Delta\\tau/\Delta t$' en lugar de 'Tasa $\Delta\tau/\Delta t$'
# para evitar el 'SyntaxWarning: invalid escape sequence' de Python 3.
plt.ylabel(r'Tasa de Tiempo Local ($\Delta\tau/\Delta t$)') 

plt.xlim(0.999999, 100) # Enfocamos el gráfico cerca del Horizonte
plt.ylim(-0.05, 1.05)
plt.grid(True, which="major", linestyle='--')
plt.legend()
plt.xscale('log') # Escala logarítmica para ver el acercamiento al Horizonte
plt.show()