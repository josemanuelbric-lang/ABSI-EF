#jose manuel Briceno Mendoza
import cmath

class ConjuntoComplejoEF:
    def __init__(self, inicio, ancho, ruta, nivel):
        self.centro = inicio
        self.ancho = ancho
        self.ruta = ruta
        self.nivel = nivel

def operacion_conjunto_zeta(conjunto, delta_t, forzar_error=False):
    # Si forzamos el error, movemos el centro a 0.6 (fuera del 0.5)
    if forzar_error:
        nuevo_centro = complex(0.6, conjunto.centro.imag + delta_t)
    else:
        nuevo_centro = conjunto.centro + complex(0, delta_t)
    
    distancia_al_eje = abs(nuevo_centro.real - 0.5)
    
    # CRITERIO ABSI: Solo si estás en el eje, el ancho se reduce (Contracción)
    if distancia_al_eje < 0.00001:
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho * 0.5, conjunto.ruta + "R", conjunto.nivel + 1), "R"
    else:
        # Si hay error, el ancho se estanca (ya no hay contracción beneficiosa)
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho, conjunto.ruta + "L", conjunto.nivel + 1), "L"

bloque_inicial = ConjuntoComplejoEF(complex(0.5, 14.13), 8, "N", 0)
niveles = 16
paso_t = 1.0

arbol = [bloque_inicial]
print(f"Iniciando Simulación con Error Provocado en Nivel 7...")

for i in range(niveles):
    # Introducimos el error a propósito en la iteración 7
    error_activo = (i == 7)
    
    nuevo_bloque, tipo = operacion_conjunto_zeta(arbol[-1], paso_t, forzar_error=error_activo)
    arbol.append(nuevo_bloque)
    
    # Marcamos visualmente dónde ocurrió el error
    marca_error = " <--- !!! ERROR INTRODUCIDO" if i == 7 else ""
    print(f"Nivel {i:2}: Ruta {nuevo_bloque.ruta:18} | Ancho: {nuevo_bloque.ancho:.10f} | {tipo:12} {marca_error}")
