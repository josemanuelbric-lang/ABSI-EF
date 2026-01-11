import numpy as np

# --- Constantes Universales (para RG) ---
G = 6.674e-11  # Constante Gravitacional (m^3 kg^-1 s^-2)
c = 299792458  # Velocidad de la Luz (m/s)

# --- Parámetros de la Fuente (Masa/Tensión) ---
# Usamos un valor análogo al Sol (M_sol)
M_sol = 1.989e30  # Masa del Sol (kg)

# --- Parámetros de la Tensión Dimensional (TD) ---
# Suponemos que TU Tensión (sigma) es proporcional a la Masa (M)
sigma_sol = G * M_sol  # Asumimos sigma = GM (para igualar la aceleración Newtoniana)
ALPHA_TD = 2 / (c**2)  # Asumimos alpha = 2/c^2 (para igualar la dilatación del tiempo)

def dilatacion_tiempo_RG(r, M):
    """
    Calcula la tasa de tiempo local (sqrt(g_00)) según la Relatividad General.
    rg_factor = 2GM / (c^2 r)
    """
    rg_factor = (2 * G * M) / (c**2 * r)
    # Debe ser 1 - factor (el tiempo se ralentiza)
    return np.sqrt(1 - rg_factor) if rg_factor < 1 else 0.0

def dilatacion_tiempo_TD(r, sigma, alpha):
    """
    Calcula la tasa de tiempo local (dtau/dt) según tu modelo de Tensión Dimensional.
    potencial_norm = alpha * sigma / r
    """
    # El potencial de Tensión que causa el efecto
    potencial_norm = (alpha * sigma) / r
    # Tu fórmula es 1 - potencial_norm (que debe ser positivo)
    return np.sqrt(1 - potencial_norm) if potencial_norm < 1 else 0.0

# --- Comparación a una Distancia Fija (Analogía) ---
# Distancia radial grande, p. ej., 1000 veces el radio de Schwarzschild (1000 * 3000 m para el Sol)
R_TEST = 300000000.0 # 300,000 km (para obtener un factor significativo)

# 1. Tasa de Tiempo Local (TD)
tasa_td = dilatacion_tiempo_TD(R_TEST, sigma_sol, ALPHA_TD)
print(f"Predicción TD (con ajustes): dtau/dt = {tasa_td:.15f}")

# 2. Tasa de Tiempo Local (RG)
tasa_rg = dilatacion_tiempo_RG(R_TEST, M_sol)
print(f"Predicción RG (Schwarzschild): dtau/dt = {tasa_rg:.15f}")

# 3. Diferencia
diferencia = abs(tasa_td - tasa_rg)
print(f"\nDiferencia Absoluta: {diferencia:.20e}")

# Si la diferencia es muy cercana a cero, tu modelo TD es formalmente idéntico a la RG en el campo estático.