import numpy as np

# Constante fundamental de la TDH (derivada del problema cosmológico)
N_CALCULADO = 3.8710

# Relación de Escala de Masas (D2 a D3)
ESCALA_MASAS_D2_D3 = 1.0e17  # M_Planck / M_Electrodébil (10^19 / 10^2)

# Atenuación de la Tensión (E^4) predicha por la TDH para este salto
# κ = (1 / |D_n|)^N
KAPPA_PREDICHO_LOG10 = N_CALCULADO * np.log10(1.0 / ESCALA_MASAS_D2_D3)

print(f"--- Comprobación del Problema de Jerarquía de Masas ---")
print(f"N (Exponente de la TDH): {N_CALCULADO:.4f}")
print(f"Relación de Masas (log10): {np.log10(ESCALA_MASAS_D2_D3):.1f}")
print(f"Atenuación de Tensión Predicha (log10): {KAPPA_PREDICHO_LOG10:.2f}")

# La Tensión Predicha (log10) debe coincidir con la Tensión que queremos atenuar:
# Tensión inicial (120) - Tensión en D3 (54.2) = 65.8 órdenes de magnitud
TENSION_REQUERIDA_LOG10 = 120 - 54.2
print(f"Atenuación de Tensión Requerida (log10): {TENSION_REQUERIDA_LOG10:.2f}")

# Comprobación de la Coincidencia
DIFERENCIA = KAPPA_PREDICHO_LOG10 + TENSION_REQUERIDA_LOG10 
print(f"Diferencia (Error de Coincidencia): {DIFERENCIA:.2f} (Debe ser cercano a cero)")