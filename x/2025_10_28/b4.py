import numpy as np
from scipy.optimize import minimize
from scipy.linalg import inv
from scipy.integrate import quad

# --- RUTAS DE ARCHIVOS CORREGIDAS ---
# Usamos cadenas 'raw' (r"...") para evitar errores de secuencias de escape
DATA_FILE = r"C:\Users\bric\Documents\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES.dat"
COV_FILE = r"C:\Users\bric\Documents\DataRelease\Pantheon+_Data\4_DISTANCES_AND_COVAR\Pantheon+SH0ES_STAT+SYS.cov"

# 1. CARGA DE DATOS (z y mu) para determinar N_SN
try:
    # Columnas: 1 (zCMB), 3 (m_b_corr)
    data = np.loadtxt(DATA_FILE, skiprows=1, usecols=(4, 8)) 
    
    z_obs = data[:, 0]  # Redshift (zCMB)
    mB_obs = data[:, 1] # Magnitud aparente corregida (m_b_corr)
    N_SN = len(z_obs)
    
    print(f"Paso 1: Datos de Supernovas cargados. Número de SN (N_SN): {N_SN}")
except Exception as e:
    print(f"ERROR en Paso 1 (Carga de datos): {e}")
    exit()

# 2. CARGA Y REFORMA DE LA MATRIZ DE COVARIANZA (C)
try:
    # 💡 MEJORA: Saltamos la línea de encabezado (N) en el .cov (Línea 1)
    C_flat = np.loadtxt(COV_FILE, skiprows=1) 
    expected_size = N_SN * N_SN # 1701 * 1701 = 2893401
    
    if C_flat.size == expected_size:
        C = C_flat.reshape((N_SN, N_SN))
        print(f"Paso 2a: Matriz de covarianza C reformada. Dimensión final: {C.shape}")
    elif C_flat.size == expected_size + 1:
        # Corrección para el desajuste de 1 elemento (2893402 vs 2893401)
        print(f"Paso 2b: Se detecta elemento extra en C_flat ({C_flat.size}). Recortando el último.")
        C_flat = C_flat[:-1] 
        C = C_flat.reshape((N_SN, N_SN))
        print(f"Paso 2c: Matriz C reformada tras recorte. Dimensión final: {C.shape}")
    else:
        print(f"ERROR CRÍTICO: No se pudo reformar la matriz. Tamaño de C_flat: {C_flat.size}, Esperado: {expected_size}.")
        exit()
        
except Exception as e:
    print(f"ERROR en Paso 2 (Carga/Reforma de Covarianza): {e}")
    exit()

# 3. INICIALIZACIÓN DEL CÁLCULO
mu_obs = mB_obs 
try:
    C_inv = inv(C)
    print("Paso 3: Matriz de Covarianza Inversa (C_inv) calculada.")
except Exception as e:
    print(f"ERROR en Paso 3 (Cálculo de C_inv): {e}")
    exit()

# -------------------------------------------------------------
# --- FUNCIONES DE CÁLCULO COSOMOLÓGICO Y CHI^2 ---
# -------------------------------------------------------------
c = 299792.458 # Velocidad de la luz en km/s

def E_z(z, Omega_M, w_sigma):
    """Función de expansión E(z) para el modelo wCDM (o tu TD)."""
    Omega_DE = 1.0 - Omega_M 
    arg = Omega_M * (1 + z)**3 + Omega_DE * (1 + z)**(3 * (1 + w_sigma))
    if arg < 0: return np.inf
    return np.sqrt(arg)

def luminosity_distance(z, Omega_M, w_sigma):
    """Distancia de luminosidad D_L(z) en unidades de c/H0."""
    def integrand(zp): return 1.0 / E_z(zp, Omega_M, w_sigma)
    integral, _ = quad(integrand, 0, z)
    return (1.0 + z) * integral

def mu_model(z, Omega_M, w_sigma, M_offset):
    """Módulo de Distancia teórico mu(z)."""
    D_L_c_H0 = luminosity_distance(z, Omega_M, w_sigma)
    mu = 5.0 * np.log10(D_L_c_H0) + M_offset
    return mu

def chi2_function(params):
    """Calcula el Chi-Cuadrado: χ² = Δμᵀ ⋅ C⁻¹ ⋅ Δμ"""
    w_sigma, Omega_M, M_offset = params
    
    # Restricciones (Priors)
    if not (0.0 <= Omega_M <= 1.0) or not (-3.0 <= w_sigma <= 0.0):
        return np.inf

    mu_model_vec = np.array([mu_model(z, Omega_M, w_sigma, M_offset) for z in z_obs])
    Delta_mu = mu_model_vec - mu_obs
    chi2 = Delta_mu.T @ C_inv @ Delta_mu
    return chi2

# -------------------------------------------------------------
# --- 4. AJUSTE Y OBTENCIÓN DE CALIBRACIÓN ÓPTIMA ---
# -------------------------------------------------------------
print("\n--- Iniciando minimización con Powell (más robusto) ---")

# TD: Tensión Dimensional (w_sigma, Omega_M, M_offset son libres)
initial_guess_TD = [-0.95, 0.3, 25.0]
bounds_TD = [(-3.0, 0.0), (0.0, 1.0), (20.0, 30.0)]
# 💡 MEJORA: Usamos Powell para mejor convergencia que SLSQP
result_TD = minimize(chi2_function, initial_guess_TD, method='Powell', bounds=bounds_TD) 

# LCDM: Lambda CDM (Omega_M, M_offset son libres; w_sigma = -1.0)
def chi2_LCDM(params):
    Omega_M, M_offset = params
    return chi2_function([-1.0, Omega_M, M_offset])
initial_guess_LCDM = [0.3, 25.0]
bounds_LCDM = [(0.0, 1.0), (20.0, 30.0)]
result_LCDM = minimize(chi2_LCDM, initial_guess_LCDM, method='Powell', bounds=bounds_LCDM)


# -------------------------------------------------------------
# --- 5. VISUALIZACIÓN DE RESULTADOS Y CONCLUSIÓN ---
# -------------------------------------------------------------

print("\n===============================================")
print("✅ ANÁLISIS DE CALIBRACIÓN Y PRECISIÓN (M_offset)")
print("===============================================")

# Extracción de resultados para BIC
chi2_min_TD = result_TD.fun if result_TD.success else np.inf
chi2_min_LCDM = result_LCDM.fun if result_LCDM.success else np.inf
k_TD = 3 # Parámetros libres: w_sigma, Omega_M, M_offset
k_LCDM = 2 # Parámetros libres: Omega_M, M_offset
BIC_TD = chi2_min_TD + k_TD * np.log(N_SN)
BIC_LCDM = chi2_min_LCDM + k_LCDM * np.log(N_SN)

# --- Calibración Óptima y Chi^2/dof ---
M_B_SH0ES_REF = 25.0 
print(f"Calibración de Referencia (M_offset): {M_B_SH0ES_REF:.4f}")

if result_TD.success:
    w_sigma_fit, Omega_M_fit, M_offset_TD_optima = result_TD.x
    dof_TD = N_SN - k_TD
    chi2_dof_TD = chi2_min_TD / dof_TD
    print(f"\n1. Modelo TD:")
    print(f"  Calibración Óptima = {M_offset_TD_optima:.4f}")
    print(f"  Mejor w_sigma: {w_sigma_fit:.4f}, Mejor Ω_M: {Omega_M_fit:.4f}")
    print(f"  BIC: {BIC_TD:.2f} (χ²/dof: {chi2_dof_TD:.2f})")
else:
    print("\n1. Modelo TD: Fallo en la convergencia.")

if result_LCDM.success:
    Omega_M_LCDM, M_offset_LCDM_optima = result_LCDM.x
    dof_LCDM = N_SN - k_LCDM
    chi2_dof_LCDM = chi2_min_LCDM / dof_LCDM
    print(f"\n2. Modelo ΛCDM:")
    print(f"  Calibración Óptima = {M_offset_LCDM_optima:.4f}")
    print(f"  Mejor Ω_M: {Omega_M_LCDM:.4f}")
    print(f"  BIC: {BIC_LCDM:.2f} (χ²/dof: {chi2_dof_LCDM:.2f})")
else:
    print("\n2. Modelo ΛCDM: Fallo en la convergencia.")

print("\n-----------------------------------------------")
print("CONCLUSIÓN DE PRECISIÓN Y CALIBRACIÓN")
print("-----------------------------------------------")

# Se define el modelo preferido
if BIC_TD < BIC_LCDM:
    modelo_preferido = "Tensión Dimensional (TD)"
    M_offset_TD_optima = result_TD.x[2] if result_TD.success else 0.0
    M_offset_LCDM_optima = result_LCDM.x[1] if result_LCDM.success else 0.0
    diferencia = M_offset_TD_optima - M_offset_LCDM_optima
elif BIC_LCDM < BIC_TD:
    modelo_preferido = "Lambda CDM (ΛCDM)"
    M_offset_TD_optima = result_TD.x[2] if result_TD.success else 0.0
    M_offset_LCDM_optima = result_LCDM.x[1] if result_LCDM.success else 0.0
    diferencia = M_offset_TD_optima - M_offset_LCDM_optima
else:
    modelo_preferido = "Ambos"
    diferencia = 0.0

print(f"🏆 El modelo más preciso (BIC más bajo) es: **{modelo_preferido}**.")
if result_TD.success and result_LCDM.success:
    print(f"Diferencia de Calibración: M_offset(TD)={M_offset_TD_optima:.4f} - M_offset(ΛCDM)={M_offset_LCDM_optima:.4f} = **{diferencia:.4f}**.")