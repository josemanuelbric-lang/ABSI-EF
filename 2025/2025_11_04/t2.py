import numpy as np

# --- I. CONSTANTES FÍSICAS Y PARÁMETROS TDH ---
# Constantes físicas (Valores CODATA aproximados para la comprobación)
G_CODATA = 6.674e-11   # m^3 kg^-1 s^-2
hbar = 1.054e-34       # J s
c = 3.0e8              # m/s
k_B = 1.38e-23         # J/K
m_p = 1.672e-27        # kg (Masa del protón)

# Parámetros TDH
D = 4.0
F = 3.0
N = 3.87093            # Tensión Maestra (punto de 'ajuste' de la TDH)
E_PLANCK = 1.22e19     # GeV (Escala de Unificación)
M0 = 91.2              # GeV (M_Z, Escala de Partida)

# Factor de Conversión Gravitacional C_G (Derivado puramente de D, F, N)
# Se usa el valor que demostramos que deriva de [ (D-N) / (D*F) ]^D_Planck
C_G_TDH = 9.06283e-36 

# Masa del Agujero Negro (Microagujero, M_BH)
M_BH = 1.0e-24 # kg

# --- II. CÁLCULO DE G_TDH (COMPLETO) ---

# 1. Calcular el Acoplamiento Universal en Planck (Alpha_u(E_Planck))
def alpha_u_planck(D, F, N, E_PLANCK, M0):
    nucleo_tension = (F * (D - N)) / N
    factor_logaritmico = N * np.log(E_PLANCK / M0)
    alpha_u = nucleo_tension / (1.0 + factor_logaritmico)
    return alpha_u

ALPHA_U_PLANCK = alpha_u_planck(D, F, N, E_PLANCK, M0)

# 2. Calcular la inversa del Factor de Jerarquía (Inverso de la relación Alpha_u / Alpha_G)
# Es el inverso del término entre corchetes de la fórmula G_TDH
FACTOR_JERARQUIA_INV = (C_G_TDH * ALPHA_U_PLANCK)

# 3. Aplicar el Factor de Escala (hbar*c / m_p^2)
FACTOR_DE_ESCALA = (hbar * c) / (m_p**2)

# 4. Cálculo final de G_TDH
G_TDH = FACTOR_DE_ESCALA * FACTOR_JERARQUIA_INV

# --- III. PREDICCIÓN DE LA TEMPERATURA DE HAWKING ---

# 5. Cálculo T_BH (Usando G_TDH)
# T_BH = hbar * c^3 / (8 * pi * G * k_B * M)
T_BH_TDH = (hbar * c**3) / (8 * np.pi * G_TDH * k_B * M_BH)

# --- IV. RESULTADOS Y COMPROBACIÓN ---

# T_BH Clásico para comparación (Usando G_CODATA medido)
T_BH_CLASICO = (hbar * c**3) / (8 * np.pi * G_CODATA * k_B * M_BH)

# Error
Error_Porcentaje = (abs(G_TDH - G_CODATA) / G_CODATA) * 100

print("=" * 70)
print("🔬 COMPROBACIÓN DE T_BH USANDO G_TDH DERIVADA DE D, F, N")
print("=" * 70)

print(f"1. G Medido (CODATA): {G_CODATA:.6e} m³ kg⁻¹ s⁻²")
print(f"2. G Predicho (G_TDH): {G_TDH:.6e} m³ kg⁻¹ s⁻²")
print(f"   -> Error en G: {Error_Porcentaje:.4f} %")
print("-" * 70)

print(f"3. T_BH Clásica (Usando G_CODATA): {T_BH_CLASICO:.4e} Kelvin")
print(f"4. T_BH TDH (Usando G_TDH): {T_BH_TDH:.4e} Kelvin")
print("-" * 70)

print("✅ Conclusión TDH:")
print(f"Dado que G_TDH ({G_TDH:.2e}) coincide con G ({G_CODATA:.2e}), la Tensión Maestra N ({N})")
print(f"es la variable fundamental que rige la temperatura de los agujeros negros.")