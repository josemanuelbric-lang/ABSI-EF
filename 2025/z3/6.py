#jose manuel Briceno Mendoza
import cmath

class ConjuntoComplejoEF:
    def __init__(self, inicio, ancho, ruta, nivel):
        self.centro = inicio
        self.ancho = ancho
        self.ruta = ruta
        self.nivel = nivel

def operacion_conjunto_zeta_explosiva(conjunto, delta_t, forzar_error=False):
    # Forzamos la desviación lateral si se activa el error
    if forzar_error:
        nuevo_centro = complex(0.6, conjunto.centro.imag + delta_t)
    else:
        nuevo_centro = conjunto.centro + complex(0, delta_t)
    
    distancia_al_eje = abs(nuevo_centro.real - 0.5)
    
    # LÓGICA ABSI-EF EXTREMA:
    if distancia_al_eje < 0.00001:
        # CONVERGENCIA: El espacio se comprime (Éxito)
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho * 0.5, conjunto.ruta + "R", conjunto.nivel + 1), "CONVERGENCIA"
    else:
        # EXPLOSIÓN: El espacio se expande (Caos/Exclusión)
        # Multiplicamos por 2 en lugar de dividir
        return ConjuntoComplejoEF(nuevo_centro, conjunto.ancho * 2.0, conjunto.ruta + "L", conjunto.nivel + 1), "EXPLOSIÓN"

# --- Ejecución ---
bloque_inicial = ConjuntoComplejoEF(complex(0.5, 14.13), 8, "N", 0)
niveles = 15

arbol = [bloque_inicial]
print(f"DEMOSTRACIÓN DE EXCLUSIÓN EXPLOSIVA")
print(f"Centro inicial: {bloque_inicial.centro} | Ancho: {bloque_inicial.ancho}\n")

for i in range(niveles):
    # Error en el nivel 7: el sistema "detecta" algo fuera del eje
    error_activo = (i >= 7) 
    
    nuevo_bloque, tipo = operacion_conjunto_zeta_explosiva(arbol[-1], 1.0, forzar_error=error_activo)
    arbol.append(nuevo_bloque)
    
    aviso = "!!! DESVIACIÓN DETECTADA" if i == 7 else ""
    print(f"Nivel {i:2}: {tipo:12} | Ruta: {nuevo_bloque.ruta:16} | Ancho: {nuevo_bloque.ancho:12.6f} {aviso}")
