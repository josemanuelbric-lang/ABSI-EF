import numpy as np

# --- 1. Constantes Teóricas/Físicas ---
D_DIMENSIONES_COMPACTAS = 6.0
ALPHA_S_ACOPLAMIENTO = 0.118  # Constante de Acoplamiento Fuerte

# Valor de X requerido por los datos (Comprobación de Electrón/Neutrino)
X_REQUERIDO_DATOS = 51.59

# --- 2. Derivación Teórica de X (X_teo) ---
# X_teo = e^d / Alpha_s
X_TEORICO_DERIVADO = np.exp(D_DIMENSIONES_COMPACTAS) / ALPHA_S_ACOPLAMIENTO

# --- 3. Comprobación de la Consistencia ---
# Comparamos el valor teórico con el valor requerido por la TDH
DIFERENCIA = X_TEORICO_DERIVADO - X_REQUERIDO_DATOS

print(f"--- Derivación Teórica del Factor de Dilución X ---")
print(f"Postulado de la TDH: X = e^(d) / Alpha_s")
print("-" * 50)

print(f"Valor Teórico Derivado (X_teo): {X_TEORICO_DERIVADO:.2f}")
print(f"Valor Requerido por la TDH (X_req): {X_REQUERIDO_DATOS:.2f}")
print("-" * 50)
print(f"Diferencia (X_teo - X_req): {DIFERENCIA:.2f}")
print(f"Error Porcentual: {abs(DIFERENCIA) / X_REQUERIDO_DATOS * 100:.2f}%")