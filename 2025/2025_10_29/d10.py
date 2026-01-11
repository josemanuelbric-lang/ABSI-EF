import numpy as np
import matplotlib.pyplot as plt

# --- Datos Físicos Reales (Log10 de la Energía) ---
# Usamos el logaritmo de la energía de cada escala.
# La energía es proporcional a M^4.

# Dimensión D2: Escala de Planck
LOG_ENERGY_D2 = 120  # Log10(M_Planck^4) ~ 120 (en unidades GeV^4)

# Dimensión D3: Escala Electrodébil (Atenuación 2->3)
LOG_ENERGY_D3 = LOG_ENERGY_D2 - (3.8710 * 17) # 120 - (N * log|D_2_3|) ~ 54

# Dimensión D4: Escala Observada (Tensión Final)
LOG_ENERGY_D4 = LOG_ENERGY_D3 - (3.8710 * 14) # 54 - (N * log|D_3_4|) ~ 1.0

# Puntos de la Jerarquía
dimensiones = ['D2 (Planck)', 'D3 (Electrodoméstica)', 'D4 (Observada)']
log_tension = [LOG_ENERGY_D2, LOG_ENERGY_D3, LOG_ENERGY_D4]
indices = np.arange(len(dimensiones))

# --- Generación de la Gráfica ---
plt.figure(figsize=(10, 6))
plt.plot(indices, log_tension, marker='o', linestyle='-', color='blue', linewidth=3)

# Puntos y etiquetas
for i, (dim, tension) in enumerate(zip(dimensiones, log_tension)):
    plt.annotate(f'{dim}\n(log10 Tensión: {tension:.1f})', 
                 (i, tension), 
                 textcoords="offset points", 
                 xytext=(0,10), 
                 ha='center', 
                 fontsize=10)
    
# Línea de la Brecha
plt.plot([0, len(dimensiones) - 1], [LOG_ENERGY_D2, LOG_ENERGY_D4], 
         linestyle='--', color='red', alpha=0.5, 
         label=f'Atenuación Total ({LOG_ENERGY_D2:.0f} órdenes)')

# Títulos y Ejes
plt.title(r'Dilución Logarítmica de la Tensión del Vacío a través de la Jerarquía Dimensional ($\mathbf{N=3.87}$)')
plt.xlabel('Salto Dimensional')
plt.ylabel(r'Logaritmo Base 10 de la Densidad de Tensión ($\log_{10}(\rho_{vac})$)')
plt.xticks(indices, dimensiones)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()