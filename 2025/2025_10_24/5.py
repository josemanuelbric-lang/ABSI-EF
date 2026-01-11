import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, fixed, HBox, VBox, Layout
from IPython.display import display, clear_output

# ==========================================================
# 1. CLASE CuerpoDimensional (sin cambios)
# ==========================================================

class CuerpoDimensional:
    def __init__(self, nombre, x, y, tension_sigma):
        self.nombre = nombre
        # Posición inicial en el D4 (simplificada a 2D espacial)
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0], dtype=float) 
        # Tensión de Organización (Análogo a la masa/energía)
        self.sigma = tension_sigma 
        self.trayectoria = [self.pos.copy()]
        # Nueva propiedad para cuantificar la "resta de coordenadas temporales"
        self.tasa_tiempo_local = 1.0 
        self.registro_tasa_tiempo = [1.0]
        
    def calcular_fuerza_tension(self, otro_cuerpo):
        """Calcula la fuerza de reorganización de la Tensión (análogo a la gravedad)."""
        r_vec = otro_cuerpo.pos - self.pos
        r = np.linalg.norm(r_vec)
        
        # Constante de corte para evitar singularidades
        r = max(r, 0.5)

        # FÓRMULA DE INTERACCIÓN DE TENSIÓN: F ~ (sigma1 * sigma2) / r^2
        fuerza_mag = (self.sigma * otro_cuerpo.sigma) / (r**2)
        direccion_unit = r_vec / r
        
        return direccion_unit * fuerza_mag

    def calcular_potencial_tension(self, otro_cuerpo):
        """Calcula el Potencial de Tensión (análogo al potencial gravitatorio Phi).
            U = -G*M/r. Usaremos U ~ -sigma / r"""
        r = np.linalg.norm(otro_cuerpo.pos - self.pos)
        r = max(r, 0.5)
        # El Potencial es NEGATIVO y es más fuerte cerca de un cuerpo con alta sigma
        return -otro_cuerpo.sigma / r
        
# ==========================================================
# 2. FUNCIÓN DE SIMULACIÓN (simular_tension_emergente)
# ==========================================================

def simular_tension_emergente(cuerpos, pasos_totales, dt, C_AJUSTE_POTENCIAL):
    """Evoluciona el sistema de cuerpos a través del tiempo discreto (Delta tau)."""
    
    # Reiniciar trayectorias y registros para la nueva simulación
    for cuerpo in cuerpos:
        cuerpo.trayectoria = [cuerpo.pos.copy()]
        cuerpo.registro_tasa_tiempo = [1.0]

    for _ in range(pasos_totales):
        fuerzas_totales = [np.array([0.0, 0.0]) for _ in cuerpos]
        potenciales_totales = [0.0 for _ in cuerpos]
        
        # 2.1. CÁLCULO DE INTERACCIÓN (Tensión y Potencial)
        for i, c1 in enumerate(cuerpos):
            for j, c2 in enumerate(cuerpos):
                if i != j:
                    # Suma de fuerzas de reorganización (movimiento)
                    fuerzas_totales[i] += c1.calcular_fuerza_tension(c2)
                    # Suma de potenciales de tensión (dilatación del tiempo)
                    potenciales_totales[i] += c1.calcular_potencial_tension(c2)
        
        # 2.2. APLICACIÓN DE LA TENSIÓN (Movimiento)
        for i, cuerpo in enumerate(cuerpos):
            
            # --- CÁLCULO DE LA "RESTA TEMPORAL" (Dilatación) ---
            
            potencial_normalizado = -potenciales_totales[i] * C_AJUSTE_POTENCIAL
            
            if potencial_normalizado < 1.0:
                cuerpo.tasa_tiempo_local = np.sqrt(1.0 - potencial_normalizado)
            else:
                cuerpo.tasa_tiempo_local = 0.0 # Tiempo se detiene
                
            cuerpo.registro_tasa_tiempo.append(cuerpo.tasa_tiempo_local)
            
            # --- CÁLCULO DEL MOVIMIENTO ESPACIAL ---
            
            aceleracion = fuerzas_totales[i] / cuerpo.sigma
            
            # El tiempo discreto (dt) se ajusta por la tasa local de tiempo
            dt_local = dt * cuerpo.tasa_tiempo_local
            
            cuerpo.vel += aceleracion * dt_local
            cuerpo.pos += cuerpo.vel * dt_local
            
            cuerpo.trayectoria.append(cuerpo.pos.copy())

# ==========================================================
# 3. FUNCIÓN DE GRAFICADO
# ==========================================================

def graficar_simulacion(cuerpos_simulados, PASOS, DT, C_AJUSTE_POTENCIAL):
    """Ejecuta la simulación y grafica los resultados."""
    
    # NOTA: Los cuerpos deben ser re-inicializados si se van a cambiar sus parámetros 
    # de posición y velocidad inicial, pero para la interactividad simple 
    # asumimos que la simulación se reinicia con la misma configuración inicial.

    simular_tension_emergente(cuerpos_simulados, PASOS, DT, C_AJUSTE_POTENCIAL)

    # Visualización
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colores = ['orange', 'blue', 'green']

    # --- Gráfico 1: Trayectoria ---
    ax1 = axes[0]
    for i, cuerpo in enumerate(cuerpos_simulados):
        trayectoria_array = np.array(cuerpo.trayectoria)
        ax1.plot(trayectoria_array[:, 0], trayectoria_array[:, 1], 
                 label=f'Trayectoria {cuerpo.nombre}', color=colores[i], linewidth=1)
        # Posición final
        ax1.plot(cuerpo.pos[0], cuerpo.pos[1], 'o', color=colores[i], markersize=5) 

    ax1.set_title('1. Trayectoria Espacial (D4) - Efecto de la Tensión')
    ax1.set_xlabel('Coordenada Espacial X (D4)')
    ax1.set_ylabel('Coordenada Espacial Y (D4)')
    ax1.grid(True)
    ax1.legend()
    ax1.axis('equal')

    # --- Gráfico 2: Tasa de Tiempo ---
    ax2 = axes[1]
    # El eje X es el tiempo global
    tiempo_global = np.arange(0, PASOS * DT, DT) 
    
    for i, cuerpo in enumerate(cuerpos_simulados):
        registro = np.array(cuerpo.registro_tasa_tiempo)[:len(tiempo_global)]
        ax2.plot(tiempo_global, registro, label=f'Tasa $\\Delta t$ {cuerpo.nombre}', color=colores[i], linewidth=2)

    ax2.axhline(y=1.0, color='r', linestyle='--', label='Tasa de Tiempo Plana (1.0)')
    ax2.set_title('2. Resta de Coordenadas Temporales (Dilatación)')
    ax2.set_xlabel('Tiempo de Evolución ($\Delta\\tau$ Global)')
    ax2.set_ylabel('Tasa de Tiempo Local (1.0 = Tiempo normal)')
    ax2.set_ylim(0.0, 1.1)
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

# ==========================================================
# 4. CONFIGURACIÓN INICIAL Y WIDGETS
# ==========================================================

# 4.1. Configuración Inicial (para resetear)
def configurar_cuerpos(sigma_sol, vel_planeta, sigma_planeta, vel_luna, sigma_luna):
    """Crea y retorna los cuerpos con parámetros específicos."""
    c1 = CuerpoDimensional("Sol (D4)", 0, 0, sigma_sol)

    c2 = CuerpoDimensional("Planeta (D4)", 5, 0, sigma_planeta)
    c2.vel = np.array([0.0, vel_planeta]) 

    c3 = CuerpoDimensional("Luna (D4)", 6.5, 0, sigma_luna)
    c3.vel = np.array([0.0, vel_luna]) 

    return [c1, c2, c3]

# Parámetros por defecto
DEFAULT_PASOS = 5
DEFAULT_DT = 0.01
DEFAULT_C_AJUSTE = 0.005

# Cuerpo central
DEFAULT_SIGMA_SOL = 1.0
# Planeta
DEFAULT_VEL_PLANETA = 2.5
DEFAULT_SIGMA_PLANETA = 0.5
# Luna
DEFAULT_VEL_LUNA = 2.0
DEFAULT_SIGMA_LUNA = 0.1


# 4.2. Definición de Widgets 🎛️

# Parámetros de la simulación
pasos_widget = widgets.IntSlider(min=1000, max=10000, step=500, value=DEFAULT_PASOS, description='Pasos:', layout=Layout(width='auto'))
dt_widget = widgets.FloatSlider(min=0.001, max=0.1, step=0.005, value=DEFAULT_DT, description='$\Delta \\tau$ (dt):', layout=Layout(width='auto'))
c_ajuste_widget = widgets.FloatSlider(min=0.001, max=0.02, step=0.001, value=DEFAULT_C_AJUSTE, description='Ajuste Potencial:', layout=Layout(width='auto'))

# Parámetros del Sol
sigma_sol_widget = widgets.FloatSlider(min=50, max=200, step=5, value=DEFAULT_SIGMA_SOL, description='$\sigma$ Sol:', layout=Layout(width='auto'))

# Parámetros del Planeta
vel_planeta_widget = widgets.FloatSlider(min=1.0, max=4.0, step=0.1, value=DEFAULT_VEL_PLANETA, description='Vel Planeta:', layout=Layout(width='auto'))
sigma_planeta_widget = widgets.FloatSlider(min=0.1, max=5.0, step=0.1, value=DEFAULT_SIGMA_PLANETA, description='$\sigma$ Planeta:', layout=Layout(width='auto'))

# Parámetros de la Luna
vel_luna_widget = widgets.FloatSlider(min=1.0, max=4.0, step=0.1, value=DEFAULT_VEL_LUNA, description='Vel Luna:', layout=Layout(width='auto'))
sigma_luna_widget = widgets.FloatSlider(min=0.01, max=1.0, step=0.05, value=DEFAULT_SIGMA_LUNA, description='$\sigma$ Luna:', layout=Layout(width='auto'))


# 4.3. Función de Aleatorización 🎲
def aleatorizar_parametros(_):
    """Asigna valores aleatorios a los widgets de la simulación."""
    
    # Parámetros globales
    pasos_widget.value = np.random.choice([3000, 5000, 7000])
    dt_widget.value = np.round(np.random.uniform(0.005, 0.05), 3)
    c_ajuste_widget.value = np.round(np.random.uniform(0.001, 0.015), 3)

    # Cuerpo central (Sol)
    sigma_sol_widget.value = np.round(np.random.uniform(80, 150), 1)

    # Planeta
    vel_planeta_widget.value = np.round(np.random.uniform(1.5, 3.5), 1)
    sigma_planeta_widget.value = np.round(np.random.uniform(0.2, 2.0), 1)

    # Luna
    vel_luna_widget.value = np.round(np.random.uniform(1.5, 3.0), 1)
    sigma_luna_widget.value = np.round(np.random.uniform(0.05, 0.5), 2)
    
# 4.4. Botón de Aleatorizar y Botón de Reset
boton_aleatorizar = widgets.Button(description="🎲 Aleatorizar Parámetros", button_style='info')
boton_aleatorizar.on_click(aleatorizar_parametros)

def reset_parametros(_):
    """Resetea los parámetros a sus valores por defecto."""
    pasos_widget.value = DEFAULT_PASOS
    dt_widget.value = DEFAULT_DT
    c_ajuste_widget.value = DEFAULT_C_AJUSTE
    sigma_sol_widget.value = DEFAULT_SIGMA_SOL
    vel_planeta_widget.value = DEFAULT_VEL_PLANETA
    sigma_planeta_widget.value = DEFAULT_SIGMA_PLANETA
    vel_luna_widget.value = DEFAULT_VEL_LUNA
    sigma_luna_widget.value = DEFAULT_SIGMA_LUNA

boton_reset = widgets.Button(description="🔄 Resetear", button_style='warning')
boton_reset.on_click(reset_parametros)


# 4.5. Configuración del Layout
controles_sim = VBox([pasos_widget, dt_widget, c_ajuste_widget], layout=Layout(border='solid 1px black', padding='5px', margin='2px'))
controles_sol = VBox([sigma_sol_widget], layout=Layout(border='solid 1px black', padding='5px', margin='2px'))
controles_planeta = VBox([vel_planeta_widget, sigma_planeta_widget], layout=Layout(border='solid 1px black', padding='5px', margin='2px'))
controles_luna = VBox([vel_luna_widget, sigma_luna_widget], layout=Layout(border='solid 1px black', padding='5px', margin='2px'))

controles_interactivos = HBox([
    controles_sim,
    controles_sol,
    controles_planeta,
    controles_luna
])

botones = HBox([boton_aleatorizar, boton_reset])


# 4.6. Función de Enlace y Ejecución
def actualizar_y_graficar(PASOS, DT, C_AJUSTE_POTENCIAL, SIGMA_SOL, VEL_PLANETA, SIGMA_PLANETA, VEL_LUNA, SIGMA_LUNA):
    """Función de callback para el widget interactivo."""
    # Reconfigurar cuerpos con los nuevos parámetros del slider
    cuerpos = configurar_cuerpos(SIGMA_SOL, VEL_PLANETA, SIGMA_PLANETA, VEL_LUNA, SIGMA_LUNA)
    graficar_simulacion(cuerpos, PASOS, DT, C_AJUSTE_POTENCIAL)


# El widget 'interact' une los controles a la función de graficado
interfaz = interact(
    actualizar_y_graficar,
    PASOS=pasos_widget,
    DT=dt_widget,
    C_AJUSTE_POTENCIAL=c_ajuste_widget,
    SIGMA_SOL=sigma_sol_widget,
    VEL_PLANETA=vel_planeta_widget,
    SIGMA_PLANETA=sigma_planeta_widget,
    VEL_LUNA=vel_luna_widget,
    SIGMA_LUNA=sigma_luna_widget
)

# Mostrar los controles y botones
display(botones, controles_interactivos)