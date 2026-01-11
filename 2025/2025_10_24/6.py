import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. Definición de Atomodimensionales (Estructuras de Cuerpos)
# ==========================================================

# Función auxiliar para re-inicializar cuerpos para el gráfico de Sigma
def configurar_cuerpos_inicial():
    c1 = CuerpoDimensional("Sol (D4)", 0, 0, 50.0)
    c2 = CuerpoDimensional("Planeta (D4)", 5, 0, 0.5)
    c2.vel = np.array([0.0, 2.5]) 
    c3 = CuerpoDimensional("Luna A (D4)", 5.5, 0, 0.1)
    c3.vel = np.array([0.0, 2.5]) 
    c4 = CuerpoDimensional("Luna B (D5)", 5.5, 0.5, 0.1)
    c4.vel = np.array([0.0, 2.5]) 
    return [c1, c2, c3, c4]
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
# 2. SIMULACIÓN DE EVOLUCIÓN DISCRETA (D4)
# ==========================================================

def simular_tension_emergente(cuerpos, pasos_totales, dt, tasa_transferencia):
    """Evoluciona el sistema de cuerpos a través del tiempo discreto (Delta tau)."""
    
    # Constante para escalar el potencial y evitar valores negativos en la raíz cuadrada
    C_AJUSTE_POTENCIAL = 0.005 
    
    # Identificadores de los cuerpos
    sol = cuerpos[0]
    lunas = cuerpos[2:] # Asumiendo que las Lunas están en las posiciones [2] en adelante

    for _ in range(pasos_totales):
        
        # ==========================================================
        # 2.0. APLICAR TRANSFERENCIA DE TENSIÓN (Masa)
        # ==========================================================
        
        # Tensión que se pierde por el Sol en este paso de tiempo
        sigma_perdida_sol = tasa_transferencia * dt 
        
        # Tensión total que ganarán las lunas
        sigma_ganada_lunas = sigma_perdida_sol
        
        # Pérdida del Sol:
        sol.sigma -= sigma_perdida_sol
        if sol.sigma < 0.0: sol.sigma = 0.0 # Evitar Tensión negativa
        
        # Ganancia de las Lunas: 
        # Repartimos la ganancia equitativamente entre todas las lunas
        sigma_por_luna = sigma_ganada_lunas / len(lunas)
        for luna in lunas:
            luna.sigma += sigma_por_luna

        # ==========================================================
        # 2.1 - 2.2. Cálculo de Interacción y Movimiento (Igual que antes)
        # ==========================================================

        fuerzas_totales = [np.array([0.0, 0.0]) for _ in cuerpos]
        potenciales_totales = [0.0 for _ in cuerpos]
        
        # Cálculo de Interacción (Fuerza y Potencial)
        for i, c1 in enumerate(cuerpos):
            for j, c2 in enumerate(cuerpos):
                if i != j:
                    fuerzas_totales[i] += c1.calcular_fuerza_tension(c2)
                    potenciales_totales[i] += c1.calcular_potencial_tension(c2)
        
        # Aplicación de la Tensión (Movimiento)
        for i, cuerpo in enumerate(cuerpos):
            
            # CÁLCULO DE LA "RESTA TEMPORAL" (Dilatación)
            potencial_normalizado = -potenciales_totales[i] * C_AJUSTE_POTENCIAL
            
            if potencial_normalizado < 1.0:
                cuerpo.tasa_tiempo_local = np.sqrt(1.0 - potencial_normalizado)
            else:
                cuerpo.tasa_tiempo_local = 0.0
                
            cuerpo.registro_tasa_tiempo.append(cuerpo.tasa_tiempo_local)
            
            # CÁLCULO DEL MOVIMIENTO ESPACIAL
            aceleracion = fuerzas_totales[i] / cuerpo.sigma if cuerpo.sigma > 0 else 0
            
            dt_local = dt * cuerpo.tasa_tiempo_local
            
            cuerpo.vel += aceleracion * dt_local
            cuerpo.pos += cuerpo.vel * dt_local
            
            cuerpo.trayectoria.append(cuerpo.pos.copy())


# ==========================================================
# 3. EJECUCIÓN DEL PROBLEMA DE TRES CUERPOS
# ==========================================================

# Parámetros de la simulación
DT = 0.01          # Paso de tiempo discreto (Delta tau)
PASOS = 5000       
TASA_TRANSFERENCIA = 0.01  # <--- NUEVO: Tasa de pérdida/ganancia de Tensión por unidad de tiempo

# 1. Cuerpo Central (Alta Tensión)
c1 = CuerpoDimensional("Sol (D4)", 0, 0, 50.0)

# 2. Primer Cuerpo (Tensión Media)
c2 = CuerpoDimensional("Planeta (D4)", 5, 0, 0.5)
c2.vel = np.array([0.0, 2.5]) 

# 3. Segundo Cuerpo (Baja Tensión, lunas)
c3 = CuerpoDimensional("Luna A (D4)", 5.5, 0, 0.1)
c3.vel = np.array([0.0, 2.5]) 

c4 = CuerpoDimensional("Luna B (D5)", 5.5, 0.5, 0.1)
c4.vel = np.array([0.0, 2.5]) 


cuerpos_simulados = [c1, c2, c3, c4]

# Ejecutar la simulación (Se pasa la nueva tasa de transferencia)
simular_tension_emergente(cuerpos_simulados, PASOS, DT, TASA_TRANSFERENCIA)

# ==========================================================
# 4. VISUALIZACIÓN DE LA EMERGENCIA
# ==========================================================

# Visualización de la trayectoria espacial (X vs Y)
plt.figure(figsize=(18, 6)) # Aumentamos el tamaño para incluir el gráfico de sigma
colores = ['orange', 'blue', 'green', 'red']

# --- GRÁFICO 1: TRAYECTORIA ---
plt.subplot(1, 3, 1) 
for i, cuerpo in enumerate(cuerpos_simulados):
    trayectoria_array = np.array(cuerpo.trayectoria)
    plt.plot(trayectoria_array[:, 0], trayectoria_array[:, 1], 
             label=f'Trayectoria {cuerpo.nombre}', color=colores[i], linewidth=1)
    plt.plot(cuerpo.pos[0], cuerpo.pos[1], 'o', color=colores[i], markersize=5)

plt.title('1. Trayectoria Espacial (D4) - Efecto de la Tensión')
plt.xlabel('Coordenada Espacial X (D4)')
plt.ylabel('Coordenada Espacial Y (D4)')
plt.grid(True)
plt.legend()
plt.axis('equal')

# --- GRÁFICO 2: TASA DE TIEMPO (DILATACIÓN) ---
plt.subplot(1, 3, 2)
tiempo_global = np.arange(0, PASOS * DT, DT) 

for i, cuerpo in enumerate(cuerpos_simulados):
    registro = np.array(cuerpo.registro_tasa_tiempo)[:len(tiempo_global)]
    plt.plot(tiempo_global, registro, label=f'Tasa $\\Delta t$ {cuerpo.nombre}', color=colores[i], linewidth=2)

plt.axhline(y=1.0, color='r', linestyle='--', label='Tasa de Tiempo Plana (1.0)')
plt.title('2. Resta de Coordenadas Temporales (Dilatación)')
plt.xlabel('Tiempo de Evolución ($\Delta\\tau$ Global)')
plt.ylabel('Tasa de Tiempo Local (1.0 = Tiempo normal)')
plt.ylim(0.0, 1.1)
plt.grid(True)
plt.legend()

# --- GRÁFICO 3: CAMBIO DE TENSIÓN ---
plt.subplot(1, 3, 3)
tiempos_eje = np.arange(0, PASOS * DT + DT, DT)
if len(tiempos_eje) > PASOS + 1:
    tiempos_eje = tiempos_eje[:PASOS + 1]

# Extraer el registro de Tensión (Sigma) a lo largo del tiempo
registro_sigma = [[cuerpo.sigma] for cuerpo in cuerpos_simulados]
# Volver a ejecutar la simulación, capturando solo las sigmas
# (Se hace esto de manera simple para no complicar el bucle principal, aunque es menos eficiente)
sigmas_cuerpos = [[] for _ in cuerpos_simulados]
cuerpos_temp = configurar_cuerpos_inicial() # Re-inicializar para el gráfico

for _ in range(PASOS + 1):
    sigma_perdida_sol = TASA_TRANSFERENCIA * DT
    
    # Pérdida y Ganancia
    cuerpos_temp[0].sigma -= sigma_perdida_sol
    sigma_por_luna = sigma_perdida_sol / len(cuerpos_temp[2:])
    for luna in cuerpos_temp[2:]:
        luna.sigma += sigma_por_luna
        
    for i in range(len(cuerpos_temp)):
        sigmas_cuerpos[i].append(cuerpos_temp[i].sigma)


for i, cuerpo in enumerate(cuerpos_simulados):
    if i < len(sigmas_cuerpos) and len(sigmas_cuerpos[i]) > 0:
        plt.plot(tiempos_eje, sigmas_cuerpos[i], label=f'$\sigma$ {cuerpo.nombre}', color=colores[i])

plt.title('3. Evolución de la Tensión ($\sigma$)')
plt.xlabel('Tiempo de Evolución ($\Delta\\tau$ Global)')
plt.ylabel('Tensión ($\sigma$)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
