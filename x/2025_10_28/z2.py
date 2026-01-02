import numpy as np
import matplotlib.pyplot as plt

# --- 1. Constantes y Parámetros del Modelo de Tensión Dinámica (TD) ---

# Constantes de Fuerza
G = 1.0           # Constante Gravitacional (simplificada)
M_star = 100.0    # Masa de la estrella central
M_planet = 0.1    # Masa de cada planeta

# Constantes de Tensión
# Coeficiente para el Déficit de Tensión (S < 0 -> Atracción)
C_D_TENSION = G * M_star * M_planet  # Valor: 10.0
# Coeficiente para el Exceso de Tensión (S > 0 -> Repulsión)
C_E_TENSION = 0.005 * M_planet       # Valor: 0.0005

# Cálculo del Radio Crítico (Rc) donde F_Atraccion = F_Repulsion
R_critico = (C_D_TENSION / C_E_TENSION)**(1/3)
print(f"El Radio Crítico (Rc) donde la fuerza es nula es: {R_critico:.3f} unidades.")

# Parámetros de la simulación
num_planetas = 4  # CAMBIO CLAVE: Solo 4 planetas
tiempo_total = 15.0 # Aumentamos el tiempo para ver mejor el crecimiento
dt = 0.5
num_pasos = int(tiempo_total / dt)
num_orbits_to_plot = 4 # Trazamos las 4 órbitas

# --- 2. Inicialización del Sistema Planetario ---

# Radios iniciales bien espaciados para los 4 planetas
r_initial_list = np.array([3.0, 7.0, 11.0, 15.0]) 
theta_initial_list = np.random.uniform(0, 2 * np.pi, num_planetas) # Ángulos aleatorios

x = r_initial_list * np.cos(theta_initial_list)
y = r_initial_list * np.sin(theta_initial_list)

# Velocidades iniciales para órbita circular estable
v_kepler = np.sqrt(G * M_star / r_initial_list)
vx = -v_kepler * np.sin(theta_initial_list)
vy = v_kepler * np.cos(theta_initial_list)

center = np.array([0.0, 0.0])
posiciones_historicas = np.zeros((num_pasos, num_planetas, 2))
# Como solo hay 4, trazamos los 4
indices_to_plot = np.arange(num_planetas) 

# --- 3. Bucle de Simulación (Mecánica TD) ---

for paso in range(num_pasos):
    r_vec = np.array([x, y]).T - center
    r_mag = np.linalg.norm(r_vec, axis=1)
    r_mag[r_mag < 0.1] = 0.1 
    r_unit = r_vec / r_mag[:, np.newaxis]
    
    # Déficit de Tensión (S < 0) -> Atracción
    F_deficit_tension_mag = C_D_TENSION / (r_mag**2)
    F_deficit_tension_vec = -F_deficit_tension_mag[:, np.newaxis] * r_unit

    # Exceso de Tensión (S > 0) -> Repulsión
    F_exceso_tension_mag = C_E_TENSION * r_mag
    F_exceso_tension_vec = F_exceso_tension_mag[:, np.newaxis] * r_unit

    # Fuerza Total Neta
    F_total_vec = F_deficit_tension_vec + F_exceso_tension_vec
    
    # Integración
    ax = F_total_vec[:, 0] / M_planet
    ay = F_total_vec[:, 1] / M_planet
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt

    posiciones_historicas[paso] = np.array([x, y]).T

# --- 4. Visualización A. Sistema Planetario (Trayectorias más limpias) ---

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
# Planetas Iniciales
plt.scatter(posiciones_historicas[0, :, 0], posiciones_historicas[0, :, 1], 
            s=50, color='lightblue', alpha=0.8, label='Posición Inicial')

# Trazar órbitas
for i in indices_to_plot:
     plt.plot(posiciones_historicas[:, i, 0], posiciones_historicas[:, i, 1], 
              alpha=0.6, linewidth=1.5, linestyle='-', label=f'Planeta {i+1}')
    
# Planetas Finales
plt.scatter(posiciones_historicas[-1, :, 0], posiciones_historicas[-1, :, 1], 
            s=100, color='red', alpha=0.9, label='Posición Final')
    
# Estrella Central
plt.scatter(center[0], center[1], s=400, marker='*', color='gold', edgecolor='black', label='Estrella Central')
plt.title(f'1. Sistema (1 Estrella, 4 Planetas) con Tensión Dinámica')
plt.xlabel('X (Unidades Arbitrarias)')
plt.ylabel('Y (Unidades Arbitrarias)')
plt.legend(fontsize=9)
plt.gca().set_aspect('equal', adjustable='box')

max_coord_sim = np.max(np.abs(posiciones_historicas)) + 5 
plt.xlim(-max_coord_sim, max_coord_sim)
plt.ylim(-max_coord_sim, max_coord_sim)

# --- 5. Visualización B. Radios de Crecimiento (Expansión Orbital) ---

distancias = np.linalg.norm(posiciones_historicas - center, axis=2)
tiempo = np.linspace(0, tiempo_total, num_pasos)

plt.subplot(1, 3, 2)
# Trazar la evolución del radio para cada uno de los 4 planetas
for i in indices_to_plot:
    plt.plot(tiempo, distancias[:, i], label=f'Planeta {i+1} (R={r_initial_list[i]:.1f})', linewidth=2)
    
plt.title('2. Radios de Crecimiento (Expansión Orbital)')
plt.xlabel('Tiempo (Pasos de Simulación)')
plt.ylabel('Distancia al Centro (Radio Orbital)')
plt.legend(fontsize=9)
plt.grid(True)


# --- 6. Visualización C. Radios de Actuación (Fuerza Neta) ---

r_plot = np.linspace(0.1, 40, 500) 

F_attr_plot = C_D_TENSION / (r_plot**2)
F_rep_plot = C_E_TENSION * r_plot
F_neta_plot = F_attr_plot - F_rep_plot

plt.subplot(1, 3, 3)
plt.plot(r_plot, F_attr_plot, label=r'Fuerza $S<0$ (Déficit/Atracción)', color='blue')
plt.plot(r_plot, F_rep_plot, label=r'Fuerza $S>0$ (Exceso/Repulsión)', color='orange')
plt.plot(r_plot, F_neta_plot, label='Fuerza Neta', color='red', linewidth=2)

# Marcar el Radio Crítico (Rc)
plt.axvline(R_critico, color='red', linestyle='--', label=f'$R_c \\approx {R_critico:.1f}$')
plt.axhline(0, color='black', linestyle='-', linewidth=0.5)

plt.title('3. Radios de Actuación de la Tensión Dinámica')
plt.xlabel('Distancia al Centro (r)')
plt.ylabel('Magnitud de la Fuerza (F)')
plt.legend(fontsize=8)
plt.ylim(-1, 5) 
plt.grid(True)
plt.tight_layout()
plt.show()