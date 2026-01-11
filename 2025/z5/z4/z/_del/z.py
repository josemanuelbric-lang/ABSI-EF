import numpy as np
import matplotlib.pyplot as plt

# === CONSTANTES FUNDAMENTALES (Para la Físicas) ===
# Usaremos una masa M grande y simplificaremos las constantes para que el gráfico sea legible.
G = 1.0  # Constante Gravitacional (simplificada para graficar)
c = 1.0  # Velocidad de la luz (simplificada)
M = 10.0 # Masa de la fuente (simulando T_mu_nu)

# Constante de Einstein (kappa_Einstein)
kappa_Einstein = (8 * np.pi * G) / (c**4)

# === 1) FUNCIÓN DE CAMPO GRAVITACIONAL ESCALAR (Magnitud de la Fuerza/Campo) ===
# La magnitud del campo gravitacional (g) sigue una ley 1/r^2:
# |g| = G * M / r^2
def campo_gravitacional(r, M, G):
    """Calcula la magnitud del campo gravitacional G*M/r^2. Retorna np.inf si r es cero."""
    # Evita la división por cero
    r[r == 0] = np.finfo(float).eps  
    return (G * M) / (r**2)

# === 2) CONFIGURACIÓN DEL ESPACIO DE GRÁFICO (Ejes) ===
# Crea un rango de distancias 'r' (desde muy cerca hasta lejos)
r_min = 1.0
r_max = 50.0
r_values = np.linspace(r_min, r_max, 500)

# === 3) CÁLCULOS Y GRÁFICOS ===

# Calcular el campo (la intensidad del lado derecho de la ecuación)
intensidad_materia = campo_gravitacional(r_values, M, G)
intensidad_einstein = kappa_Einstein * intensidad_materia # Multiplicar por la constante de Einstein para relacionarlo

# --- Energía Oscura (Tensor Métrico relacionado) ---
# La energía oscura se representa con la Constante Cosmológica (Lambda).
# Su efecto es constante, NO depende de la distancia r, sino de Lambda * g_mu_nu.
# Asumimos una contribución constante y MUY PEQUEÑA para ser realista.
Lambda = 0.0001
intensidad_oscura = np.full_like(r_values, Lambda)

# === 4) VISUALIZACIÓN EN MATPLOTLIB ===
plt.figure(figsize=(10, 6))

# Trazar la intensidad de la Materia/Tensor T
plt.plot(r_values, intensidad_materia, label=r'$|\mathbf{T}|$ (Materia / $\mathbf{S}_{\mu\nu}$)', color='blue', linewidth=2)

# Trazar el lado derecho de la Ecuación de Einstein
plt.plot(r_values, intensidad_einstein, label=r'$\frac{8 \pi G}{c^4} |\mathbf{T}|$ (Lado Einstein)', linestyle='--', color='darkgreen')

# Trazar la Energía Oscura (Constante)
plt.plot(r_values, intensidad_oscura, label=r'$\Lambda$ (Energía Oscura)', color='red', linestyle=':', linewidth=3)

# Configuración del Título y Etiquetas
plt.title(r'Intensidad del Campo Gravitacional vs. Distancia ($1/r^2$)', fontsize=16)
plt.xlabel('Distancia Radial $r$', fontsize=14)
plt.ylabel('Intensidad del Campo ($|\mathbf{F}|$ o $|\mathbf{T}|$) (unidades arbitrarias)', fontsize=14)

# Configuración del Gráfico
plt.grid(True, linestyle='--')
plt.yscale('log') # Usar escala logarítmica para ver mejor la caída y el valor constante de Lambda
plt.xlim(r_min, r_max)
plt.legend()
plt.show()