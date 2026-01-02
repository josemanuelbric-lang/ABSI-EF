section .text
global add_big_asm

add_big_asm:
    ; RDI = Res->d, RSI = A->d, RDX = WORDS
    test rdx, rdx
    jz .done
    clc                 ; Limpiar Carry inicialmente

.loop_4x:
    cmp rdx, 4          ; ¿Quedan al menos 4 palabras?
    jl .remainder

    ; Procesar 4 palabras de 64 bits de un tirón
    mov r8, [rsi]
    adc [rdi], r8
    mov r8, [rsi + 8]
    adc [rdi + 8], r8
    mov r8, [rsi + 16]
    adc [rdi + 16], r8
    mov r8, [rsi + 24]
    adc [rdi + 24], r8

    add rsi, 32         ; Avanzar punteros 32 bytes (4 * 8)
    add rdi, 32
    sub rdx, 4
    jnz .loop_4x
    jmp .done

.remainder:
    test rdx, rdx
    jz .done
.loop_1x:
    mov r8, [rsi]
    adc [rdi], r8
    add rsi, 8
    add rdi, 8
    dec rdx
    jnz .loop_1x

.done:
    ret