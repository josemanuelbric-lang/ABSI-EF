import numpy as np

# --- Parámetros Fundamentales de la TDH ---
# Escala de Planck (M_p) simplificada
LAMBDA_PLANK = 1e3 
# Número de Atomodimensionales en la Dimensión D_1 (finito y contable)
# ESTE ES EL POSTULADO CLAVE DE FINITUD
NUMERO_A1 = 500

# El volumen cuantificado de cada Atomodimensional V_A1
# En Gravedad Cuántica, V_A1 es del orden de la longitud de Planck al cubo (l_p^3)
# Aquí, lo definimos inversamente proporcional al número de A1 para simplificar la normalización
VOLUMEN_A1 = 1.0 / NUMERO_A1

# Tensión/Energía del Vacío por A1 (Analogía al término Lambda en el Modelo Estándar)
# En la TQC, este valor por unidad es enorme, del orden de M_p^4.
# Usaremos M_p^4 aquí, lo que haría explotar la integral si fuera continua.
TENSION_POR_A1_TEORICA = LAMBDA_PLANK**4 


# --- Escenario A: Acción TQC (Divergente) ---
# La TQC asume un espacio-tiempo continuo y suma la energía del vacío (E_vacío) hasta el límite infinito.

def calcular_accion_tqc_divergente():
    """Simula la acción si la TQC fuera una suma infinita."""
    # En la TQC, la E_vacío predicha es E_vacío = TENSION_POR_A1_TEORICA * Volumen Total
    # Si el volumen fuera infinito (V_Total -> inf), S_TQC -> inf.
    # Aquí simulamos un volumen total muy grande (un factor 1e20 veces mayor al volumen cuantificado)
    VOLUMEN_TOTAL_TQC_IMAGINARIO = 1e20
    accion_tqc = TENSION_POR_A1_TEORICA * VOLUMEN_TOTAL_TQC_IMAGINARIO 
    return accion_tqc

S_TQC = calcular_accion_tqc_divergente()
print(f"--- 1. Acción TQC Estándar (Divergente) ---")
print(f"S_TQC (Energía del Vacío sin cuantificar): {S_TQC:.2e} unidades de Acción (Tendencia al infinito)")

# --- Escenario B: Acción TDH (Cuantificada y Convergente) ---
# La TDH impone la restricción de que S debe ser una suma finita sobre A_n.

def calcular_accion_tdh_convergente(num_a1, tension_por_a1, vol_a1):
    """
    Calcula la Acción TDH como la suma finita sobre los Atomodimensionales.
    S_TDH = SUM[Tensión_A1 * Volumen_A1]
    """
    # La Tensión total (E_vacío TDH) es el producto de la Tensión individual por el número de A1.
    energia_vacio_tdh = tension_por_a1 * num_a1 * vol_a1 
    
    # En la TDH, esta energía es el término de Tensión en la Acción.
    # La acción S_TDH converge a este valor finito.
    return energia_vacio_tdh

S_TDH = calcular_accion_tdh_convergente(NUMERO_A1, TENSION_POR_A1_TEORICA, VOLUMEN_A1)

print("\n" + "="*50 + "\n")
print(f"--- 2. Acción TDH (Solución Cuantificada) ---")
print(f"Número de A1 (Límite Físico |D1|): {NUMERO_A1:,}")
print(f"S_TDH (Valor Finito y Convergente): {S_TDH:.2e} unidades de Acción")

# --- 3. Comprobación Científica (Conexión con la Realidad) ---

# Problema Científico: La TQC predice S_TQC >> S_OBSERVADA.
# S_OBSERVADA debe estar cerca del valor muy pequeño de la Energía Oscura real.

# En esta simulación, S_TDH se cancela por construcción: S_TDH = M_p^4 * N_A1 * (1/N_A1) = M_p^4
# Aunque el valor de 1e12 es muy grande, es M_p^4, que es FINITO.

# Para que sea científico, el valor final de S_TDH DEBE AJUSTARSE al valor observado.
S_OBSERVADA = 1.0 # (Simulando un valor muy pequeño y medido)

# La tarea científica es encontrar un factor de acoplamiento F (la tensión κ) 
# que reduzca S_TDH a S_OBSERVADA.

FACTOR_DE_AJUSTE_TDH = S_OBSERVADA / S_TDH

print("\n--- 3. Comprobación Científica (Ajuste Fino Necesario) ---")
print(f"Valor Observado (Simulado): {S_OBSERVADA:.2e}")
print(f"El Factor de Acoplamiento TDH (κ) debe ser de orden: {FACTOR_DE_AJUSTE_TDH:.2e}")