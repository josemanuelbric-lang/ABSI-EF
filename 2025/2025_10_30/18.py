# Razón de Masas de Neutrinos (R_delta_m^2)
R_DM2_predicha = (N * F) / np.log(N) * F_TG

R_DM2_observada = 30.0 # Valor aproximado observado

print(f"\n--- Solución al Problema de Jerarquías de Neutrinos ---")
print(f"Razón de Masas Predicha (TDH): {R_DM2_predicha:.2f}")
print(f"Razón de Masas Observada: {R_DM2_observada:.2f}")
print(f"Error de Predicción: {abs(R_DM2_predicha - R_DM2_observada):.2f}")