import numpy as np
import matplotlib.pyplot as plt

# Parámetros Fijos
D = 4.0
F = 3.0

# Valores Observados (Objetivos)
OBS_ALPHA_INV = 137.036
OBS_MW = 80.379  # GeV (Valor observado y refinado)

# Rango de la Tensión Maestra N (Exploramos el equilibrio cerca de 4)
N_range = np.linspace(3.5, 4.5, 500)

# --- Definición de las Funciones de la TDH ---

# 1. Función para Alpha Inverso (Electromagnetismo)
# f_alpha_inv(N) = (D^F + F^D) - N * (1 + N/D)
def f_alpha_inv(N):
    return (D**F + F**D) - N * (1 + N/D)

# 2. Función para la Masa del Bosón W (Fuerza Débil)
# f_mW(N) = (F^D * D) / N
def f_mW(N):
    return (F**D * D) / N

# Calculamos los valores de las funciones en el rango N
y_alpha_inv = f_alpha_inv(N_range)
y_mW = f_mW(N_range)

# --- Configuración y Generación de la Gráfica ---

fig, ax1 = plt.subplots(figsize=(10, 6))

# Eje X: Tensión Maestra N
ax1.set_xlabel('Tensión Maestra (N)', fontsize=12)

# --- Curva 1: Alpha Inverso (Eje Y Izquierdo) ---
color_alpha = 'tab:blue'
ax1.set_ylabel(r'$\alpha^{-1}$ (Electromagnetismo)', color=color_alpha, fontsize=12)
ax1.plot(N_range, y_alpha_inv, color=color_alpha, label=r'TDH: $f_{\alpha^{-1}}(N)$')
ax1.tick_params(axis='y', labelcolor=color_alpha)

# Línea Horizontal del Valor Observado de Alpha Inversoimport numpy as np
import matplotlib.pyplot as plt

# Parámetros Fijos
D = 4.0
F = 3.0

# Valores Observados (Objetivos)
OBS_ALPHA_INV = 137.036
OBS_MW = 80.379  # GeV (Valor observado y refinado)

# Rango de la Tensión Maestra N (Exploramos el equilibrio cerca de 4)
N_range = np.linspace(3.5, 4.5, 500)

# --- Definición de las Funciones de la TDH ---

# 1. Función para Alpha Inverso (Electromagnetismo)
# f_alpha_inv(N) = (D^F + F^D) - N * (1 + N/D)
def f_alpha_inv(N):
    return (D**F + F**D) - N * (1 + N/D)

# 2. Función para la Masa del Bosón W (Fuerza Débil)
# f_mW(N) = (F^D * D) / N
def f_mW(N):
    return (F**D * D) / N

# Calculamos los valores de las funciones en el rango N
y_alpha_inv = f_alpha_inv(N_range)
y_mW = f_mW(N_range)

# --- Configuración y Generación de la Gráfica ---

fig, ax1 = plt.subplots(figsize=(10, 6))

# Eje X: Tensión Maestra N
ax1.set_xlabel('Tensión Maestra (N)', fontsize=12)

# --- Curva 1: Alpha Inverso (Eje Y Izquierdo) ---
color_alpha = 'tab:blue'
ax1.set_ylabel(r'$\alpha^{-1}$ (Electromagnetismo)', color=color_alpha, fontsize=12)
ax1.plot(N_range, y_alpha_inv, color=color_alpha, label=r'TDH: $f_{\alpha^{-1}}(N)$')
ax1.tick_params(axis='y', labelcolor=color_alpha)

# Línea Horizontal del Valor Observado de Alpha Inverso
ax1.axhline(OBS_ALPHA_INV, color=color_alpha, linestyle='--', linewidth=1, label=r'Observado: $\alpha^{-1}$' )

# --- Curva 2: Masa del Bosón W (Eje Y Derecho) ---
ax2 = ax1.twinx()  # Crea un segundo eje Y que comparte el mismo eje X
color_mW = 'tab:red'
ax2.set_ylabel(r'$m_W$ (GeV) (Fuerza Débil)', color=color_mW, fontsize=12)
ax2.plot(N_range, y_mW, color=color_mW, linestyle='-', label=r'TDH: $f_{m_W}(N)$')
ax2.tick_params(axis='y', labelcolor=color_mW)

# Línea Horizontal del Valor Observado de m_W
ax2.axhline(OBS_MW, color=color_mW, linestyle='--', linewidth=1, label=r'Observado: $m_W$')

# --- Marcadores de Convergencia ---
# El valor de N=3.8710
N_TDH = 3.8710
ax1.axvline(N_TDH, color='k', linestyle=':', linewidth=1.5, label=f'N = {N_TDH}')
ax1.annotate(f'N = {N_TDH}', xy=(N_TDH, 140), xytext=(N_TDH + 0.05, 140),
             arrowprops=dict(facecolor='black', shrink=0.05, width=0.5), fontsize=10)

# Leyendas
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
plt.title('Convergencia Estructural de las Constantes Físicas en función de N', fontsize=14)
plt.grid(True, linestyle='dotted', alpha=0.5)
plt.show()

# --- Se puede insertar un tag de imagen aquí para ilustrar la gráfica ---
#
ax1.axhline(OBS_ALPHA_INV, color=color_alpha, linestyle='--', linewidth=1, label=r'Observado: $\alpha^{-1}$' )

# --- Curva 2: Masa del Bosón W (Eje Y Derecho) ---
ax2 = ax1.twinx()  # Crea un segundo eje Y que comparte el mismo eje X
color_mW = 'tab:red'
ax2.set_ylabel(r'$m_W$ (GeV) (Fuerza Débil)', color=color_mW, fontsize=12)
ax2.plot(N_range, y_mW, color=color_mW, linestyle='-', label=r'TDH: $f_{m_W}(N)$')
ax2.tick_params(axis='y', labelcolor=color_mW)

# Línea Horizontal del Valor Observado de m_W
ax2.axhline(OBS_MW, color=color_mW, linestyle='--', linewidth=1, label=r'Observado: $m_W$')

# --- Marcadores de Convergencia ---
# El valor de N=3.8710
N_TDH = 3.8710
ax1.axvline(N_TDH, color='k', linestyle=':', linewidth=1.5, label=f'N = {N_TDH}')
ax1.annotate(f'N = {N_TDH}', xy=(N_TDH, 140), xytext=(N_TDH + 0.05, 140),
             arrowprops=dict(facecolor='black', shrink=0.05, width=0.5), fontsize=10)

# Leyendas
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
plt.title('Convergencia Estructural de las Constantes Físicas en función de N', fontsize=14)
plt.grid(True, linestyle='dotted', alpha=0.5)
plt.show()

# --- Se puede insertar un tag de imagen aquí para ilustrar la gráfica ---
#