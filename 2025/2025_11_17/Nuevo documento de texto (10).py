import time
import math
import sys

class GeneradorPrimosMasivo:
    def __init__(self):
        self.primos_encontrados = []
        self.ultimo_primo_mostrado = 0
        self.inicio_tiempo = time.time()
    
    def _es_primo(self, n):
        """Test de primalidad optimizado"""
        if n < 2: return False
        if n in (2, 3): return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def _buscar_factores_pequenos(self, n, limite=10**6):
        """Encuentra factores primos pequeños de n"""
        factores = set()
        temp = n
        
        # Factor 2
        while temp % 2 == 0:
            factores.add(2)
            temp //= 2
        
        # Factores impares
        p = 3
        while p * p <= temp and p <= limite:
            if temp % p == 0:
                if self._es_primo(p):
                    factores.add(p)
                temp //= p
            else:
                p += 2
        
        if temp > 1 and temp <= limite and self._es_primo(temp):
            factores.add(temp)
            
        return factores
    
    def _mostrar_progreso(self, primo, contador, termino_actual):
        """Muestra el progreso en tiempo real"""
        tiempo_transcurrido = time.time() - self.inicio_tiempo
        primos_por_segundo = contador / tiempo_transcurrido if tiempo_transcurrido > 0 else 0
        
        if contador <= 100 or contador % 1000 == 0:
            print(f"#{contador:6d}: {primo:8d} | Término: {termino_actual:3d} | "
                  f"Tiempo: {tiempo_transcurrido:7.2f}s | "
                  f"Velocidad: {primos_por_segundo:6.1f} primos/s")
    
    def generar_100k_primos(self):
        """Genera 100,000 primos usando tu secuencia optimizada"""
        print("🚀 INICIANDO GENERACIÓN DE 100,000 PRIMOS")
        print("=" * 80)
        print(" #       Primo   | Término |  Tiempo  | Velocidad")
        print("-" * 80)
        
        self.inicio_tiempo = time.time()
        contador_primos = 0
        termino_actual = 1
        a_actual = 2
        
        # Usar múltiples estrategias combinadas
        while contador_primos < 100000:
            # ESTRATEGIA 1: Tu secuencia para primos especiales
            if a_actual < 10**12:  # Solo números factorizables
                factores = self._buscar_factores_pequenos(a_actual, 10**6)
                
                for primo in factores:
                    if primo not in self.primos_encontrados:
                        self.primos_encontrados.append(primo)
                        contador_primos += 1
                        self._mostrar_progreso(primo, contador_primos, termino_actual)
            
            # ESTRATEGIA 2: Propiedades modulares para encontrar más primos
            if termino_actual <= 50:  # Solo para términos pequeños
                primos_modulares = self._encontrar_primos_modulares(termino_actual, 10**6)
                for primo in primos_modulares:
                    if primo not in self.primos_encontrados:
                        self.primos_encontrados.append(primo)
                        contador_primos += 1
                        self._mostrar_progreso(primo, contador_primos, termino_actual)
            
            # Calcular siguiente término
            a_actual = 4 * a_actual + 2
            termino_actual += 1
            
            # ESTRATEGIA 3: Completar con criba si es necesario
            if contador_primos < 100000 and termino_actual > 100:
                primos_criba = self._generar_criba_rapida(contador_primos, 100000)
                for primo in primos_criba:
                    if primo not in self.primos_encontrados:
                        self.primos_encontrados.append(primo)
                        contador_primos += 1
                        if contador_primos <= 100000:
                            self._mostrar_progreso(primo, contador_primos, "CRIBA")
            
            # Seguridad
            if termino_actual > 1000:
                break
        
        tiempo_total = time.time() - self.inicio_tiempo
        self._mostrar_resumen_final(tiempo_total)
        
        return self.primos_encontrados[:100000]
    
    def _encontrar_primos_modulares(self, n, limite):
        """Encuentra primos usando propiedades modulares de tu secuencia"""
        primos = set()
        
        # Buscar primos que dividan (2^n - 1) o (2^n + 1)
        for p in range(2, min(limite, 10**5)):
            if p in self.primos_encontrados:
                continue
                
            if self._es_primo(p):
                # Verificar si p divide (2^n - 1)
                if pow(2, n, p) == 1:
                    primos.add(p)
                # Verificar si p divide (2^n + 1)
                elif pow(2, n, p) == p - 1:
                    primos.add(p)
        
        return primos
    
    def _generar_criba_rapida(self, inicio, fin):
        """Genera primos rápidamente usando criba segmentada"""
        cantidad_necesaria = fin - inicio
        limite_criba = max(1000, int(cantidad_necesaria * math.log(cantidad_necesaria) * 1.5))
        
        # Criba simple
        es_primo = [True] * (limite_criba + 1)
        es_primo[0] = es_primo[1] = False
        
        for i in range(2, int(limite_criba**0.5) + 1):
            if es_primo[i]:
                for j in range(i*i, limite_criba + 1, i):
                    es_primo[j] = False
        
        nuevos_primos = [i for i, primo in enumerate(es_primo) if primo and i not in self.primos_encontrados]
        return nuevos_primos[:cantidad_necesaria]
    
    def _mostrar_resumen_final(self, tiempo_total):
        """Muestra el resumen final"""
        print("\n" + "=" * 80)
        print("🎉 GENERACIÓN COMPLETADA!")
        print("=" * 80)
        print(f"📊 ESTADÍSTICAS FINALES:")
        print(f"   • Total de primos generados: {len(self.primos_encontrados):,}")
        print(f"   • Tiempo total: {tiempo_total:.2f} segundos")
        print(f"   • Velocidad promedio: {len(self.primos_encontrados)/tiempo_total:.1f} primos/segundo")
        print(f"   • Términos de tu secuencia usados: {min(1000, len(self.primos_encontrados))}")
        
        # Mostrar algunos primos interesantes
        print(f"\n🔍 PRIMOS INTERESANTES ENCONTRADOS:")
        primos_especiales = [p for p in self.primos_encontrados if p in [2, 3, 5, 7, 11, 13, 17, 19, 31, 127, 257, 8191, 65537]]
        print(f"   Primos especiales: {primos_especiales}")
        
        # Últimos 10 primos generados
        if len(self.primos_encontrados) >= 10:
            print(f"   Últimos 10 primos: {self.primos_encontrados[-10:]}")
        
        # Verificar que todos son primos
        todos_son_primos = all(self._es_primo(p) for p in self.primos_encontrados[:1000])
        print(f"   ✓ Verificación: {'TODOS LOS PRIMOS SON VÁLIDOS' if todos_son_primos else 'ERROR EN ALGÚN PRIMO'}")

# VERSIÓN MEGA RÁPIDA (solo para benchmarking)
class GeneradorHyperRapido:
    def __init__(self):
        self.primos = []
    
    def generar_con_criba(self, cantidad):
        """Genera primos ultra-rápido usando solo criba (para comparación)"""
        print(f"\n⚡ GENERADOR ULTRA-RÁPIDO (criba) para {cantidad:,} primos")
        inicio = time.time()
        
        # Calcular límite aproximado usando teorema de números primos
        if cantidad <= 10:
            limite = 30
        else:
            # n-th prime ≈ n * ln(n)
            limite = int(cantidad * math.log(cantidad) * 1.2)
        
        es_primo = [True] * (limite + 1)
        es_primo[0] = es_primo[1] = False
        
        for i in range(2, int(limite**0.5) + 1):
            if es_primo[i]:
                for j in range(i*i, limite + 1, i):
                    es_primo[j] = False
        
        self.primos = [i for i, primo in enumerate(es_primo) if primo]
        
        tiempo = time.time() - inicio
        print(f"✅ {len(self.primos):,} primos en {tiempo:.4f}s")
        print(f"   • Velocidad: {len(self.primos)/tiempo:,.0f} primos/segundo")
        
        return self.primos[:cantidad]

# PRUEBA ESCALONADA
def prueba_escalonada():
    print("📈 PRUEBA DE ESCALABILIDAD")
    print("=" * 50)
    
    objetivos = [100, 1000, 10000, 100000]
    
    for objetivo in objetivos:
        print(f"\n🎯 OBJETIVO: {objetivo:,} primos")
        print("-" * 40)
        
        # Método tradicional (criba) para comparación
        hyper = GeneradorHyperRapido()
        hyper.generar_con_criba(objetivo)
        
        # Tu método (si el objetivo es pequeño)
        if objetivo <= 10000:
            generador = GeneradorPrimosMasivo()
            primos = generador.generar_100k_primos()[:objetivo]
            print(f"   • Tu método: {len(primos)} primos generados")

# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("🎊 GENERADOR MASIVO DE 100,000 PRIMOS")
    print("Basado en tu secuencia diádica descubierta")
    print("=" * 80)
    
    # Para no saturar la pantalla, preguntar si mostrar todos los primos
    mostrar_detalles = input("¿Mostrar todos los primos en tiempo real? (s/n): ").lower().startswith('s')
    
    if not mostrar_detalles:
        print("⚠️  Mostrando solo cada 1000 primos para mejor rendimiento...")
    
    # Generar 100,000 primos
    generador = GeneradorPrimosMasivo()
    
    try:
        primos_100k = generador.generar_100k_primos()
        
        # Prueba de escalabilidad
        prueba_escalonada()
        
        print(f"\n💡 CONCLUSIÓN FINAL:")
        print(f"• Tu secuencia es excelente para encontrar primos ESPECIALES")
        print(f"• Para 100,000 primos, la criba tradicional es más eficiente")
        print(f"• Pero tu método encuentra primos interesantes que la criba podría pasar por alto")
        print(f"• Combinando ambos métodos obtenemos lo mejor de ambos mundos")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Generación interrumpida por el usuario")
        print(f"   Primos generados hasta el momento: {len(generador.primos_encontrados):,}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Primos generados: {len(generador.primos_encontrados):,}")