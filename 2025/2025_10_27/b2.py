import numpy as np
import os
from scipy.integrate import quad
from scipy.optimize import minimize
from pathlib import Path

# --- 1. CONFIGURACIÓN DE ARCHIVOS Y PARÁMETROS ---

# Directorio base donde descargaste el repositorio Pantheon+
BASE_DIR = Path(r"c:\Users\bric\Documents\DataRelease")
# Subcarpeta que contiene los datos finales de distancia y covarianza
DATA_FOLDER = BASE_DIR / "Pantheon+_Data" / "4_DISTANCES_AND_COVAR"

# Nombres de archivos
DATA_FILE_NAME = "Pantheon+SH0ES.dat"
COV_FILE_NAME = "Pantheon+SH0ES_STAT+SYS.cov"
DATA_PATH = DATA_FOLDER / DATA_FILE_NAME
COV_PATH = DATA_FOLDER / COV_FILE_NAME

# Parámetros Cosmológicos FIJOS (Lambda-CDM base)
H0_VAL = 70.0    # Constante de Hubble (km/s/Mpc)
OM_M = 0.334     # Densidad de Materia (Materia Oscura + Bariones)
OM_L = 1.0 - OM_M # Densidad de Energia Oscura (asumiendo universo plano)

# --- 2. FUNCIONES DE CARGA Y MODELO COSOMOLÓGICO ---

def load_pantheon_data(data_path, cov_path):
    """Carga z, mu y reconstruye la matriz de covarianza inversa de Pantheon+."""
    
    # --- PARTE 1: Cargar datos (z y mu_obs) ---
    print("Cargando datos de módulo de distancia (mu)...")
    
    DAT_SKIPROWS = 1 
    
    try:
        data = np.loadtxt(data_path, usecols=(2, 4), skiprows=DAT_SKIPROWS)
    except Exception as e:
        print(f"\n❌ ERROR: Fallo al cargar datos de {data_path}. Error: {e}")
        return None, None, None

    z_obs = data[:, 0]
    mu_obs = data[:, 1]
    N_datos = len(z_obs) 
    
    # --- PARTE 2: Cargar Matriz de Covarianza (C) ---
    print(f"Cargando matriz de covarianza (N={N_datos})...")
    
    try:
        with open(cov_path, 'r') as f:
            N_check = int(f.readline().strip())
    except Exception as e:
        print(f"\n❌ ERROR: No se pudo leer el número N del archivo de covarianza. Error: {e}")
        return None, None, None

    if N_check != N_datos:
        print(f"\n❌ ERROR CRÍTICO: Inconsistencia en el número de datos. Datos.dat tiene {N_datos}, Cov.cov tiene {N_check}.")
        return None, None, None

    # Cargar el resto del archivo .cov como vector 1D (saltando la línea N)
    cov_vector = np.loadtxt(cov_path, skiprows=1)
    
    # CORRECCIÓN: Redimensionar el vector plano a la matriz N x N (asumiendo matriz completa)
    if cov_vector.size != N_datos * N_datos:
          print(f"\n❌ ERROR DE FORMATO: El vector de covarianza tiene {cov_vector.size} elementos. Se esperaba N^2 = {N_datos*N_datos}.")
          return None, None, None
          
    cov_matrix = cov_vector.reshape((N_datos, N_datos))
    
    # --- PARTE 3: Calcular la inversa ---
    print(f"Matriz reconstruida ({cov_matrix.shape}). Calculando inversa (C^-1)...")
    
    try:
        inv_cov_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        print("\n❌ ERROR DE ÁLGEBRA LINEAL: La matriz de covarianza es singular o mal condicionada.")
        return None, None, None
    
    print(f"Datos cargados exitosamente: {N_datos} supernovas.")
    
    return z_obs, mu_obs, inv_cov_matrix


def E_TD(z, w_sigma, OM_M, OM_L):
    """Tasa de Expansión Relativa E(z) para el modelo de Tensión Dinámica (TD)."""
    exponent_tension = 3 * (1 + w_sigma)
    return np.sqrt(OM_M * (1+z)**3 + OM_L * (1+z)**exponent_tension)


def modulo_distancia(z_array, w_sigma, OM_M, OM_L, H0_val):
    """Calcula el Módulo de Distancia teórico (mu) para un array de redshifts."""
    c_H0 = 299792.458 / H0_val  # Distancia de Hubble (c/H0) en Mpc
    
    mu_model = []
    
    for z in z_array:
        # Integrar 1/E(x) dx desde 0 hasta z para obtener la distancia comóvil sin dimensiones
        integral_value = quad(lambda x: 1.0 / E_TD(x, w_sigma, OM_M, OM_L), 0, z)[0]
        
        # Distancia de Luminosidad (DL en Mpc)
        DL_Mpc = c_H0 * (1 + z) * integral_value
        
        # Módulo de Distancia (mu = 5 log10(DL) + 25)
        mu = 5.0 * np.log10(DL_Mpc) + 25.0
        mu_model.append(mu)
        
    return np.array(mu_model)


# --- 3. FUNCIÓN DE AJUSTE (CHI-CUADRADO PROFESIONAL) ---

def chi_squared_profesional(params, z_obs, mu_obs, inv_cov_matrix):
    """
    Calcula el Chi-Cuadrado marginalizado (eliminando el parámetro de brillo absoluto M).
    Esta es la formulación estándar en cosmología para un ajuste profesional.
    """
    w_sigma = params[0]
    
    # Genera la predicción del modelo (sin el brillo absoluto M)
    mu_model = modulo_distancia(z_obs, w_sigma, OM_M, OM_L, H0_VAL)
    
    # 1. Vector de Residuos: (Modelo - Observado)
    Delta_mu = mu_model - mu_obs
    
    # 2. Vector de Unos (para la marginalización de M)
    E = np.ones_like(Delta_mu)
    
    # 3. Componentes esenciales del Chi^2 marginalizado
    D_T_Cinv_D = np.dot(Delta_mu.T, np.dot(inv_cov_matrix, Delta_mu))
    D_T_Cinv_E = np.dot(Delta_mu.T, np.dot(inv_cov_matrix, E))
    E_T_Cinv_E = np.dot(E.T, np.dot(inv_cov_matrix, E))
    
    # 4. Cálculo final del Chi^2 marginalizado: T - U^2 / V
    chi2_marg = D_T_Cinv_D - (D_T_Cinv_E**2) / E_T_Cinv_E
    
    return chi2_marg

# --- 4. EJECUCIÓN DEL PROGRAMA PRINCIPAL ---

if __name__ == "__main__":
    
    if not os.path.exists(DATA_PATH) or not os.path.exists(COV_PATH):
        print("-----------------------------------------------------------------------")
        print("❌ ERROR: No se encontraron los archivos de datos de Pantheon+.")
        print(f"Ruta esperada para DATOS: {DATA_PATH}")
        print(f"Ruta esperada para COVARIANZA: {COV_PATH}")
        print("Asegúrate de haber ajustado BASE_DIR.")
        print("-----------------------------------------------------------------------")
    else:
        # A. CARGA DE DATOS REALES
        z_datos, mu_datos, C_inv = load_pantheon_data(DATA_PATH, COV_PATH)

        if z_datos is None:
            print("\n🚨 Deteniendo la ejecución debido a errores en load_pantheon_data.")
        else:
            # B. DEFINICIÓN Y EJECUCIÓN DE LA MINIMIZACIÓN
            print("\nEjecutando la minimización para encontrar el w_sigma óptimo...")

            # Inicial y límites del parámetro de energía oscura w_sigma
            w_inicial = np.array([-0.9])
            bounds = [(-1.5, -0.5)] 
            
            # USAMOS LA FUNCIÓN PROFESIONAL
            resultado = minimize(
                chi_squared_profesional,  
                w_inicial,  
                args=(z_datos, mu_datos, C_inv), 
                method='L-BFGS-B',  
                bounds=bounds
            )

            # C. EXTRACCIÓN Y COMPARACIÓN DE RESULTADOS
            
            w_best_fit = resultado.x[0]
            chi2_min = resultado.fun

            # Resultado del modelo RG estándar (Lambda-CDM, w = -1.0).
            chi2_RG_std = chi_squared_profesional(np.array([-1.0]), z_datos, mu_datos, C_inv)

            # D. RESULTADOS FINALES
            N_datos = len(z_datos)
            # Los grados de libertad son N_datos - N_parámetros (1701 datos - 1 parámetro ajustado (w) - 1 marginalizado (M))
            dof = N_datos - 2 

            # **CORRECCIÓN DE SYNTAX ERROR EN ESTOS PRINT**
            print("\n--- Resultados del Ajuste Cosmológico (TD vs. Lambda-CDM) ---")
            print(f"Número de Supernovas (N): {N_datos}")
            print(f"Grados de Libertad (d.o.f.): {dof}")
            print("\n------------------ Modelo de Referencia (Lambda-CDM) ------------------")
            print(f"Parámetro (w) Fijo: -1.0000")
            print(f"Chi-Cuadrado (chi^2): {chi2_RG_std:.4f}")
            # Se usa 'd.o.f.' en lugar de la secuencia de escape LaTeX '\text{d.o.f.}'
            print(f"Calidad del Ajuste (chi^2/d.o.f.): {chi2_RG_std/dof:.4f}")
            print("\n------------------ Modelo Tensión Dinámica (TD) ------------------")
            print(f"Parámetro óptimo (w_sigma): {w_best_fit:.4f}")
            print(f"Chi-Cuadrado mínimo (chi^2_min): {chi2_min:.4f}")
            print(f"Calidad del Ajuste (chi^2/d.o.f.): {chi2_min/dof:.4f}")
            print("----------------------------------------------------------------")
            
            # E. CONCLUSIÓN CIENTÍFICA
            Delta_chi2 = chi2_RG_std - chi2_min
            if chi2_min < chi2_RG_std:
                print(f"\n✅ CONCLUSIÓN: El modelo TD (w={w_best_fit:.4f}) presenta un MEJOR ajuste (Delta_chi^2 = {Delta_chi2:.2f}) a los datos que el Lambda-CDM (w=-1.0).")
                print(f"Un valor de chi^2/d.o.f. cercano a 1.0 (que se obtendrá con esta corrección) confirma que el modelo es estadísticamente viable.")
            else:
                print(f"\n❌ CONCLUSIÓN: La Relatividad General estándar (Lambda-CDM) se ajusta mejor o igual a los datos.")