import numpy as np
import matplotlib.pyplot as plt

# --- Constantes de Referencia (RG) ---
# Usaremos unidades normalizadas donde G=c=M=1.
# Esto nos permite comparar la forma funcional de 1/r.
G = 6.674e-11   # Constante Gravitacional (m^3 kg^-1 s^-2)
c = 299792458   # Velocidad de la Luz (m/s)
M = 1.989e30    # Masa del Sol (M_sun)

# --- Parámetros de Simulación de Campo Débil ---
# Definimos un rango de distancia r (en unidades arbitrarias, ej. 10^11 m)
r_min = 1.0  # Unidad de distancia (ej. radio del cuerpo)
r_max = 100.0 # Distancia lejana
r = np.linspace(r_min, r_max, 500)

# --- 1. Definición de la Curvatura (Potenciales Normalizados) ---

# Potencial RG (Newtoniano/Schwarzschild): U_RG ~ 1/r
# La forma funcional de RG (Schwarzschild) es: 1 - (2GM / (c^2 * r))
def metric_g00_RG(r, G_eff, M_eff):
    """
    Representa el término de curvatura de la métrica g_00 en campo débil.
    Normalizamos las constantes a 1 para comparar la dependencia 1/r.
    """
    # En unidades normalizadas, esto es simplemente 1/r
    return -1.0 + (1.0 / r) 

# Potencial Modelo TD: U_TD ~ 1/r (con acoplamiento a la Tensión)
# Asumimos que su modelo también sigue una ley 1/r en campo débil, pero con 
# una "carga" diferente (Tensión sigma vs. Masa M).
# Para la visualización, la forma funcional es la misma (1/r), 
# pero el coeficiente es diferente.
def metric_g00_TD(r, alpha_sigma):
    """
    Representa el término de curvatura de su modelo TD.
    Aquí, 'alpha_sigma' representa el acoplamiento efectivo (α*σ).
    """
    # Usaremos un coeficiente 'alpha_sigma' que da una ligera diferencia 
    # de fuerza respecto a RG (ej. 0.95 * 1/r)
    return -1.0 + (alpha_sigma / r)

# --- Parámetros de Acoplamiento Efectivo (Ajuste) ---
# Usamos un factor de escala para mostrar la diferencia:
alpha_sigma_TD = 0.95 # El acoplamiento efectivo en su modelo
G_eff_RG = 1.0      # El acoplamiento efectivo en RG (GM)

# --- 2. Cálculo de la Métrica Modificada (Desviación del Espacio Plano) ---
# Queremos ver qué tanto se desvía el g_00 de -1 (espacio plano)
# La magnitud de la curvatura es |g_00 + 1|
curvatura_TD = np.abs(metric_g00_TD(r, alpha_sigma_TD) + 1.0)
curvatura_RG = np.abs(metric_g00_RG(r, G_eff_RG, M) + 1.0)


# --- 3. Visualización de las Curvaturas ---
plt.figure(figsize=(10, 6))

# a) Curvatura absoluta
plt.plot(r, curvatura_TD, label=r'Modelo TD ($\propto \alpha\sigma/r$)', color='blue')
plt.plot(r, curvatura_RG, label=r'Relatividad General ($\propto GM/r$)', color='red', linestyle='--')

plt.yscale('log') # Escala logarítmica para ver la caída 1/r
plt.xscale('log')

plt.xlabel(r'Distancia Normalizada ($r/r_0$)')
plt.ylabel(r'Magnitud de la Curvatura ($\approx |g_{00} + 1|$)')
plt.title('Comparación de Curvaturas de Campo Débil (Potenciales 1/r)')
plt.legend()
plt.grid(True, which="both", ls="--")

# b) Visualización de la Diferencia Relativa
plt.figure(figsize=(10, 4))
diferencia_relativa = (curvatura_TD - curvatura_RG) / curvatura_RG * 100

plt.plot(r, diferencia_relativa, color='purple')
plt.axhline(0, color='black', linestyle=':', linewidth=0.8)
plt.axhline((alpha_sigma_TD - G_eff_RG) / G_eff_RG * 100, color='gray', linestyle='--')

plt.xlabel(r'Distancia Normalizada ($r/r_0$)')
plt.ylabel(r'Diferencia Relativa de Curvatura (\%)')
plt.title(r'Diferencia entre la Curvatura TD y RG')
plt.grid(True, which="both", ls="--")
plt.show()

# --- Conexión con los Resultados Cosmológicos ---
print("\n--- Conexión con los Resultados Cosmológicos ---")
print(f"El modelo TD tuvo w_sigma = -0.5772 y Omega_M = 0.1274.")
print("Este 'desajuste' cosmológico (w != -1 y Omega_M bajo) indica que su 'Tensión' (σ) tiene")
print("un efecto cosmológico diferente a la Constante Cosmológica de Einstein (Λ).")
print("Si su modelo fuera la fuente de la energía oscura, la constante de acoplamiento κ")
print("debería ser la causa de w != -1, diferenciando su modelo de RG a gran escala.")