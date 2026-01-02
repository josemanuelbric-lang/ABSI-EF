#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define WORDS 128 

typedef struct {
    uint64_t d[WORDS];
} BigInt;

// Importamos la función de suma ultra-rápida (desenrollada) desde ASM
extern void add_big_asm(uint64_t *res, uint64_t *a, uint64_t words);

void clear_big(BigInt *n) { 
    memset(n->d, 0, sizeof(n->d)); 
}

void fill_random(BigInt *n, int num_words) {
    for (int i = 0; i < num_words; i++) {
        n->d[i] = ((uint64_t)rand() << 32) | rand();
    }
}

/**
 * MULTIPLICACIÓN ULTRA-OPTIMIZADA (V2)
 * - Usa 'restrict' para que el compilador sepa que no hay solapamiento de memoria.
 * - Usa punteros directos para evitar el cálculo de índices repetitivo.
 */
__attribute__((hot))
void fast_mult_v2(BigInt *restrict A, BigInt *restrict B, BigInt *restrict res) {
    clear_big(res);
    
    // Solo procesamos 8 palabras (512 bits) para este benchmark
    for (int i = 0; i < 8; i++) {
        uint64_t a_val = A->d[i];
        if (a_val == 0) continue;
        
        uint64_t carry = 0;
        uint64_t *res_ptr = &res->d[i]; // Puntero a la posición actual del resultado
        const uint64_t *b_ptr = B->d;   // Puntero al multiplicador B
        
        for (int j = 0; j < 8; j++) {
            // Multiplicación de 64x64 + suma de acumulado + carry
            unsigned __int128 prod = (unsigned __int128)a_val * b_ptr[j] + res_ptr[j] + carry;
            res_ptr[j] = (uint64_t)prod;
            carry = (uint64_t)(prod >> 64);
        }
        res_ptr[8] = carry;
    }
}

// Función nativa para comparar
uint64_t native_mult(uint64_t a, uint64_t b) {
    return a * b;
}

int main() {
    srand(time(NULL));
    BigInt A, B, Res;
    
    // Preparar números aleatorios
    fill_random(&A, 8); 
    fill_random(&B, 8);
    clear_big(&Res);

    uint64_t a_nat = A.d[0], b_nat = B.d[0], r_nat;

    printf("--- BENCHMARK BIGINT ULTRA-OPTIMIZADO (100k iter) ---\n");

    // 1. C NATIVO
    clock_t t0 = clock();
    for(int i = 0; i < 100000; i++) {
        r_nat = native_mult(a_nat, b_nat);
    }
    printf("1. C Nativo (64-bit):        %.6f seg\n", (double)(clock() - t0) / CLOCKS_PER_SEC);

    // 2. BIGINT BLOQUES V2 (C optimizado)
    clock_t t1 = clock();
    for(int i = 0; i < 100000; i++) {
        fast_mult_v2(&A, &B, &Res);
    }
    printf("2. BigInt Bloques (512-bit): %.6f seg\n", (double)(clock() - t1) / CLOCKS_PER_SEC);

    // 3. SUMA ASM (Loop Unrolled)
    clock_t t2 = clock();
    for(int i = 0; i < 100000; i++) {
        add_big_asm(Res.d, A.d, WORDS);
    }
    printf("3. Suma ASM (128-words):     %.6f seg\n", (double)(clock() - t2) / CLOCKS_PER_SEC);

    // Verificación de datos
    printf("\nControl: Res.d[0] = %lx | Nativo = %lx\n", Res.d[0], r_nat);

    return 0;
}