#jose manuel Briceno Mendoza
import cmath

class ConjuntoComplejoEF:
    def __init__(self, inicio, ancho, ruta, nivel):
        self.centro = inicio
        self.ancho = ancho
        self.ruta = ruta
        self.nivel = nivel

def operacion_conjunto_zeta(conjunto, delta_t):
    nuevo_centro = conjunto.centro + complex(0, delta_t)
    distancia_al_eje = abs(nuevo_centro.real - 0.5)
    
    if distancia_al_eje < 0.00001:
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho * 0.5, conjunto.ruta + "R", conjunto.nivel + 1), "R"
    else:
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho, conjunto.ruta + "L", conjunto.nivel + 1), "L"
bloque_inicial = ConjuntoComplejoEF(complex(0.5, 14.13), 8, "N", 0)
niveles = 16
paso_t = 1.0

print(f"Iniciando Operación sobre Conjunto: Re(0.5) con ancho {bloque_inicial.ancho}")

arbol = [bloque_inicial]
for i in range(niveles):
    nuevo_bloque, tipo = operacion_conjunto_zeta(arbol[-1], paso_t)
    arbol.append(nuevo_bloque)
    print(f"Nivel {i}: Ruta {nuevo_bloque.ruta} | Ancho del Conjunto: {nuevo_bloque.ancho:.16f} | {'CONVERGENCIA' if tipo == 'R' else 'EXCLUSIÓN'}")
