import numpy as np
import matplotlib.pyplot as plt

# --- 1. Parámetros de la Observación (Planck/CMB, z ~ 1090) ---

# Resultado publicado: Delta_alpha / alpha = (0.0 +/- 3.7) x 10^-3
DELTA_ALPHA_OBSERVADO = 0.0
ERROR_OBSERVADO = 3.7e-3     

# --- 2. Parámetros de la TDH ---

D = 4.0
N_OBS = 3.8710 
EPSILON_OBS = (D - N_OBS) / D # 0.03225

# Rango de Tensión N para graficar (cercano a la perfección)
N_VALORES = np.linspace(3.8, 4.0, 100) 
EPSILON_TEORICO = (D - N_VALORES) / D

# Factor de escala para mapear epsilon a Delta_alpha / alpha
C_ESCALA = 1.0 
DELTA_ALPHA_TEORICO = C_ESCALA * EPSILON_TEORICO

# --- 3. Generación del Gráfico ---
plt.figure(figsize=(10, 6))

# Trazar la Hipótesis TDH
# Título con formato LaTeX simplificado
plt.plot(N_VALORES, DELTA_ALPHA_TEORICO * 1e3, color='orange', linestyle='-', 
         label=r'Hipótesis TDH: $\Delta\alpha/\alpha \propto (D-N)/D$')

# Marcar el punto de Perfección (N=4, Delta_alpha=0)
plt.axvline(x=4.0, color='gray', linestyle='--', alpha=0.6, label=r'Perfección N=4 ($\epsilon=0$)')

# Trazar la Restricción del CMB (Planck) - LÍNEA CORREGIDA
# La restricción es un intervalo de error centrado en Delta_alpha = 0
plt.axhspan(DELTA_ALPHA_OBSERVADO * 1e3 - ERROR_OBSERVADO * 1e3, 
            DELTA_ALPHA_OBSERVADO * 1e3 + ERROR_OBSERVADO * 1e3, 
            color='blue', alpha=0.3, label='Observación Planck (z ~ 1090)') # Etiqueta simplificada

plt.axhline(DELTA_ALPHA_OBSERVADO * 1e3, color='blue', linestyle='-', label=r'Planck Centro: $\Delta\alpha/\alpha = 0$')

# Marcar el punto de N Observable (P != NP)
plt.plot(N_OBS, EPSILON_OBS * 1e3, 'ro', label=r'N Observable ($\mathbf{N \approx 3.871}$)', markersize=8)

# Configuración del Gráfico
plt.xlabel(r'Tensión Maestra ($\mathbf{N}$)', fontsize=14)
plt.ylabel(r'$10^3 \times \frac{\Delta\alpha}{\alpha}$ (ppm/1000)', fontsize=14)
plt.title(r'Prueba de la TDH: Variación de $\alpha$ vs. Restricción del CMB', fontsize=16)
plt.grid(True, which='both', linestyle=':', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

print(f"\nCódigo ejecutado. Límite de Planck (z ~ 1090) graficado con un error de +/- {ERROR_OBSERVADO * 1e3:.1f} x 10^-3.")