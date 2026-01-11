import numpy as np
import matplotlib.pyplot as plt

# --- Constantes Fundamentales de la TDH ---
D = 4       # Dimensionalidad
F = 3       # Familias
N_real = 3.8710 # Tensión Maestra Real

# --- VALORES REALES OBSERVADOS (Contexto Físico) ---
# La realidad a la que apunta la TDH
REAL_VALUES = {
    "EM": 137.036,      # Inverso de la Constante de Estructura Fina
    "Fuerte": 0.118,    # Constante de Acoplamiento Fuerte (a m_Z)
    "Debil": 80.379,    # Masa del Bosón W (GeV)
    "Gravedad": 36.0    # Exponente Jerárquico (log10)
}

# --- LEYES ESTRUCTURALES DE LA TDH (f(N)) ---

# 1. Fuerza Electromagnética (Alpha^-1)
# f(N) = (D^F + F^D) - N * (1 + N/D)
def f_em(N):
    return (D**F + F**D) - (N * (1 + N / D))

# 2. Fuerza Nuclear Fuerte (Alpha_s)
# f(N) = (F * (D - N)) / (D + F - N)
def f_fuerte(N):
    # D + F - N es el Amortiguador de Tensión Lineal (3.129 en N_real)
    return (F * (D - N)) / (D + F - N)

# 3. Fuerza Nuclear Débil (Masa W, GeV)
# f(N) = (F^D * D) / N
def f_debil(N):
    # F^D * D es el Esfuerzo de Tensión Total (324)
    return (F**D * D) / N

# 4. Fuerza Gravitatoria (Exponente E_36)
# f(N) = (D * F * ((D * F) / N)) - ((D**F) / (N**F))
def f_gravitatoria(N):
    # (D*F/N) es el Factor de Eficiencia Dimensional
    return (D * F * ((D * F) / N)) - ((D**F) / (N**F))

# --- CÁLCULO DE EJEMPLOS REALES ---
# Aplicar N_real (3.8710) a cada función
resultados_tdh = {
    "EM": f_em(N_real),
    "Fuerte": f_fuerte(N_real),
    "Debil": f_debil(N_real),
    "Gravedad": f_gravitatoria(N_real)
}

# --- VISUALIZACIÓN EN GRÁFICA ---
N_sim = np.linspace(3.0, 4.0, 100) # Simular N para el eje X

fig, axs = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Leyes Estructurales de la TDH: Calibración de las 4 Fuerzas por la Tensión Maestra (N)', fontsize=16)

# 1. Electromagnética
axs[0, 0].plot(N_sim, f_em(N_sim), label=r'$f_{EM}(N)$ TDH')
axs[0, 0].axvline(N_real, color='grey', linestyle='--', label=f'N Real ({N_real})')
axs[0, 0].axhline(REAL_VALUES['EM'], color='blue', linestyle=':', label=f'Observado ({REAL_VALUES["EM"]})')
axs[0, 0].plot(N_real, resultados_tdh['EM'], 'ro', label=f'TDH={resultados_tdh["EM"]:.4f}')
axs[0, 0].set_title(r'Fuerza EM ($\alpha^{-1}$) vs. $N$')
axs[0, 0].set_ylabel('Valor de $\\alpha^{-1}$')
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# 2. Nuclear Fuerte
axs[0, 1].plot(N_sim, f_fuerte(N_sim), label=r'$f_{Fuerte}(N)$ TDH', color='red')
axs[0, 1].axvline(N_real, color='grey', linestyle='--')
axs[0, 1].axhline(REAL_VALUES['Fuerte'], color='red', linestyle=':', label=f'Observado ({REAL_VALUES["Fuerte"]})')
axs[0, 1].plot(N_real, resultados_tdh['Fuerte'], 'bo', label=f'TDH={resultados_tdh["Fuerte"]:.4f}')
axs[0, 1].set_title(r'Fuerza Nuclear Fuerte ($\alpha_s$) vs. $N$')
axs[0, 1].set_ylabel('Valor de $\\alpha_s$')
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.3)

# 3. Nuclear Débil (Masa W)
axs[1, 0].plot(N_sim, f_debil(N_sim), label=r'$f_{Debil}(N)$ TDH', color='green')
axs[1, 0].axvline(N_real, color='grey', linestyle='--')
axs[1, 0].axhline(REAL_VALUES['Debil'], color='green', linestyle=':', label=f'Observado ({REAL_VALUES["Debil"]} GeV)')
axs[1, 0].plot(N_real, resultados_tdh['Debil'], 'ko', label=f'TDH={resultados_tdh["Debil"]:.4f} GeV')
axs[1, 0].set_title('Masa del Bosón W vs. $N$')
axs[1, 0].set_ylabel('Masa (GeV)')
axs[1, 0].set_xlabel(r'Tensión Maestra Simulada ($N$)')
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.3)

# 4. Gravitatoria (Exponente E_36)
axs[1, 1].plot(N_sim, f_gravitatoria(N_sim), label=r'$f_{Gravitatoria}(N)$ TDH', color='purple')
axs[1, 1].axvline(N_real, color='grey', linestyle='--')
axs[1, 1].axhline(REAL_VALUES['Gravedad'], color='purple', linestyle=':', label=f'Observado ({REAL_VALUES["Gravedad"]})')
axs[1, 1].plot(N_real, resultados_tdh['Gravedad'], 'yo', label=f'TDH={resultados_tdh["Gravedad"]:.4f}')
axs[1, 1].set_title(r'Jerarquía Gravitatoria ($E_{36}$) vs. $N$')
axs[1, 1].set_ylabel('Exponente Jerárquico')
axs[1, 1].set_xlabel(r'Tensión Maestra Simulada ($N$)')
axs[1, 1].legend()
axs[1, 1].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()

# --- Salida de Resultados de Ejemplo (TDH vs. Observado) ---
print("\n--- Resultados de Ejemplo (TDH vs. Observado) ---")
for force, tdh_value in resultados_tdh.items():
    obs_value = REAL_VALUES[force]
    print(f"{force.capitalize()}: TDH={tdh_value:.4f} | Obs={obs_value} | Error={abs(tdh_value - obs_value)/obs_value * 100:.2f}%")