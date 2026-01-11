# Variables del entorno (TDH)
L_MAX = 23.26
EPSILON_BASE = 0.03225
FACTOR_ATENUACION = 0.95
COSTO_CORRECCION = 10

# Nuevo input: n=4
N_INPUT = 4
PASOS_NP_BASE = 2**N_INPUT # 16

P_exito_anterior = (1 - EPSILON_BASE) ** PASOS_NP_BASE
k = 0

print(f"Búsqueda con n={N_INPUT} (Pasos Base=16) vs L_MAX={L_MAX}:")
print("-" * 60)

while True:
    T_total_actual = PASOS_NP_BASE + (k * COSTO_CORRECCION)
    
    # 🛑 Criterio de Parada
    if T_total_actual > L_MAX:
        break
        
    epsilon_actual = EPSILON_BASE * (FACTOR_ATENUACION ** k)
    P_exito_actual = (1 - epsilon_actual) ** T_total_actual
    
    ganancia_marginal = P_exito_actual - P_exito_anterior
    
    # 🛑 Criterio de No-Rentabilidad por ganancia marginal baja
    if k > 0 and ganancia_marginal < 1e-6:
        break
        
    P_exito_anterior = P_exito_actual
    k += 1

k -= 1 # Retrocede un paso para mostrar el último ciclo rentable

print(f"   Ciclos de Corrección Rentables (k*): {k}")
print(f"   Error Estructural Residual Mínimo: {EPSILON_BASE * (FACTOR_ATENUACION ** k):.8f}")
print(f"   Pasos de Cómputo Total Final: {PASOS_NP_BASE + (k * COSTO_CORRECCION)}")
print(f"   Probabilidad de Éxito Final (Optimizada): {(1 - EPSILON_BASE * (FACTOR_ATENUACION ** k)) ** (PASOS_NP_BASE + (k * COSTO_CORRECCION)):.8f}")
print(f"   Ganancia en el Último Ciclo: {ganancia_marginal:.8e}")

if k > 0:
    print(f"\n✅ Conclusión: El problema es viable. Es rentable realizar {k} ciclo(s) de corrección.")
else:
    print(f"\n⚠️ Conclusión: No es rentable realizar ni un solo ciclo de corrección (k=0), aunque es viable.")