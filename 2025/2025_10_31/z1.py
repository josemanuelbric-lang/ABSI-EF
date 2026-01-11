import numpy as np

# --- 1. Parámetros Estructurales de la TDH ---
D = 4.0
N = 3.8710

# --- 2. Ley Estructural: Cálculo de la Probabilidad de Error (Epsilon) ---
# Epsilon (epsilon) es la probabilidad de que un paso de cómputo falle debido a la Tensión.
epsilon = (D - N) / D
PROB_EXITO_POR_PASO = 1 - epsilon

print("--- Simulación del Algoritmo de la MTU Tensionada (MTU_T) ---")
print(f"Probabilidad de Error Estructural (epsilon): {epsilon:.5f}")
print(f"Probabilidad de Éxito por Paso (1 - epsilon): {PROB_EXITO_POR_PASO:.5f}")
print("-" * 60)


def simular_mtu_t(n_input, complejidad_tipo, nombre_algoritmo):
    """
    Simula la probabilidad de éxito de un algoritmo dado su complejidad
    y el error estructural (epsilon) de la MTU_T.
    
    Argumentos:
    n_input (int): El tamaño del input del problema (n).
    complejidad_tipo (str): 'P' (Polinomial, n^2) o 'NP' (Exponencial, 2^n).
    nombre_algoritmo (str): Nombre descriptivo para el resultado.
    """
    
    if complejidad_tipo == 'P':
        # Simulación de un algoritmo P (e.g., Ordenamiento)
        # Número de Pasos = n^2
        pasos = n_input**2
    elif complejidad_tipo == 'NP':
        # Simulación de un algoritmo NP-Completo (e.g., Problema del Vendedor Viajero)
        # Número de Pasos = 2^n (Representa la búsqueda de la solución)
        pasos = 2**n_input
    else:
        raise ValueError("El tipo de complejidad debe ser 'P' o 'NP'.")
        
    # Probabilidad de Éxito del Algoritmo Completo:
    # P(Total) = (1 - epsilon) ^ Pasos
    probabilidad_exito_total = PROB_EXITO_POR_PASO ** pasos
    
    print(f"[{nombre_algoritmo} | Tipo: {complejidad_tipo}]")
    print(f"   Tamaño del Input (n): {n_input}")
    print(f"   Pasos de Cómputo Requeridos: {pasos:,.0f}")
    print(f"   Probabilidad de Éxito Total: {probabilidad_exito_total:.6f}")
    
    return probabilidad_exito_total

# --- 3. Implementación de la Prueba ---

N_SIZE = 15 # Tamaño del input para la prueba

# Caso 1: Algoritmo de Clase P (Tiempo Polinomial)
simular_mtu_t(
    n_input=N_SIZE,
    complejidad_tipo='P',
    nombre_algoritmo='Cómputo Polinomial P (n^2)'
)

print("-" * 60)

# Caso 2: Algoritmo de Clase NP (Tiempo Exponencial)
simular_mtu_t(
    n_input=N_SIZE,
    complejidad_tipo='NP',
    nombre_algoritmo='Búsqueda NP (2^n)'
)

# --- 4. Conclusión del Algoritmo ---
# La Probabilidad de Falla de la MTU_T es (1 - Probabilidad de Éxito Total).