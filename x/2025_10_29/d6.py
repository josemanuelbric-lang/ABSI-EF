import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros de Simulación TDH ---
# Límite Físico (Escala de Planck simplificada)
LAMBDA_PLANK = 100 
# Número de Atomodimensionales (la cuantificación finita)
NUMERO_ATOMODIMENSIONALES = 10000

# Función de Densidad de Energía (Simulación: k^3)
def energia_densidad(k):
    return k**3

# --- 1. Cálculo de la TQC (Continuo) ---
# Se utiliza una integral numérica (el área bajo la curva)
k_continuo = np.linspace(0, LAMBDA_PLANK, 500) # Muchos puntos para simular la continuidad
densidad_continua = energia_densidad(k_continuo)

# El Valor Total TQC (Área total bajo la curva)
area_total_tqc = (1/4) * (LAMBDA_PLANK**4) 

# --- 2. Cálculo de la TDH (Discreto y Contable) ---
# Se utiliza la suma de los Atomodimensionales (A_n)
k_tdh_discreto = np.linspace(0, LAMBDA_PLANK, NUMERO_ATOMODIMENSIONALES + 1)
# El ancho de cada A_n (el paso discreto)
dk_tdh = k_tdh_discreto[1] - k_tdh_discreto[0] 
# La altura de cada Atomodimensional
altura_tdh = energia_densidad(k_tdh_discreto[:-1]) 
# El Valor Total TDH (Suma de las áreas de los rectángulos)
area_total_tdh = np.sum(altura_tdh * dk_tdh)

# --- 3. Generación de la Gráfica ---
plt.figure(figsize=(10, 6))

# Gráfico 1: TQC (La curva continua)
plt.plot(k_continuo, densidad_continua, label=r'Densidad Continua TQC ($\propto k^3$)', color='blue', linewidth=2)

# Gráfico 2: TDH (Los rectángulos discretos / Atomodimensionales)
plt.bar(k_tdh_discreto[:-1], altura_tdh, width=dk_tdh, 
        align='edge', alpha=0.6, color='red', edgecolor='black', 
        label=r'Atomodimensionales TDH ($A_n$)')

# Etiqueta de Límite (Planck)
plt.axvline(x=LAMBDA_PLANK, color='green', linestyle='--', 
            label=r'Límite Físico ($\Lambda$, finito)')

# Títulos y Etiquetas
plt.title(f'Reducción de la Divergencia: TQC (Continuo) vs TDH (Discreto, |D|={NUMERO_ATOMODIMENSIONALES})')
plt.xlabel(r'Momento/Escala de Energía ($k$)')
plt.ylabel(r'Densidad de Energía del Vacío ($\propto k^3$)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# Imprime los resultados para la comprobación
print(f"\n--- Resultados de la Comprobación Numérica ---")
print(f"Límite (Λ): {LAMBDA_PLANK}")
print(f"Predicción Teórica TQC (1/4 * Λ^4): {area_total_tqc:,.2f} u.")
print(f"Predicción Física TDH (Suma de A_n): {area_total_tdh:,.2f} u.")
print(f"Diferencia (Error de la discretización): {area_total_tqc - area_total_tdh:,.2f} u.")