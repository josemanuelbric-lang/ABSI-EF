import numpy as np
import emcee
from scipy.integrate import quad
from scipy.interpolate import interp1d

# =========================================================
# 1. Definición del Modelo de Tensión Dinámica (TD)
# =========================================================

# NOTA: EL PARÁMETRO Om_L NO ESTABA DEFINIDO, LO CALCULAMOS ASUMIENDO FLAT (Om_k = 0)
# EN ESTE ESQUEMA SIMPLIFICADO.

# Función de la Ecuación de Estado de la Energía Oscura w(z)
def w_TD(z, w0, wa):
    """Evolución del parámetro w de la EO según el modelo CPL."""
    return w0 + wa * (z / (1.0 + z))

# Función de Expansión de Hubble H(z) para tu modelo TD
def H_TD(z, H0, Om_M, w0, wa):
    """Tasa de expansión de Hubble para el modelo TD."""
    
    # Suponemos un universo plano para simplificar: Om_k = 0.0
    Om_k = 0.0 
    Om_L = 1.0 - Om_M - Om_k # Densidad de Energía Oscura (EO) hoy
    
    if Om_L <= 0.0: # Evitar la raíz cuadrada de un número negativo
        return 1e10 * H0

    # Integral del término de la Energía Oscura (EO). Se usa una lambda function
    try:
        integral_EO, _ = quad(lambda z_prime: (1.0 + z_prime)**(3 * (1.0 + w_TD(z_prime, w0, wa))), 0, z)
    except Exception:
        # En caso de error de integración, devuelve un valor grande
        return 1e10 * H0
        
    # Ecuación de Friedman con EO Dinámica
    E_z_squared = (Om_M * (1.0 + z)**3) + \
                  (Om_k * (1.0 + z)**2) + \
                  (Om_L * np.exp(integral_EO)) 
                  
    if E_z_squared <= 0.0: # Evitar la raíz cuadrada de un número negativo
        return 1e10 * H0
        
    return H0 * np.sqrt(E_z_squared)

# Tasa de Crecimiento de Estructuras f*sigma8(z)
def f_sigma8_TD(z, H0, Om_M, w0, wa, gamma, sigma8_fid):
    """Predice f*sigma8(z) para el modelo TD."""
    
    # Para manejar múltiples valores de z (un array), necesitamos iterar o usar np.vectorize
    # Usaremos una aproximación simple. La verdadera f(z) requiere resolver ODEs.
    E_z = H_TD(z, H0, Om_M, w0, wa) / H0
    Om_M_z = Om_M * (1.0 + z)**3 / (E_z**2)
    
    # 2. Calcular la tasa de crecimiento f(z) ~ Omega_M(z)^gamma
    # Usamos una máscara para prevenir 0**gamma
    Om_M_z_safe = np.where(Om_M_z > 0, Om_M_z, 1e-10) 
    f_z = Om_M_z_safe**gamma
    
    # Simplificación: f*sigma8(z) es proporcional a f(z) * sigma8(z).
    # Aquí aproximamos sigma8(z) = sigma8_fiducial * D(z)/D(0)
    # y la función D(z) es compleja. Usaremos la aproximación más sencilla por ahora:
    
    # Nota: El término (1+z) fue eliminado de la simplificación anterior, era incorrecto.
    # Necesitas un factor de crecimiento D(z), que es un cálculo complejo.
    # Por ahora, solo usamos f(z) * sigma8_fiducial
    
    return f_z * sigma8_fid 

# =========================================================
# 2. Datos Observacionales (EJEMPLO SIMPLIFICADO)
# =========================================================

# Columnas: [Corrimiento_al_rojo (z), f*sigma8 (Valor Medido), Error (sigma)]
DATA_FSIGMA8 = np.array([
    [0.32, 0.430, 0.080],  # 6dFGS
    [0.60, 0.470, 0.045],  # BOSS
    [0.86, 0.400, 0.040],  # WiggleZ
    [1.52, 0.380, 0.120]   # eBOSS
])

# =========================================================
# 3. MCMC y Log-Verosimilitud
# =========================================================

# ... (log_likelihood, log_prior, log_probability sin cambios) ...

def log_likelihood(theta, data):
    z_data, fs8_data, fs8_err = data[:, 0], data[:, 1], data[:, 2]
    H0, Om_M, w0, wa, gamma, sigma8_fid = theta
    
    # Validación de parámetros antes de la predicción
    if not np.isfinite(H0) or not np.isfinite(Om_M) or Om_M <= 0 or Om_M >= 1:
        return -np.inf

    fs8_pred = np.array([f_sigma8_TD(z, H0, Om_M, w0, wa, gamma, sigma8_fid) for z in z_data])
    
    # Verificar valores infinitos/NaN en la predicción
    if not np.all(np.isfinite(fs8_pred)):
        return -np.inf
    
    chi2 = np.sum(((fs8_pred - fs8_data) / fs8_err)**2)
    return -0.5 * chi2

def log_prior(theta):
    H0, Om_M, w0, wa, gamma, sigma8_fid = theta
    if (60 < H0 < 80) and \
       (0.1 < Om_M < 0.5) and \
       (-2.0 < w0 < 0.0) and \
       (-2.0 < wa < 2.0) and \
       (0.3 < gamma < 1.0) and \
       (0.6 < sigma8_fid < 1.0):
        return 0.0
    return -np.inf

def log_probability(theta, data):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, data)

# =========================================================
# 4. EJECUCIÓN Y RESULTADOS
# =========================================================
print("--- Iniciando MCMC para Modelo de Tensión Dinámica (TD) ---")

# Configuración MCMC
nwalkers = 32
ndim = 6 # [H0, Om_M, w0, wa, gamma, sigma8_fid]
nsteps = 5000 # Un número alto para asegurar convergencia

# Estado inicial (semilla aleatoria cerca de valores de consenso)
initial_state = np.array([70.0, 0.3, -1.0, 0.0, 0.55, 0.8]) 
pos = initial_state + 1e-4 * np.random.randn(nwalkers, ndim)

# Inicializar y ejecutar el Sampler
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, args=[DATA_FSIGMA8])
sampler.run_mcmc(pos, nsteps, progress=True)

# -----------------------------------------------
# PROCESAMIENTO DE RESULTADOS
# -----------------------------------------------

# Descartar los primeros pasos (burn-in) y aplanar la cadena
burn_in = 1000
flat_samples = sampler.get_chain(discard=burn_in, flat=True)

# Nombres de los parámetros para la impresión
labels = ["H0", "Omega_M", "w0", "wa", "gamma", "sigma8_fid"]

print("\n--- Resultados Finales del Ajuste (Media y Desviación Estándar) ---")

# Imprimir los resultados
for i in range(ndim):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    q = np.diff(mcmc)
    txt = "{0} = {1:.4f} +{2:.4f} / -{3:.4f}"
    print(txt.format(labels[i], mcmc[1], q[1], q[0]))

print("\n--- Ejecución Finalizada ---")