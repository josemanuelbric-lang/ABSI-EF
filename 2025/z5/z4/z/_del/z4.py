# Símbolos para las densidades y presiones
rho_M, p_M = symbols('rho_M p_M') # Materia (Bariónica y Oscura)
rho_DE, p_DE = symbols('rho_DE p_DE') # Energía Oscura (TD Exceso)

# Supuesto 1: La materia es polvo (p_M = 0)
p_M_val = 0

# Supuesto 2: La Energía Oscura (Exceso de Tensión) tiene una ecuación de estado w_sigma
w_sigma = symbols('w_sigma')
p_DE_val = w_sigma * rho_DE

# 1. Componente de DÉFICIT de Tensión (S < 0) - Materia
# La Materia causa ATRACCIÓN (T>0), por lo tanto, es el Déficit.
# T_munu_Materia (diagonal) ~ [rho_M, p_M, p_M, p_M]
# El tensor de Tensión S- debe estar relacionado con esto, pero con el signo de tensión contrario.
S_neg_tension = -rho_M # Usamos solo el componente de densidad para simplificar la comparación

# 2. Componente de EXCESO de Tensión (S > 0) - Energía Oscura
# La Energía Oscura causa REPULSIÓN (T<0), por lo tanto, es el Exceso.
# T_munu_EO ~ [rho_DE, p_DE, p_DE, p_DE]
S_pos_tension = rho_DE # Usamos el componente de densidad de EO

# 3. Tensión Total (S_Total)
S_total_rho = S_neg_tension + S_pos_tension

print("\n--- Definición Simbólica de las Tensiones ---")
print(f"Tensión S- (Déficit/Materia): {-S_neg_tension}") # Imprimimos la densidad de la fuente
print(f"Tensión S+ (Exceso/EO): {S_pos_tension}")

# 4. Cálculo de la Densidad de Energía Efectiva de la TD
# Si G_munu ~ S_munu, entonces la densidad efectiva rho_TD debe ser proporcional a S_total_rho
rho_TD_efectiva = S_total_rho * G / (c**4) # Se re-escala por las constantes de acoplamiento

print(f"\nDensidad Efectiva Total TD (rho_M + rho_DE): {rho_TD_efectiva}")