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
    
    # CORRECCIÓN CRÍTICA FINAL: Ajustando skiprows a 1 para cargar los 1701 datos.
    DAT_SKIPROWS = 1 
    
    try:
        # Columna 2: Z_CMB (redshift)
        # Columna 4: MU (Módulo de Distancia Observado)
        data = np.loadtxt(data_path, usecols=(2, 4), skiprows=DAT_SKIPROWS)
    except Exception as e:
        print(f"\n❌ ERROR: Fallo al cargar datos de {data_path}. Revise 'skiprows={DAT_SKIPROWS}' en el .dat. Error: {e}")
        return None, None, None

    z_obs = data[:, 0]
    mu_obs = data[:, 1]
    N_datos = len(z_obs) 
    
    # --- PARTE 2: Cargar Matriz de Covarianza (C) ---
    print(f"Cargando matriz de covarianza (N={N_datos})...")
    
    # 1. Leer N del archivo .cov para validar.
    try:
        with open(cov_path, 'r') as f:
            N_check = int(f.readline().strip())
    except Exception as e:
        print(f"\n❌ ERROR: No se pudo leer el número N del archivo de covarianza. Error: {e}")
        return None, None, None

    # Verificación de consistencia (ahora esperamos N_datos == 1701)
    if N_check != N_datos:
        print(f"\n❌ ERROR CRÍTICO: Inconsistencia en el número de datos. Datos.dat tiene {N_datos}, Cov.cov tiene {N_check}.")
        return None, None, None

    # 2. Cargar el resto del archivo .cov como vector 1D (saltando la línea N)
    # **Importante: skiprows=1 funciona porque el N_check ya leyó la primera línea.**
    cov_vector = np.loadtxt(cov_path, skiprows=1)
    
    # 3. Reconstruir la matriz simétrica N x N 
    # 💥 CORRECCIÓN DEL ERROR CRÍTICO AQUÍ:
    # EL ARCHIVO .cov DE PANTHEON+ CONTIENE LA MATRIZ COMPLETA N^2 APLANADA (NO SOLO EL TRIÁNGULO INFERIOR).
    if cov_vector.size != N_datos * N_datos:
         print(f"\n❌ ERROR DE FORMATO: El vector de covarianza tiene {cov_vector.size} elementos, pero se esperaban {N_datos*N_datos} (Matriz completa) o {N_datos*(N_datos+1)//2} (Triángulo inferior).")
         return None, None, None
         
    # Redimensionar el vector plano a la matriz N x N
    cov_matrix = cov_vector.reshape((N_datos, N_datos))
    
    # --- PARTE 3: Calcular la inversa ---
    print(f"Matriz reconstruida ({cov_matrix.shape}). Calculando inversa (C^-1)...")
    
    # Se añade un manejo de error para matrices mal condicionadas (aunque poco probable aquí)
    try:
        inv_cov_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        print("\n❌ ERROR DE ÁLGEBRA LINEAL: La matriz de covarianza es singular o mal condicionada.")
        return None, None, None
    
    print(f"Datos cargados exitosamente: {N_datos} supernovas.")
    
    return z_obs, mu_obs, inv_cov_matrix


def E_TD(z, w_sigma, OM_M, OM_L):
    """
    Tasa de Expansión Relativa E(z) para el modelo de Tensión Dinámica (TD).
    Modelo: H(z)^2 / H0^2 = Omega_M * (1+z)^3 + Omega_L * (1+z)^(3(1+w_sigma))
    """
    exponent_tension = 3 * (1 + w_sigma)
    return np.sqrt(OM_M * (1+z)**3 + OM_L * (1+z)**exponent_tension)


def modulo_distancia(z_array, w_sigma, OM_M, OM_L, H0_val):
    """
    Calcula el Módulo de Distancia teórico (mu) para un array de redshifts.
    mu = 5 log10(DL) + 25
    """
    c_H0 = 299792.458 / H0_val  # Distancia de Hubble (c/H0) en Mpc
    
    mu_model = []
    
    for z in z_array:
        # Integrar 1/E(x) dx desde 0 hasta z para obtener la distancia comóvil sin dimensiones
        integral_value = quad(lambda x: 1.0 / E_TD(x, w_sigma, OM_M, OM_L), 0, z)[0]
        
        # Distancia de Luminosidad (DL en Mpc)
        DL_Mpc = c_H0 * (1 + z) * integral_value
        
        # Módulo de Distancia (mu)
        mu = 5.0 * np.log10(DL_Mpc) + 25.0
        mu_model.append(mu)
        
    return np.array(mu_model)


# --- 3. FUNCIÓN DE AJUSTE (CHI-CUADRADO) ---

def chi_squared(params, z_obs, mu_obs, inv_cov_matrix):
    """
    Calcula el Chi-Cuadrado (chi^2) utilizando la matriz de covarianza inversa.
    """
    w_sigma = params[0]
    
    # Genera la predicción del modelo
    mu_model = modulo_distancia(z_obs, w_sigma, OM_M, OM_L, H0_VAL)
    
    # Vector de residuos: (Modelo - Observado)
    Delta_mu = mu_model - mu_obs
    
    # Cálculo del Chi-Cuadrado: chi^2 = Delta_mu^T * C_inv * Delta_mu
    chi2 = np.dot(Delta_mu.T, np.dot(inv_cov_matrix, Delta_mu))
    
    return chi2

# --- 4. EJECUCIÓN DEL PROGRAMA PRINCIPAL ---

if __name__ == "__main__":
    
    # VERIFICACIÓN DE ARCHIVOS
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

        # B. VERIFICACIÓN DE CARGA EXITOSA (Manejo del error 'NoneType')
        if z_datos is None:
            print("\n🚨 Deteniendo la ejecución debido a errores en load_pantheon_data.")
        else:
            # C. DEFINICIÓN Y EJECUCIÓN DE LA MINIMIZACIÓN
            print("\nEjecutando la minimización para encontrar el w_sigma óptimo...")

            # Inicial y límites del parámetro de energía oscura w_sigma
            w_inicial = np.array([-0.9])
            bounds = [(-1.5, -0.5)] # Rango de búsqueda razonable para w
            
            # Realizar la minimización (ajuste de curvas)
            resultado = minimize(
                chi_squared, 
                w_inicial, 
                args=(z_datos, mu_datos, C_inv), 
                method='L-BFGS-B', 
                bounds=bounds
            )

            # D. EXTRACCIÓN Y COMPARACIÓN DE RESULTADOS
            
            # 1. Resultado del modelo TD (tu hipótesis dinámica)
            w_best_fit = resultado.x[0]
            chi2_min = resultado.fun

            # 2. Resultado del modelo RG estándar (Lambda-CDM, w = -1.0)
            chi2_RG_std = chi_squared(np.array([-1.0]), z_datos, mu_datos, C_inv)

            print("\n--- Resultados de la Verificación (Tensión Dinámica vs. RG) ---")
            print(f"Chi-Cuadrado de la RG estándar (w = -1.0):       {chi2_RG_std:.4f}")
            print(f"Mejor valor de Tensión (w_sigma) encontrado:    {w_best_fit:.4f}")
            print(f"Chi-Cuadrado mínimo para la TD (w = {w_best_fit:.4f}): {chi2_min:.4f}")
            
            # E. CONCLUSIÓN CIENTÍFICA
            # d.o.f = N_datos - N_parametros (1701 - 1 = 1700)
            dof = len(z_datos) - 1 
            print(f"Chi^2/d.o.f para TD: {chi2_min/dof:.4f}")

            if chi2_min < chi2_RG_std:
                print(f"\n✅ CONCLUSIÓN: El modelo de Tensión Dinámica (TD) se ajusta MEJOR a los datos de Pantheon+.")
                print("Si el valor de w_sigma óptimo es significativamente diferente de -1.0,")
                print("esto podría apoyar un modelo de energía oscura dinámico.")
            else:
                print("\n❌ CONCLUSIÓN: La Relatividad General estándar (w=-1.0) se ajusta mejor o igual a los datos.")
                print("Tu modelo es una reformulación teórica, pero sin evidencia de una Tensión Dinámica.")