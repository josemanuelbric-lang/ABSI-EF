import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. Definición de Atomodimensionales (Estructuras de Cuerpos)
# ==========================================================

class CuerpoDimensional:
    def __init__(self, nombre, x, y, tension_sigma):
        self.nombre = nombre
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0], dtype=float)  
        self.sigma = tension_sigma  
        self.trayectoria = [self.pos.copy()]
        self.tasa_tiempo_local = 1.0  
        self.registro_tasa_tiempo = [1.0]
        self.registro_sigma = [tension_sigma] # Registro para el gráfico de sigma
        self.activo = True 

    def calcular_fuerza_tension(self, otro_cuerpo):
        """Calcula la fuerza de reorganización de la Tensión (análogo a la gravedad)."""
        if not otro_cuerpo.activo: 
            return np.array([0.0, 0.0])

        r_vec = otro_cuerpo.pos - self.pos
        r = np.linalg.norm(r_vec)
        r = max(r, 0.5) 

        fuerza_mag = (self.sigma * otro_cuerpo.sigma) / (r**2)
        direccion_unit = r_vec / r
        
        return direccion_unit * fuerza_mag

    def calcular_potencial_tension(self, otro_cuerpo):
        """Calcula el Potencial de Tensión (análogo al potencial gravitatorio Phi)."""
        if not otro_cuerpo.activo: 
            return 0.0
            
        r = np.linalg.norm(otro_cuerpo.pos - self.pos)
        r = max(r, 0.5)
        return -otro_cuerpo.sigma / r
        
# ==========================================================
# 2. SIMULACIÓN DE EVOLUCIÓN DISCRETA (D4)
# ==========================================================

def simular_tension_emergente(cuerpos, pasos_totales, dt, tasa_transferencia=0.0):
    """Evoluciona el sistema de cuerpos a través del tiempo discreto (Delta tau)."""
    
    C_AJUSTE_POTENCIAL = 0.005  
    RADIO_SCHWARZSCHILD = 1.5 # Definición interna para la lógica de absorción

    # Identificar los cuerpos al inicio
    agujero_negro = next((c for c in cuerpos if "Agujero Negro" in c.nombre), None)
    sol = next((c for c in cuerpos if "Sol" in c.nombre), None)
    lunas = [c for c in cuerpos if "Luna" in c.nombre]
    
    for _ in range(pasos_totales):
        
        # 2.0. APLICAR TRANSFERENCIA DE TENSIÓN (Masa)
        if tasa_transferencia > 0.0 and sol is not None:
            sigma_perdida_sol = tasa_transferencia * dt  
            sol.sigma -= sigma_perdida_sol
            if sol.sigma < 0.0: sol.sigma = 0.0  
            
            lunas_activas = [l for l in lunas if l.activo]
            if lunas_activas: 
                sigma_por_luna = sigma_perdida_sol / len(lunas_activas)
                for luna in lunas_activas:
                    luna.sigma += sigma_por_luna

        # 2.1. CÁLCULO DE INTERACCIÓN (Tensión y Potencial)
        fuerzas_totales = [np.array([0.0, 0.0]) for _ in cuerpos]
        potenciales_totales = [0.0 for _ in cuerpos]
        
        for i, c1 in enumerate(cuerpos):
            if not c1.activo: continue 
            for j, c2 in enumerate(cuerpos):
                if i != j and c2.activo: 
                    fuerzas_totales[i] += c1.calcular_fuerza_tension(c2)
                    potenciales_totales[i] += c1.calcular_potencial_tension(c2)
        
        # 2.2. APLICACIÓN DE LA TENSIÓN (Movimiento y Dilatación)
        for i, cuerpo in enumerate(cuerpos):
            
            # 1. Registro de Sigma (antes de la posible absorción)
            cuerpo.registro_sigma.append(cuerpo.sigma)
            
            if not cuerpo.activo:  
                cuerpo.trayectoria.append(cuerpo.pos.copy()) 
                cuerpo.registro_tasa_tiempo.append(0.0) 
                continue 

            # 2. Detección de Absorción por Agujero Negro
            if agujero_negro and cuerpo != agujero_negro:
                dist_a_agujero = np.linalg.norm(agujero_negro.pos - cuerpo.pos)
                if dist_a_agujero < RADIO_SCHWARZSCHILD:
                    print(f"¡{cuerpo.nombre} ha sido absorbido por el Agujero Negro!")
                    agujero_negro.sigma += cuerpo.sigma 
                    agujero_negro.registro_sigma[-1] = agujero_negro.sigma # Actualizar sigma del AN
                    cuerpo.sigma = 0.0 
                    cuerpo.activo = False 
                    cuerpo.vel = np.array([0.0, 0.0]) 
                    cuerpo.tasa_tiempo_local = 0.0 
                    cuerpo.trayectoria.append(cuerpo.pos.copy()) 
                    cuerpo.registro_tasa_tiempo.append(0.0)
                    continue 

            # 3. CÁLCULO DE LA "RESTA TEMPORAL" (Dilatación)
            potencial_normalizado = -potenciales_totales[i] * C_AJUSTE_POTENCIAL
            
            if potencial_normalizado < 1.0:
                cuerpo.tasa_tiempo_local = np.sqrt(1.0 - potencial_normalizado)
            else:
                cuerpo.tasa_tiempo_local = 0.0  
                
            cuerpo.registro_tasa_tiempo.append(cuerpo.tasa_tiempo_local)
            
            # 4. CÁLCULO DEL MOVIMIENTO ESPACIAL
            aceleracion = fuerzas_totales[i] / cuerpo.sigma if cuerpo.sigma > 0 else np.array([0.0, 0.0])
            
            dt_local = dt * cuerpo.tasa_tiempo_local
            
            cuerpo.vel += aceleracion * dt_local
            cuerpo.pos += cuerpo.vel * dt_local
            
            cuerpo.trayectoria.append(cuerpo.pos.copy())

# ==========================================================
# 3. CONFIGURACIÓN Y EJECUCIÓN
# ==========================================================

def configurar_cuerpos():
    c1 = CuerpoDimensional("Sol (D4)", 0, 0, 50.0)
    c2 = CuerpoDimensional("Planeta (D4)", 5, 0, 0.5)
    c2.vel = np.array([0.0, 2.0]) 
    c3 = CuerpoDimensional("Luna A (D4)", 5.5, 0, 0.1)
    c3.vel = np.array([0.0, 2.5]) 
    c4 = CuerpoDimensional("Luna A (D4)", 5.5, 0, 0.1)
    c4.vel = np.array([0.0, 2.1]) 
    # Agujero Negro: alta tensión, lejos de la órbita inicial
    #c4 = CuerpoDimensional("Agujero Negro (D4)", 10, 10, 10.0) 
    return [c1, c2, c3, c4]

# Parámetros de la simulación
DT = 0.01          
PASOS = 10000   
TASA_TRANSFERENCIA = 0.1
RADIO_SCHWARZSCHILD = 1.5 # Definición global para el gráfico

# Inicialización
cuerpos_simulados = configurar_cuerpos()
agujero_negro = next((c for c in cuerpos_simulados if "Agujero Negro" in c.nombre), None)

# Ejecutar la simulación
simular_tension_emergente(cuerpos_simulados, PASOS, DT, TASA_TRANSFERENCIA)

# ==========================================================
# 4. VISUALIZACIÓN DE LA EMERGENCIA
# ==========================================================

# Visualización de la trayectoria espacial (X vs Y)
plt.figure(figsize=(18, 6)) 
colores = ['orange', 'blue', 'green', 'black'] 

# --- GRÁFICO 1: TRAYECTORIA ---
plt.subplot(1, 3, 1) 
for i, cuerpo in enumerate(cuerpos_simulados):
    trayectoria_array = np.array(cuerpo.trayectoria)
    
    # Dibujar la trayectoria
    plt.plot(trayectoria_array[:, 0], trayectoria_array[:, 1], 
             label=f'Trayectoria {cuerpo.nombre}', color=colores[i], linewidth=1)
    
    # Dibujar la posición final
    if cuerpo.activo: 
        plt.plot(cuerpo.pos[0], cuerpo.pos[1], 'o', color=colores[i], markersize=5)
    else: 
        # Punto final para cuerpos absorbidos
        plt.plot(trayectoria_array[-1, 0], trayectoria_array[-1, 1], 'x', color='red', markersize=8, label=f'Absorbido {cuerpo.nombre}')

# Dibujar el Radio de Schwarzschild (Horizonte de Sucesos)
if agujero_negro:
    circulo_schwarzschild = plt.Circle(agujero_negro.pos, RADIO_SCHWARZSCHILD, color='gray', alpha=0.3, fill=True, linestyle='--', label='Horizonte de Sucesos')
    plt.gca().add_patch(circulo_schwarzschild)


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

for i, cuerpo in enumerate(cuerpos_simulados):
    registro_sigma_array = np.array(cuerpo.registro_sigma)
    # Ajustar el eje de tiempo para que coincida con la longitud del registro de sigma
    tiempos_eje = np.arange(0, len(registro_sigma_array) * DT, DT)
    
    plt.plot(tiempos_eje, registro_sigma_array, label=f'$\sigma$ {cuerpo.nombre}', color=colores[i])

plt.title('3. Evolución de la Tensión ($\sigma$)')
plt.xlabel('Tiempo de Evolución ($\Delta\\tau$ Global)')
plt.ylabel('Tensión ($\sigma$)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()