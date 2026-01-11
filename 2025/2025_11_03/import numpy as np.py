import numpy as np

# --- 1. Definición del Acoplamiento Binario (α_B) ---

def calcular_entropia_binaria(n):
    """
    Calcula la "Entropía Binaria" (longitud del bit) de un número.
    Esto representa la complejidad o "dimensionalidad informacional".
    """
    if n <= 0:
        return 0
    return n.bit_length()

def acoplamiento_binario_alpha(entropia):
    """
    Define el Acoplamiento Binario (α_B) como el inverso de la complejidad.
    Menos bits (menor complejidad) -> Mayor acoplamiento (más eficiente).
    """
    if entropia == 0:
        return 0.0
    # Usamos el inverso de la entropía para que sea análogo a una fuerza
    # (donde la intensidad es inversamente proporcional a la complejidad)
    return 1.0 / entropia

# --- 2. Análisis de Números (30, 16, 12) ---

numeros_a_analizar = [30, 16, 12]

print("=" * 80)
print("📊 ANÁLISIS DEL ACOPLAMIENTO BINARIO (α_B) EN TDH-TN")
print("=" * 80)

for E_par in numeros_a_analizar:
    k = E_par // 2
    
    # 1. Componentes Binarios (k + k)
    bits_k = calcular_entropia_binaria(k)
    alpha_k = acoplamiento_binario_alpha(bits_k)

    # 2. El Par Completo (E_par)
    bits_E = calcular_entropia_binaria(E_par)
    alpha_E = acoplamiento_binario_alpha(bits_E)
    
    # 3. La Diferencia (Análogo al Déficit Dimensional)
    diferencia_alpha = alpha_E - (alpha_k + alpha_k)

    print(f"\n--- Número Par (E_par): {E_par} ---")
    print(f"   Representación Binaria: {bin(E_par)}")
    
    print("-" * 35)
    print("   Partes (k + k):")
    print(f"     Bits de k ({k}): {bits_k}")
    print(f"     α_B de k: {alpha_k:.4f}")
    
    print("-" * 35)
    print("   Total (E_par):")
    print(f"     Bits de E_par: {bits_E}")
    print(f"     α_B de E_par: {alpha_E:.4f}")
    
    # Análisis de la TDH
    print("\n   [ANÁLISIS TDH-TN]")
    print(f"   Suma de α_B de las Partes (α_k + α_k): {2 * alpha_k:.4f}")
    print(f"   Acoplamiento del Total (α_E): {alpha_E:.4f}")
    print(f"   Diferencia Estructural (α_E - 2α_k): {diferencia_alpha:.4f}")