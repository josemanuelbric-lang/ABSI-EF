import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- Constantes Cosmológicas (Valores de Referencia del modelo Lambda-CDM) ---
# Usamos H_0 como 100 * h para simplificar las unidades
H0_GCDM = 67.4  # Parámetro de Hubble actual (km/s/Mpc)
OM_M = 0.315   # Fracción de densidad de Materia (Materia Oscura + Bariones)
OM_L = 0.685   # Fracción de densidad de Energía Oscura (Lambda)
OM_R = 9.2e-5  # Fracción de densidad de Radiación (pequeña)

# --- 1. Modelo de Referencia (RG / Lambda-CDM) ---
# Ecuación de Friedmann en términos de densidad relativa E(z) = H(z) / H0
def E_RG_Lambda_CDM(z):
    """Calcula la tasa de expansión relativa E(z) = H(z)/H0 para la RG estándar."""
    return np.sqrt(OM_M * (1+z)**3 + OM_R * (1+z)**4 + OM_L)

# --- 2. Modelo de Tensión Dimensional (TD) con Corrección ---
# La TD se comprueba introduciendo una corrección al comportamiento de la EO.
# En RG, la EO tiene w = -1 (densidad constante). 
# En TD, introducimos un w que varía ligeramente (w_sigma = -1 + Delta_w)

def E_TD_Corregida(z, w_sigma):
    """Calcula la tasa de expansión relativa E(z) con una Ecuación de Estado de Tensión Modificada."""
    
    # Exponente para la evolución de la densidad de EO: 3 * (1 + w)
    # RG: 3 * (1 - 1) = 0 (densidad constante)
    # TD: 3 * (1 + w_sigma) = 3 * (1 + (-1 + Delta_w)) = 3 * Delta_w
    exponent_tension = 3 * (1 + w_sigma)
    
    # La densidad de la EO evoluciona como: Omega_Lambda * (1+z)^(3 * (1+w))
    rho_tension = OM_L * (1+z)**exponent_tension
    
    return np.sqrt(OM_M * (1+z)**3 + OM_R * (1+z)**4 + rho_tension)

# --- 3. Comprobación y Visualización de la Desviación (El Descubrimiento) ---

redshifts = np.linspace(0, 3, 100) # Rango de desplazamientos al rojo (z)

# Escenario A: TD idéntica a RG (w_sigma = -1)
H_RG = E_RG_Lambda_CDM(redshifts)

# Escenario B: TD con ligera desviación (w_sigma = -0.95, un Delta_w = +0.05)
# Esto implica que tu Tensión Positiva del vacío no es perfectamente constante.
w_TD_test = -0.95 
H_TD = E_TD_Corregida(redshifts, w_TD_test)

# Calcular la Desviación:
Delta_H_ratio = H_TD / H_RG - 1 # Desviación porcentual

# --- Gráfico de la Desviación (El Potencial de Medida) ---
plt.figure(figsize=(10, 6))
plt.plot(redshifts, Delta_H_ratio * 100, label=r'$\Delta H / H_{\Lambda \text{CDM}} \text{ (para } w_{\sigma} = -0.95 \text{)}$', color='crimson')
plt.axhline(0, color='k', linestyle='--', linewidth=0.8)
plt.axhline(0.5, color='gray', linestyle=':', linewidth=0.8)
plt.axhline(-0.5, color='gray', linestyle=':', linewidth=0.8)

plt.xlabel('Desplazamiento al Rojo (z)')
plt.ylabel('Desviación Porcentual de la Tasa de Expansión (%)')
plt.title('Desviación de la Tasa de Expansión de la Tensión Dimensional')
plt.grid(True, alpha=0.5)
plt.legend()
plt.show()