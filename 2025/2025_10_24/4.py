import numpy as np
import matplotlib.pyplot as plt

class CuerpoDimensional:
    def __init__(self, nombre, x, y, tension_sigma):
        self.nombre = nombre
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0], dtype=float) 
        self.sigma = tension_sigma 
        self.trayectoria = [self.pos.copy()]
        self.tasa_tiempo_local = 1.0 
        self.registro_tasa_tiempo = [1.0]
        
    def calcular_fuerza_tension(self, otro_cuerpo):
        """Calcula la fuerza de reorganización de la Tensión (análogo a la gravedad)."""
        r_vec = otro_cuerpo.pos - self.pos
        r = np.linalg.norm(r_vec)
        
        r = max(r, 0.5)
        fuerza_mag = (self.sigma * otro_cuerpo.sigma) / (r**2)
        direccion_unit = r_vec / r
        
        return direccion_unit * fuerza_mag

    def calcular_potencial_tension(self, otro_cuerpo):
        """Calcula el Potencial de Tensión (análogo al potencial gravitatorio Phi).
           U = -G*M/r. Usaremos U ~ -sigma / r"""
        r = np.linalg.norm(otro_cuerpo.pos - self.pos)
        r = max(r, 0.5)
        return -otro_cuerpo.sigma / r

def simular_tension_emergente(cuerpos, pasos_totales, dt):
    """Evoluciona el sistema de cuerpos a través del tiempo discreto (Delta tau)."""
    
    C_AJUSTE_POTENCIAL = 0.005 
    
    for _ in range(pasos_totales):
        fuerzas_totales = [np.array([0.0, 0.0]) for _ in cuerpos]
        potenciales_totales = [0.0 for _ in cuerpos]
        
        for i, c1 in enumerate(cuerpos):
            for j, c2 in enumerate(cuerpos):
                if i != j:
                    fuerzas_totales[i] += c1.calcular_fuerza_tension(c2)
                    potenciales_totales[i] += c1.calcular_potencial_tension(c2)
        
        for i, cuerpo in enumerate(cuerpos):
            
            
            potencial_normalizado = -potenciales_totales[i] * C_AJUSTE_POTENCIAL
            
            if potencial_normalizado < 1.0:
                 cuerpo.tasa_tiempo_local = np.sqrt(1.0 - potencial_normalizado)
            else:
                 cuerpo.tasa_tiempo_local = 0.0
            cuerpo.registro_tasa_tiempo.append(cuerpo.tasa_tiempo_local)
            
            aceleracion = fuerzas_totales[i] / cuerpo.sigma
            
            dt_local = dt * cuerpo.tasa_tiempo_local
            
            cuerpo.vel += aceleracion * dt_local
            cuerpo.pos += cuerpo.vel * dt_local
            
            cuerpo.trayectoria.append(cuerpo.pos.copy())

DT = 0.001 
PASOS = 5000

c1 = CuerpoDimensional("Sol (D4)", 0, 0, 50.0)

c2 = CuerpoDimensional("Planeta (D4)", 4, 0, 0.5)
c2.vel = np.array([0.0, 1.5]) 

c3 = CuerpoDimensional("Luna (D4)", 5.5, 0, 0.01)
c3.vel = np.array([0.0, 1.0]) 

cuerpos_simulados = [c1, c2, c3]

simular_tension_emergente(cuerpos_simulados, PASOS, DT)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
colores = ['orange', 'blue', 'green', 'red']

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

plt.subplot(1, 2, 2)
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

plt.tight_layout()
plt.show()