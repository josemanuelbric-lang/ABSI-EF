import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. Definición de Atomodimensionales (Estructuras de Cuerpos)
# ==========================================================

class CuerpoDimensional:
    def __init__(self, nombre, x, y, tension_sigma):
        self.nombre = nombre
        # Posición inicial en el D4 (simplificada a 2D espacial)
        self.pos = np.array([x, y], dtype=float)
        # Momento inicial (velocidad)
        self.vel = np.array([0.0, 0.0], dtype=float) 
        # Tensión de Organización (Análogo a la masa/energía)
        self.sigma = tension_sigma 
        self.trayectoria = [self.pos.copy()]
        
    def calcular_fuerza_tension(self, otro_cuerpo):
        """Calcula la fuerza de reorganización de la Tensión (análogo a la gravedad)."""
        r_vec = otro_cuerpo.pos - self.pos
        r = np.linalg.norm(r_vec)
        
        if r < 1.0: return np.array([0.0, 0.0]) # Evitar división por cero o singularidad

        # FÓRMULA DE INTERACCIÓN DE TENSIÓN
        # Asumimos que la fuerza (el impulso de reorganización) es proporcional al
        # producto de las tensiones e inversamente proporcional al cuadrado de la distancia.
        # Esto simula la tensión local que jala a los Atomidimensionales.
        
        # Factor de Tensión (análogo a G*M1*M2)
        fuerza_mag = (self.sigma * otro_cuerpo.sigma) / (r**2)
        
        # Vector unitario de dirección
        direccion_unit = r_vec / r
        
        # La fuerza es la manifestación del sistema buscando la Mínima Tensión
        return direccion_unit * fuerza_mag

# ==========================================================
# 2. SIMULACIÓN DE EVOLUCIÓN DISCRETA (D4)
# ==========================================================

def simular_tension_emergente(cuerpos, pasos_totales, dt):
    """Evoluciona el sistema de cuerpos a través del tiempo discreto (Delta tau)."""
    
    for _ in range(pasos_totales):
        fuerzas_totales = [np.array([0.0, 0.0]) for _ in cuerpos]
        
        # 2.1. Cálculo de Tensión (Interacción entre los 3 cuerpos)
        for i, c1 in enumerate(cuerpos):
            for j, c2 in enumerate(cuerpos):
                if i != j:
                    # c1 experimenta una fuerza de reorganización debido a c2
                    fuerzas_totales[i] += c1.calcular_fuerza_tension(c2)
        
        # 2.2. Aplicación de la Tensión (Ecuación de Evolución Discreta)
        for i, cuerpo in enumerate(cuerpos):
            # Aceleración = Fuerza (Tensión de Reorganización) / Masa Emergente (Sigma)
            # F = m*a  =>  a = F/m
            aceleracion = fuerzas_totales[i] / cuerpo.sigma
            
            # El Momento (velocidad) se actualiza por la aceleración en el tiempo discreto
            cuerpo.vel += aceleracion * dt
            
            # La Posición (estructura de Atomidimensionales) se reorganiza
            cuerpo.pos += cuerpo.vel * dt
            
            # 2.3. Registro de Trayectoria
            cuerpo.trayectoria.append(cuerpo.pos.copy())


# ==========================================================
# 3. EJECUCIÓN DEL PROBLEMA DE TRES CUERPOS
# ==========================================================

# Parámetros de la simulación
DT = 0.01          # Paso de tiempo discreto (Delta tau)
PASOS = 2000       # Número de pasos de evolución

# 1. Cuerpo Central (Alta Tensión)
c1 = CuerpoDimensional("Sol (D4)", 0, 0, 100.0)

# 2. Primer Cuerpo (Tensión Media)
c2 = CuerpoDimensional("Planeta (D4)", 5, 0, 0.5)
c2.vel = np.array([0.0, 2.5]) # Damos una velocidad inicial para que orbite

# 3. Segundo Cuerpo (Baja Tensión, más inestable)
c3 = CuerpoDimensional("Luna (D4)", 6.5, 0, 0.1)
c3.vel = np.array([0.0, 2.0])


# Ejecutar la simulación
simular_tension_emergente([c1, c2, c3], PASOS, DT)

# ==========================================================
# 4. VISUALIZACIÓN DE LA EMERGENCIA
# ==========================================================

plt.figure(figsize=(8, 8))
colores = ['orange', 'blue', 'green']
cuerpos_lista = [c1, c2, c3]

for i, cuerpo in enumerate(cuerpos_lista):
    # Convertir la lista de posiciones a un array para Matplotlib
    trayectoria_array = np.array(cuerpo.trayectoria)
    
    # Graficar la trayectoria
    plt.plot(trayectoria_array[:, 0], trayectoria_array[:, 1], 
             label=f'Trayectoria {cuerpo.nombre}', color=colores[i], linewidth=1)
    
    # Graficar la posición final
    plt.plot(cuerpo.pos[0], cuerpo.pos[1], 'o', color=colores[i], markersize=5)

plt.title('Simulación de Interacción por Tensión de Organización (Modelo D4)')
plt.xlabel('Coordenada Espacial X (D4)')
plt.ylabel('Coordenada Espacial Y (D4)')
plt.grid(True)
plt.legend()
plt.axis('equal') # Para que las órbitas no se distorsionen
plt.show()