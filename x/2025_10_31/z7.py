import numpy as np

# Parámetros TDH
D = 4.0
N_OBSERVABLE = 3.8710
EPSILON = (D - N_OBSERVABLE) / D  # 0.03225

# Cálculo de L_MAX
L_MAX_CALCULADO = -1 / np.log(1 - EPSILON)

print(f"Error Estructural (epsilon): {EPSILON:.5f}")
print(f"Límite de Complejidad Estructural (L_MAX): {L_MAX_CALCULADO:.4f}")
# Prueba con el n crítico
N_CRITICO = 5
PASOS_CRITICOS = 2**N_CRITICO  # 32

print("\n--- Comprobación de la Inviabilidad Estructural (n=5) ---")
print(f"Límite (L_MAX): {L_MAX_CALCULADO:.4f}")
print(f"Pasos Requeridos (2^5): {PASOS_CRITICOS}")

# Probabilidad de Éxito para el n crítico
P_exito_critico = (1 - EPSILON) ** PASOS_CRITICOS

print(f"Probabilidad de Éxito de SAT (n=5): {P_exito_critico:.8f}")

if PASOS_CRITICOS > L_MAX_CALCULADO:
    print(f"\n¡🛑 INVIABILIDAD COMPROBADA! Los pasos (32) exceden L_MAX (30.56).")
else:
    print(f"\n¡ERROR! El n crítico no debería exceder L_MAX.")