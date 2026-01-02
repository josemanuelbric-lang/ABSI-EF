import numpy as np

# --- Constantes del Modelo de Tensión Dimensional ---
# Constante de ajuste para el Potencial de Tensión (C_AJUSTE_POTENCIAL en el código original)
# Analogía a 2*G/c^2 en el límite newtoniano, pero aquí es un factor de ajuste (alfa).
ALPHA = 0.005 

# --- Definición de Cuerpos (Solo para tener los parámetros sigma y posición) ---
class CuerpoDimensional:
    def __init__(self, nombre, x, y, tension_sigma):
        self.nombre = nombre
        self.pos = np.array([x, y], dtype=float)
        self.sigma = tension_sigma 

# --- Configuración del Sistema (Valores Iniciales) ---
sol = CuerpoDimensional("Sol", 0, 0, 50.0)
planeta = CuerpoDimensional("Planeta", 5, 0, 0.5)

# --- Fórmulas Analíticas (Soluciones Matemáticas) ---

def calcular_distancia(pos1, pos2):
    """Calcula la distancia r entre dos cuerpos."""
    return np.linalg.norm(pos1 - pos2)

# =======================================================
# 1A. La Dinámica (Ecuación de Movimiento: Aceleración)
# =======================================================

def aceleracion_tension(cuerpo_movil, cuerpo_fuente):
    """
    Calcula la aceleración del cuerpo_movil debido a la Tensión del cuerpo_fuente.
    a = (sigma_fuente / r^2) * r_unitario.
    (El Principio de Equivalencia está implícito, a no depende de sigma_movil)
    """
    r_vec = cuerpo_fuente.pos - cuerpo_movil.pos
    r = calcular_distancia(cuerpo_movil.pos, cuerpo_fuente.pos)
    
    # Manejo del límite cercano r -> 0 (usamos el mismo límite que en el código: r = max(r, 0.5))
    r = max(r, 0.5)
    
    direccion_unit = r_vec / r
    
    # Magnitud de la aceleración: |a| = sigma_fuente / r^2
    aceleracion_mag = cuerpo_fuente.sigma / (r**2)
    
    return direccion_unit * aceleracion_mag

# =======================================================
# 1B. El Tiempo (Dilatación Temporal: Tasa de Tiempo Local)
# =======================================================

def potencial_tension(cuerpo_movil, cuerpo_fuente):
    """
    Calcula el Potencial de Tensión U ~ -sigma_fuente / r.
    (Análogo al potencial gravitatorio Phi = -G*M/r)
    """
    r = calcular_distancia(cuerpo_movil.pos, cuerpo_fuente.pos)
    r = max(r, 0.5) # Manejo del límite cercano
    return -cuerpo_fuente.sigma / r

def tasa_tiempo_local(cuerpo_analizado, cuerpos_fuente):
    """
    Calcula la Tasa de Tiempo Local (dtau/dt) basada en el Potencial Total.
    Tasa = sqrt(1 + ALPHA * Potencial_Total).
    (Análogo a la componente de la métrica g_00)
    """
    potencial_total = 0.0
    for fuente in cuerpos_fuente:
        if fuente != cuerpo_analizado: # Solo fuentes externas
            potencial_total += potencial_tension(cuerpo_analizado, fuente)
            
    # El modelo usa el valor absoluto del potencial: |U| = -U
    potencial_normalizado = -potencial_total * ALPHA
    
    # Condición de límite: si la energía potencial es demasiado grande, el tiempo se detiene (tasa = 0)
    if potencial_normalizado >= 1.0:
        return 0.0
    
    # La solución analítica para la tasa:
    tasa = np.sqrt(1.0 - potencial_normalizado)
    return tasa

# --- Ejemplos de uso de las fórmulas (Solo demostrativo) ---

# Aceleración del planeta debida al Sol (1A)
aceleracion_p_s = aceleracion_tension(planeta, sol)
print(f"1A. Aceleración del Planeta (Sol): {aceleracion_p_s}")

# Potencial Total en la posición del planeta (1B)
potencial_en_planeta = potencial_tension(planeta, sol) # Solo el Sol es fuente
print(f"1B. Potencial de Tensión en el Planeta: {potencial_en_planeta:.4f}")

# Tasa de Tiempo Local del planeta (1B)
tasa_dt = tasa_tiempo_local(planeta, [sol])
print(f"1B. Tasa de Tiempo Local (dtau/dt) del Planeta: {tasa_dt:.4f}")