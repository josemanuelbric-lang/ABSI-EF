import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

# --- Constantes Cosmológicas Fijas (Lambda-CDM base) ---
H0_VAL = 70.0    # Simplificamos H0 (km/s/Mpc)
OM_M = 0.3       # Densidad de Materia
OM_L = 0.7       # Densidad de Energia Oscura
# La velocidad de la luz c se incluye implícitamente en la integral de distancia

# --- 1. DATOS REALES SIMULADOS (basados en SNIa) ---
# z_datos: Redshifts (z) donde se midieron las supernovas
z_datos = np.array([0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]) 

# mu_datos: Módulo de Distancia (mu = m - M) observado en cada z
mu_datos = np.array([37.0, 40.2, 41.9, 43.1, 44.4, 46.0, 47.1])

# sigma_mu: Error de medición (incertidumbre)
sigma_mu = np.array([0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25])


# --- 2. MODELO DE TENSION DIMENSIONAL (TD) ---

def E_TD(z, w_sigma):
    """Calcula la tasa de expansión relativa E(z) para la TD (EO dinámica)."""
    exponent_tension = 3 * (1 + w_sigma)
    return np.sqrt(OM_M * (1+z)**3 + OM_L * (1+z)**exponent_tension)

# FUNCIÓN ESCALAR (SÓLO PARA UN ÚNICO VALOR DE Z)
def _distancia_luminosidad_scalar(z_single, w_sigma):
    """
    Calcula la Distancia de Luminosidad (DL) para el modelo TD 
    para un *único* valor de z.
    """
    # quad necesita límites de integración escalares, no arrays.
    integral_value = quad(lambda x: 1.0 / E_TD(x, w_sigma), 0, z_single)[0]
    
    # Distancia de Luminosidad sin dimensiones: DL/D_H = (1+z) * DC/D_H
    return (1 + z_single) * integral_value 

# VECTORIZAMOS LA FUNCIÓN PARA QUE PUEDA ACEPTAR EL ARRAY z_datos
distancia_luminosidad = np.vectorize(_distancia_luminosidad_scalar)

def modulo_distancia(z, w_sigma, H0_val):
    """
    Calcula el módulo de distancia (mu) teórico: mu = 5 log10(DL) + 25
    Donde DL está en Mpc.
    """
    # Constante de Hubble en unidades adecuadas para Mpc (c/H0)
    c_H0 = 299792.458 / H0_val # c en km/s, H0 en km/s/Mpc -> c/H0 en Mpc
    
    # Esta función ahora acepta un array 'z' gracias a np.vectorize
    DL_Mpc = c_H0 * distancia_luminosidad(z, w_sigma)
    
    return 5.0 * np.log10(DL_Mpc) + 25.0

# --- 3. FUNCIÓN CHI-CUADRADO (Métricas de Ajuste) ---

def chi_squared(w_sigma):
    """Calcula el Chi-Cuadrado sumando los residuos al cuadrado ponderados por el error."""
    
    # Generar las predicciones mu_modelo para el w_sigma dado
    mu_modelo = modulo_distancia(z_datos, w_sigma, H0_VAL)
    
    # Calcular Chi-Cuadrado
    chi2 = np.sum(((mu_modelo - mu_datos) / sigma_mu)**2)
    return chi2

# --- 4. OPTIMIZACIÓN Y RESULTADOS ---

w_inicial = np.array([-0.9]) # Debe ser un array si se usa con bounds en Nelder-Mead (aunque scipy lo gestiona en versiones recientes)

# Usamos la función minimize para encontrar el w_sigma que minimiza chi_squared
resultado = minimize(chi_squared, w_inicial, method='Nelder-Mead', bounds=[(-1.5, -0.5)])

# Extraer el mejor ajuste
w_best_fit = resultado.x[0]
chi2_min = resultado.fun

# ----------------------------------------------------
# Comparación con la RG estándar (w = -1)
# ----------------------------------------------------
chi2_RG_std = chi_squared(-1.0)

print(f"--- Análisis de la Tensión Dimensional (TD) vs. RG ---")
print(f"Chi-Cuadrado de la RG estándar (w = -1.0):       {chi2_RG_std:.4f}")
print(f"Mejor valor de Tensión (w_sigma) encontrado:     {w_best_fit:.4f}")
print(f"Chi-Cuadrado mínimo para la TD (w = {w_best_fit:.4f}): {chi2_min:.4f}")

if chi2_min < chi2_RG_std:
    print("\n✅ CONCLUSIÓN: ¡El modelo de Tensión Dinámica (TD) se ajusta MEJOR a los datos simulados que la RG estándar!")
    print(f"El mejor ajuste indica que la Tensión Positiva de la EO es DINÁMICA ({w_best_fit:.4f}).")
else:
    print("\n❌ CONCLUSIÓN: La RG estándar se ajusta igual o mejor a los datos simulados. Se requiere más precisión.")