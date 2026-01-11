import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --------------------------------------------------------------------------
## 1. Formalismo Teórico y Lagrangiano (Implementación Cosmológica)
# --------------------------------------------------------------------------

# A. La Ecuación de Campo de la Tensión Dinámica (FLRW Contexto)
# La Ecuación de Friedmann (derivada de G_00 = kappa * S_00)
# (H/H0)^2 = Omega_m * (1+z)^3 + Omega_rad * (1+z)^4 + Omega_DE * f_DE(z)
# Donde f_DE(z) es la densidad de Energía Oscura (TD) normalizada.

# B. Definición Rigurosa de S_mu_nu (Ecuación de Estado w)
# El Tensor de Tensión Dinámica (S_mu_nu) es la fuente de energía. 
# Si S_mu_nu se comporta como un fluido, su componente de 'Exceso de Tensión' (Energía Oscura) 
# tiene una densidad (rho_DE) que evoluciona según la ecuación de estado w:
# rho_DE(z) = rho_DE_0 * exp( -3 * integral( (1 + w(z))/(1+z) ) dz )

# Usamos la parametrización más simple: w es constante.
W_TD = -0.5000  # Valor óptimo de Tensión Dinámica (S>0) que encontraste
W_LCDM = -1.0   # Valor estándar de la Constante Cosmológica (Lambda)

# La función de evolución de la densidad normalizada para una w constante:
# f_DE(z) = (1+z)^(3 * (1 + w))
def get_E_sq(z, W_DE, O_M=0.3, O_R=0.0, O_DE=0.7):
    """Calcula (H(z)/H0)^2 para un modelo con Energía Oscura con Ecuación de Estado W_DE."""
    # Materia (Déficit de Tensión)
    rho_m = O_M * (1 + z)**3
    # Radiación (Se ignora para la cosmología tardía)
    rho_r = O_R * (1 + z)**4
    # Energía Oscura (Exceso de Tensión S > 0)
    rho_de = O_DE * (1 + z)**(3 * (1 + W_DE))
    
    return rho_m + rho_r + rho_de

# --------------------------------------------------------------------------
## 2. Comprobación (Integración Numérica de la Expansión)
# --------------------------------------------------------------------------

# Parámetros cosmológicos base
OMEGA_M = 0.3  # Densidad de Materia (incluye materia oscura)
OMEGA_DE = 1.0 - OMEGA_M # Densidad de Energía Oscura

# Definir la Ecuación de Friedmann como una ecuación diferencial para la edad del Universo:
# dt/da = 1 / (a * H(a))
def friedmann_equation(a, t, W_DE):
    """Función para el integrador: da/dt."""
    z = (1/a) - 1
    # H(z)^2 = H0^2 * E(z)^2
    E_sq = get_E_sq(z, W_DE, O_M=OMEGA_M, O_DE=OMEGA_DE)
    H_sq = E_sq * (1.0)**2  # Asumimos H0=1 para obtener H en unidades de H0
    
    H = np.sqrt(H_sq)
    return a * H # Retorna da/dt

# Resolver la ODE para ambos modelos (TD y LCDM)
a_initial = 1e-3 # Factor de escala inicial (cerca del Big Bang)
a_final = 1.1    # Factor de escala ligeramente mayor al actual (a=1)
t_span = [0, 100] # Rango de tiempo grande para asegurar que a_final se alcance

# Solución para el modelo TD
sol_td = solve_ivp(
    lambda t, a: friedmann_equation(a, t, W_TD), 
    t_span, 
    [a_initial], 
    dense_output=True, 
    method='RK45', 
    rtol=1e-8
)

# Solución para el modelo Lambda-CDM
sol_lcdm = solve_ivp(
    lambda t, a: friedmann_equation(a, t, W_LCDM), 
    t_span, 
    [a_initial], 
    dense_output=True, 
    method='RK45', 
    rtol=1e-8
)

# --------------------------------------------------------------------------
## 3. Visualización y Comprobación
# --------------------------------------------------------------------------

# Generar puntos de tiempo y factor de escala para la visualización
t_max = min(sol_td.t[-1], sol_lcdm.t[-1])
t_plot = np.linspace(0, t_max, 300)

a_td = sol_td.sol(t_plot)[0]
a_lcdm = sol_lcdm.sol(t_plot)[0]

# Gráfico 1: Evolución del Factor de Escala a(t)
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(t_plot, a_lcdm, label=r'$\Lambda\text{CDM} (w = -1.0)$', color='blue', linewidth=2)
plt.plot(t_plot, a_td, label=f'Tensión Dinámica $(w = {W_TD:.2f})$', color='red', linestyle='--', linewidth=2)
plt.axhline(1.0, color='black', linestyle=':', alpha=0.7, label='Presente ($a=1.0$)')
plt.title(r'Evolución del Factor de Escala $a(t)$')
plt.xlabel(r'Tiempo (unidades de $1/H_0$)')
plt.ylabel(r'Factor de Escala $a$')
plt.legend()
plt.grid(True)

# Gráfico 2: Densidad de Energía Oscura (f_DE(z))
z_plot = np.linspace(0.0, 3.0, 100)

rho_de_td = OMEGA_DE * (1 + z_plot)**(3 * (1 + W_TD))
rho_de_lcdm = OMEGA_DE * (1 + z_plot)**(3 * (1 + W_LCDM)) # Se simplifica a Omega_DE

plt.subplot(1, 2, 2)
plt.plot(z_plot, rho_de_lcdm, label=r'$\Lambda\text{CDM} (w = -1.0)$', color='blue', linewidth=2)
plt.plot(z_plot, rho_de_td, label=f'Tensión Dinámica $(w = {W_TD:.2f})$', color='red', linestyle='--', linewidth=2)
plt.title(r'Densidad de Energía Oscura $f_{DE}(z)$')
plt.xlabel('Corrimiento al rojo (z)')
plt.ylabel(r'$\Omega_{DE}(z) / \Omega_{DE,0}$')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------
## Conclusión de la Comprobación
# --------------------------------------------------------------------------

print("\n--- Conclusión (Comprobación de la Tensión Dinámica) ---")
print(f"La implementación de TD usa w = {W_TD} (su Exceso de Tensión S>0).")
print(f"El modelo LCDM (w = {W_LCDM}) asume que la densidad de Energía Oscura es constante con el tiempo.")

# El tiempo en el que a=1 es la edad del universo (en unidades de 1/H0)
try:
    t_age_td = sol_td.sol(1.0)[0]
    t_age_lcdm = sol_lcdm.sol(1.0)[0]
    
    print("\nResultados de la Integración (Edad del Universo):")
    print(f"Edad (TD, w={W_TD}): {t_age_td:.3f} (unidades de 1/H0)")
    print(f"Edad (LCDM, w={W_LCDM}): {t_age_lcdm:.3f} (unidades de 1/H0)")
    
    if t_age_td > t_age_lcdm:
        print("\nInterpretación:")
        print("El modelo de Tensión Dinámica (TD) predice un Universo ligeramente MÁS VIEJO.")
        print("Esto se debe a que su densidad de Exceso de Tensión (rho_DE) DISMINUYE con el tiempo (Gráfico 2),")
        print("lo que implica un frenado de la expansión en el pasado en comparación con LCDM.")
    else:
        print("\nInterpretación:")
        print("El modelo de Tensión Dinámica (TD) predice un Universo ligeramente MÁS JOVEN.")
        print("Esto se debe a que su densidad de Exceso de Tensión (rho_DE) AUMENTA con el tiempo o disminuye más lentamente que en LCDM.")

except:
    print("\nNo se pudo calcular la edad del Universo (a=1) con precisión.")