import sympy
from sympy import symbols

# --- Constantes del Mundo de Einstein (RG) ---
G = symbols('G', real=True, positive=True)      # Constante Gravitacional
c = symbols('c', real=True, positive=True)      # Velocidad de la Luz
M = symbols('M', real=True, positive=True)      # Masa
alpha = symbols('alpha', real=True, positive=True) # Constante de ajuste Potencial

# --- CORRECCIÓN: Permitir que sigma pueda ser negativa para resolver la ecuación. ---
sigma = symbols('sigma', real=True) 

# --- Relación de Equilibrio ---
# alpha * sigma = - (2 * G * M) / c^2
ecuacion_cierre = sympy.Eq(alpha * sigma, - (2 * G * M) / (c**2))

# 1. Resolver la ecuación (¡Ahora funcionará!)
solucion_sigma = sympy.solve(ecuacion_cierre, sigma)[0]

print("--- 3. Ecuación de Cierre: La Traducción de la Tensión a la Masa (CORREGIDA) ---")
print("Se asume que la Tensión (sigma) puede ser negativa.")
print("SOLUCIÓN ANALÍTICA: Tensión (sigma) en función de la Masa (M):")
print(f"sigma = {solucion_sigma}")
print("-" * 60)

# --- Verificación de la Constante de Acoplamiento (kappa) ---
kappa = symbols('kappa', real=True, positive=True)
constante_RG = 8 * sympy.pi * G / (c**4)

# La EFT se alinea si kappa = constante_RG / (-2G / alpha c^2)
kappa_necesario = (constante_RG / (-(2 * G) / (alpha * c**2))).simplify()

print("VERIFICACIÓN: La Constante de Acoplamiento (kappa) requerida:")
print(f"kappa = {kappa_necesario}")
print("-" * 60)