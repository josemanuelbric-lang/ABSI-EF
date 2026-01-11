import numpy as np
import os
from scipy.integrate import quad
from scipy.optimize import minimize
from pathlib import Path

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Ajusta esta ruta a tu directorio
BASE_DIR = Path(r"c:\Users\bric\Documents\DataRelease")
DATA_FOLDER = BASE_DIR / "Pantheon+_Data" / "4_DISTANCES_AND_COVAR"

DATA_FILE_NAME = "Pantheon+SH0ES.dat"
COV_FILE_NAME = "Pantheon+SH0ES_STAT+SYS.cov"
DATA_PATH = DATA_FOLDER / DATA_FILE_NAME
COV_PATH = DATA_FOLDER / COV_FILE_NAME

# --- 2. CARGA DE DATOS ---

def load_pantheon_data(data_path, cov_path):
    """
    Carga los datos de Pantheon+ (z, mu) y la matriz de covarianza inversa.
    """
    print("Cargando datos de módulo de distancia (mu)...")
    try:
        # Columna 1: z_CMB (Redshift en el marco del CMB)
        # Columna 3: MU_SH0ES (Módulo de distancia calibrado)
        data = np.loadtxt(data_path, usecols=(1, 3), skiprows=1)
    except Exception as e:
        print(f"❌ ERROR: Fallo al cargar datos de {data_path}. Error: {e}")
        return None, None, None

    z_obs = data[:, 0]
    mu_obs = data[:, 1] # Estos son los m_B - M (datos)
    N_datos = len(z_obs)
    print(f"Cargando matriz de covarianza (N={N_datos})...")

    try:
        # La primera línea del .cov es el número de puntos (N)
        with open(cov_path, 'r') as f:
            N_check = int(f.readline().strip())
        
        if N_check != N_datos:
            print(f"❌ ERROR: Inconsistencia de datos. {data_path} tiene {N_datos} puntos, pero {cov_path} dice tener {N_check}.")
            return None, None, None

        # Cargar el resto (el vector 1D de la matriz)
        cov_vector = np.loadtxt(cov_path, skiprows=1)
        cov_matrix = cov_vector.reshape((N_datos, N_datos))
        
    except Exception as e:
        print(f"❌ ERROR: Fallo al cargar matriz de covarianza {cov_path}. Error: {e}")
        return None, None, None

    print(f"Matriz reconstruida ({cov_matrix.shape}). Calculando inversa (C^-1)...")
    
    try:
        inv_cov_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        print("❌ ERROR: La matriz de covarianza es singular (no invertible).")
        return None, None, None
    
    print(f"Datos cargados exitosamente: {N_datos} supernovas.")
    return z_obs, mu_obs, inv_cov_matrix

# --- 3. MODELO COSOMOLÓGICO ---

def E_z(z, w_sigma, OM_M):
    """
    Función E(z) = H(z)/H0 para un universo plano (wCDM).
    """
    OM_L = 1.0 - OM_M  # Asumimos universo plano
    exponent_DE = 3 * (1 + w_sigma) # Exponente para la Energía Oscura (DE)
    
    term_materia = OM_M * (1 + z)**3
    term_energia_oscura = OM_L * (1 + z)**exponent_DE
    
    return np.sqrt(term_materia + term_energia_oscura)

def hubble_free_distance_modulus(z_array, w_sigma, OM_M):
    """
    Calcula el módulo de distancia teórico *independiente* de H0.
    El modelo que calculamos es: 
    
    mu_teorico = 5 * log10( D_L_sin_H0 )
    
    donde D_L_sin_H0 = (1+z) * integral(dz' / E(z'))
    
    El parámetro H0 (y el +25, y M_abs) será absorbido por
    el parámetro de calibración 'M_hat' durante el ajuste.
    """
    mu_model = []
    
    for z in z_array:
        # 1. Calcular la integral de comovilidad (con c=1)
        integral_comovil, _ = quad(lambda z_prime: 1.0 / E_z(z_prime, w_sigma, OM_M), 0, z)
        
        # 2. Calcular la Distancia de Luminosidad (libre de H0)
        DL_hubble_free = (1 + z) * integral_comovil
        
        # 3. Calcular el módulo de distancia (libre de H0 y +25)
        if DL_hubble_free <= 0:
            mu = -np.inf # Evita error de logaritmo
        else:
            mu = 5.0 * np.log10(DL_hubble_free)
            
        mu_model.append(mu)
        
    return np.array(mu_model)

# --- 4. FUNCIÓN DE AJUSTE (CHI-CUADRADO) ---

def chi_squared_marginalized(params, z_obs, mu_obs, inv_cov_matrix, fixed_w=None, return_M=False):
    """
    Calcula el Chi-cuadrado marginalizado sobre el parámetro de calibración M.
    
    Si 'fixed_w' se provee, 'params' es solo [OM_M].
    Si 'fixed_w' es None, 'params' es [w_sigma, OM_M].
    """
    
    # 1. Asignar parámetros
    try:
        if fixed_w is not None:
            w_sigma = fixed_w
            OM_M = params[0]
        else:
            w_sigma = params[0]
            OM_M = params[1]
    except IndexError:
        print(f"Error de parámetros: {params}")
        return np.inf

    # 2. Calcular el modelo teórico (libre de H0)
    mu_model = hubble_free_distance_modulus(z_obs, w_sigma, OM_M)
    
    # 3. Calcular el vector de residuos (Datos - Modelo)
    #    Delta_mu = mu_obs - (mu_model + M_hat)
    #    Aquí definimos Delta_mu = mu_obs - mu_model
    Delta_mu = mu_obs - mu_model
    
    # 4. Calcular los componentes del Chi^2 marginalizado
    # (Usamos '@' para producto de matrices/vectores)
    E = np.ones_like(Delta_mu)
    
    D_T_Cinv_D = Delta_mu @ inv_cov_matrix @ Delta_mu
    D_T_Cinv_E = Delta_mu @ inv_cov_matrix @ E
    E_T_Cinv_E = E @ inv_cov_matrix @ E
    
    # 5. Chi^2 final (marginalizado sobre M_hat)
    chi2_marg = D_T_Cinv_D - (D_T_Cinv_E**2) / E_T_Cinv_E
    
    if return_M:
        # 6. Calcular el M_hat óptimo
        # Este M_hat = M_abs + 25 + 5*log10(c/H0)
        M_hat = D_T_Cinv_E / E_T_Cinv_E
        return chi2_marg, M_hat
    else:
        return chi2_marg

# --- 5. EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    
    # A. Cargar datos
    if not DATA_PATH.exists() or not COV_PATH.exists():
        print(f"❌ ERROR: No se encontraron los archivos en {DATA_FOLDER}")
        print("Asegúrate de que la variable BASE_DIR esté configurada correctamente.")
    else:
        z_datos, mu_datos, C_inv = load_pantheon_data(DATA_PATH, COV_PATH)
        
        if z_datos is not None:
            N_datos = len(z_datos)
            
            # --- B. AJUSTE 1: Modelo Lambda-CDM (w=-1.0, OM_M libre) ---
            print("\nEjecutando minimización para Lambda-CDM (w=-1, fit OM_M)...")
            
            params_inicial_lcdm = [0.3]  # Valor inicial solo para OM_M
            bounds_lcdm = [(0.1, 0.6)]   # Rango físico para OM_M
            
            resultado_lcdm = minimize(
                chi_squared_marginalized, 
                params_inicial_lcdm,
                args=(z_datos, mu_datos, C_inv, -1.0), # fixed_w = -1.0
                method='L-BFGS-B',
                bounds=bounds_lcdm
            )
            
            # Recalcular para obtener M_hat
            OM_M_lcdm = resultado_lcdm.x[0]
            chi2_lcdm, M_hat_lcdm = chi_squared_marginalized(
                [OM_M_lcdm], z_datos, mu_datos, C_inv, fixed_w=-1.0, return_M=True
            )

            # --- C. AJUSTE 2: Modelo TD (w libre, OM_M libre) ---
            print("Ejecutando minimización para Tensión Dinámica (fit w, fit OM_M)...")
            
            params_inicial_td = [-0.9, 0.3] # Valor inicial para [w, OM_M]
            # Ampliamos los límites para w, ya que antes se "pegaba" al borde
            bounds_td = [(-2.0, 0.0), (0.1, 0.6)] 
            
            resultado_td = minimize(
                chi_squared_marginalized,
                params_inicial_td,
                args=(z_datos, mu_datos, C_inv, None), # fixed_w = None
                method='L-BFGS-B',
                bounds=bounds_td
            )
            
            # Recalcular para obtener M_hat
            w_td, OM_M_td = resultado_td.x
            chi2_td, M_hat_td = chi_squared_marginalized(
                [w_td, OM_M_td], z_datos, mu_datos, C_inv, fixed_w=None, return_M=True
            )

            # --- D. REPORTE DE RESULTADOS ---
            # Grados de libertad (d.o.f.)
            dof_lcdm = N_datos - 2 # (Ajustamos OM_M y M_hat)
            dof_td = N_datos - 3   # (Ajustamos w, OM_M y M_hat)

            print("\n" + "---" * 15)
            print("--- Resultados Finales del Ajuste Cosmológico ---")
            print(f"Número de Supernovas (N): {N_datos}")
            print("---" * 15)
            
            print("\n🔵 Modelo de Referencia (Lambda-CDM)")
            print(f"Grados de Libertad (d.o.f.): {dof_lcdm}")
            print(f"Parámetro (w) Fijo: -1.0000")
            print(f"Parámetro óptimo (OM_M): {OM_M_lcdm:.4f}")
            print(f"Calibración Óptima (M_hat): {M_hat_lcdm:.4f}")
            print(f"Chi-Cuadrado (chi^2): {chi2_lcdm:.4f}")
            print(f"Calidad del Ajuste (chi^2/d.o.f.): {chi2_lcdm / dof_lcdm:.4f}  <-- (Debe ser cercano a 1.0)")

            print("\n🔴 Modelo Tensión Dinámica (TD / wCDM)")
            print(f"Grados de Libertad (d.o.f.): {dof_td}")
            print(f"Parámetro óptimo (w_sigma): {w_td:.4f}")
            print(f"Parámetro óptimo (OM_M): {OM_M_td:.4f}")
            print(f"Calibración Óptima (M_hat): {M_hat_td:.4f}")
            print(f"Chi-Cuadrado mínimo (chi^2_min): {chi2_td:.4f}")
            print(f"Calidad del Ajuste (chi^2/d.o.f.): {chi2_td / dof_td:.4f}  <-- (Debe ser cercano a 1.0)")
            print("---" * 15)

            # --- E. CONCLUSIÓN ---
            Delta_chi2 = chi2_lcdm - chi2_td
            
            if (chi2_lcdm / dof_lcdm) > 1.5 or (chi2_lcdm / dof_lcdm) < 0.5:
                 print("\nADVERTENCIA: El valor de chi^2/d.o.f. está lejos de 1.0.")
                 print("Esto sugiere que aún puede haber un problema en la carga de datos o la covarianza.")
            
            if Delta_chi2 > 0:
                print(f"\n✅ CONCLUSIÓN: El modelo TD (w={w_td:.4f}) presenta un MEJOR ajuste (Delta_chi^2 = {Delta_chi2:.2f})")
                print("   que el modelo Lambda-CDM estándar.")
            else:
                print(f"\n❌ CONCLUSIÓN: El modelo Lambda-CDM estándar se ajusta mejor (o igual) a los datos")
                print(f"   (Delta_chi^2 = {Delta_chi2:.2f}).")