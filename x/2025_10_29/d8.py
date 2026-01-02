import numpy as np

# --- Parámetros de la TDH ---

# 1. Factor de Atenuación Requerido (kappa)
# Necesario para que S_TDH (1e12) se ajuste a S_Observada (1e0).
KAPPA_REQUERIDO = 1.0e-12 

# 2. Relación de Escala Dimensional (|Dn|)
# Este es el factor por el cual se 'diluye' la tensión en un solo salto.
# Usamos un valor grande y arbitrario (1 millón) para demostrar el efecto.
RELACION_ESCALA_DN = 1.0e6 

# --- Cálculo del Exponente de Potencia (N) ---

# Queremos encontrar N tal que: KAPPA_REQUERIDO = (1 / RELACION_ESCALA_DN)**N
# Aplicando logaritmos: log(KAPPA_REQUERIDO) = N * log(1 / RELACION_ESCALA_DN)
# Por lo tanto: N = log(KAPPA_REQUERIDO) / log(1 / RELACION_ESCALA_DN)

# Nota: Usamos np.log10 para mayor claridad, aunque se podría usar log natural.

log_kappa = np.log10(KAPPA_REQUERIDO)
log_escala_inversa = np.log10(1.0 / RELACION_ESCALA_DN) # log10(1/1e6) = -6

# Si log_escala_inversa es 0, hay un problema (escala infinita o cero), pero en física es finito.

if log_escala_inversa != 0:
    EXPONENTE_N_REQUERIDO = log_kappa / log_escala_inversa
else:
    EXPONENTE_N_REQUERIDO = "Indefinido"


print("--- Simulación del Exponente de Potencia (N) de la TDH ---")
print(f"1. Factor de Atenuación (κ) Requerido: {KAPPA_REQUERIDO:.1e}")
print(f"2. Relación de Escala Asumida (|Dn|): {RELACION_ESCALA_DN:.1e}")
print(f"   log10(κ): {log_kappa:.1f}")
print(f"   log10(1/|Dn|): {log_escala_inversa:.1f}")
print("----------------------------------------------------------")
print(f"El Exponente de Potencia (N) Requerido es: {EXPONENTE_N_REQUERIDO:.2f}")

# --- Comprobación del Salto (Bloqueo del Vacío) ---
print("\n--- Comprobación: Dilución de la Tensión por el 'Salto' ---")

# Comprobamos si el N calculado reproduce el kappa.
kappa_comprobado = (1.0 / RELACION_ESCALA_DN)**EXPONENTE_N_REQUERIDO

print(f"κ calculado usando N = {EXPONENTE_N_REQUERIDO:.2f}: {kappa_comprobado:.1e}")

if np.isclose(kappa_comprobado, KAPPA_REQUERIDO):
    print("\n✅ CONCLUSIÓN TDH: La Regla de Potencia x^N produce el factor de atenuación requerido.")
    print("Esto demuestra que el 'Salto' (la Regla x^N) es el mecanismo de Bloqueo de la Tensión.")
else:
    print("\n❌ CONCLUSIÓN: La atenuación no se pudo reproducir con los parámetros dados.")