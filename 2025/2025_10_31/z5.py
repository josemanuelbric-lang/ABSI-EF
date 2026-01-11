import numpy as np

# --- Parámetros de la TDH ---
L_MAX = 23.26              # Límite de Complejidad Estructural (TDH)
EPSILON_BASE = 0.03225     # Error Estructural Base (epsilon_0)
FACTOR_ATENUACION = 0.95   # Factor 'r' de reducción en cada ciclo
COSTO_CORRECCION = 10      # Coste de cómputo (pasos) por cada ciclo de corrección
N_INPUT = 5                # Tamaño del input para el problema NP (2^5 = 32 pasos base)

# Pasos base del problema NP (SAT)
PASOS_NP_BASE = 2**N_INPUT

# Umbral: La ganancia marginal debe ser menor a este valor para parar
UMBRAL_GANANCIA = 1e-6

# --- Algoritmo para Encontrar k* ---
epsilon_residual = EPSILON_BASE
P_exito_anterior = (1 - epsilon_residual) ** PASOS_NP_BASE
k = 0

print(f"Búsqueda del Punto de No-Rentabilidad (n={N_INPUT}, Pasos Base={PASOS_NP_BASE}):")
print("-" * 60)

while True:
    # 1. Costo Marginal: Aumenta los pasos por la corrección
    T_total_actual = PASOS_NP_BASE + (k * COSTO_CORRECCION)
    
    # 2. Ganancia Marginal: Reduce el error y recalcula P(exitosa)
    epsilon_actual = EPSILON_BASE * (FACTOR_ATENUACION ** k)
    P_exito_actual = (1 - epsilon_actual) ** T_total_actual
    
    ganancia_marginal = P_exito_actual - P_exito_anterior
    
    # Detener si:
    # A) La complejidad total excede el Límite TDH (L_MAX).
    # B) La ganancia marginal es menor que el umbral (ya no vale la pena).
    if T_total_actual > L_MAX or ganancia_marginal < UMBRAL_GANANCIA:
        break
        
    P_exito_anterior = P_exito_actual
    k += 1

print(f"   Ciclos de Corrección (k): {k-1}")
print(f"   Error Estructural Residual (epsilon): {epsilon_actual:.8f}")
print(f"   Pasos de Cómputo Total (T_Total): {T_total_actual}")
print(f"   Probabilidad de Éxito Final: {P_exito_actual:.8f}")
print(f"   Ganancia Marginal en el último ciclo: {ganancia_marginal:.8e}")

if T_total_actual > L_MAX:
    print(f"\n¡🛑 LÍMITE ALCANZADO! La T_Total ({T_total_actual:.2f}) ha excedido el L_MAX ({L_MAX:.2f}).")
else:
     print(f"\n¡✅ CONVERGENCIA! La ganancia marginal ({UMBRAL_GANANCIA}) es demasiado baja para continuar.")