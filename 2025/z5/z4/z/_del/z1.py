import numpy as np
import matplotlib.pyplot as plt

# 1. Definición de Constantes y Cargas
c = 3.0e8    # Velocidad de la luz
kappa_E = (8 * np.pi * 6.674e-11) / (c**4)  # Constante de Einstein (kappa_E)

# 2. Definición de Fuentes (Densidad de Energía T_00)
# Densidad de Materia (T_mat > 0)
rho_matter = np.linspace(0, 1e-25, 100) # Rango de densidades de materia (kg/m^3)
T_mat_00 = rho_matter * c**2

# Densidad de Energía Oscura (T_oscura_00 < 0 por su presión negativa)
# La energía oscura es casi constante en el espacio y tiempo (Presión negativa)
# Aquí la modelamos como una Densidad de Energía equivalente negativa (T_00 < 0)
# para causar Repulsión, o simplemente como un valor constante negativo.
T_oscura_00 = np.full(100, -1e-10 * c**2) # Una fuente equivalente negativa y constante

# 3. Curvatura (Componente 00 de G_mu_nu)
# G_00 (Curvatura) = kappa_E * T_00
G_mat_00 = kappa_E * T_mat_00
G_oscura_00 = kappa_E * T_oscura_00
G_total_00 = G_mat_00 + G_oscura_00

# 4. Graficar la Relación Curvatura vs. Fuente (Densidad)
plt.figure(figsize=(10, 6))

# Materia (Atracción)
plt.plot(rho_matter, G_mat_00, label='Materia Ordinaria (Atracción)', color='blue')

# Energía Oscura (Repulsión) - La curvatura G_00 es constante y negativa
plt.plot(rho_matter, G_oscura_00, label='Energía Oscura (Repulsión)', linestyle='--', color='red')

# Curvatura Total
plt.plot(rho_matter, G_total_00, label='Curvatura Total (Materia + Oscura)', color='green', linewidth=2)

plt.xlabel(r'Densidad de Materia $\rho$ (kg/m$^3$)')
plt.ylabel(r'Curvatura del Espacio-Tiempo $G_{00}$ (m$^{-2}$)')
plt.title('Curvatura del Espacio-Tiempo vs. Fuente (Materia y Energía Oscura)')
plt.legend()
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.show()