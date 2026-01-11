import math

def calcular_tension_compleja(N_max):
    """
    Calcula e imprime las columnas requeridas para el modelo de Tensión TDH,
    incluyendo la Tensión Total deseada y la cadena de Aplicación de la Fórmula.
    
    Tensión de Borde (T(n)): (6n - 2)
    """
    
    # Nuevo formato con la columna AplicacionDeLaFormula
    print(f"{'N':<4} | {'T(n) = 6n-2':<15} | {'P_n (Pascales)':<30} | {'AplicacionDeLaFormula':<70} | {'Sigma T_n (Alternada)':<20} | {'Tension Deseada':<15}")
    print("-" * 170)

    # Iterar desde la Dimensión n=1 hasta N_max
    for n in range(1, N_max + 1):
        
        # 1. Generación de la Fila de Pascal (Atomodimensionales A_n(k))
        pascal_row = []
        for k in range(n + 1):
             p_k = math.comb(n, k) 
             pascal_row.append(p_k)
        
        # 2. Aplicación de la Fórmula de Tensión de Borde
        tension_factor = (6 * n) - 2
        
        # 3. Cálculo de la Tensión Total Alternada (Sigma T_n) y la cadena de Aplicación
        sigma_tension_alternada = 0
        formula_str = ""
        
        for k, p_k in enumerate(pascal_row):
            # El Atomodimensional con la Tensión aplicada
            tercero = p_k * tension_factor
            
            # Aplicamos el signo alterno
            signo = "+"
            if k % 2 == 1:
                signo = "-"
                tercero *= -1 # Restar si el índice es impar
            
            # Construcción de la cadena de la fórmula
            # Excluimos el signo '+' inicial
            if k == 0:
                formula_str += f"{tercero}"
            else:
                # Usamos el valor absoluto de tercero para la impresión y luego aplicamos el signo
                formula_str += f" {signo} {abs(tercero)}"
            
            sigma_tension_alternada += tercero
        
        # 4. Cálculo de la Tensión Deseada (El valor que se espera de tu secuencia)
        tension_deseada = tension_factor
        
        # 5. Imprimir Resultados
        
        pascal_str = ' '.join(map(str, pascal_row))
        
        print(f"{n:<4} | {tension_factor:<15} | {pascal_str:<30.30} | {formula_str:<70.70} | {sigma_tension_alternada:<20} | {tension_deseada:<15}")

# Ejecutar el programa. Lo limitamos a N=10 para no saturar la salida.
N_MAXIMO = 10 
print("--- Teoría de la Jerarquía de Tensión Dimensional (TDH) ---")
print(f"Cálculo de Tensión (6N-2) hasta la Dimensión N={N_MAXIMO}")
calcular_tension_compleja(N_MAXIMO)