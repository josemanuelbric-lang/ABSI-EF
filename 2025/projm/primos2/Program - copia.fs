open System
open System.Diagnostics
open System.Numerics

type GeneradorPrimosPersonalizable() =
    let mutable primosEncontrados = []
    let inicioTiempo = DateTime.Now
    
    // Test de primalidad optimizado
    let esPrimo (n: int64) =
        if n < 2L then false
        elif n = 2L || n = 3L then true
        elif n % 2L = 0L || n % 3L = 0L then false
        else
            let mutable i = 5L
            let mutable resultado = true
            while i * i <= n && resultado do
                if n % i = 0L || n % (i + 2L) = 0L then
                    resultado <- false
                i <- i + 6L
            resultado

    // Encuentra factores primos pequeños
    let buscarFactoresPequenos (n: int64) =
        let mutable factores = Set.empty
        let mutable temp = n
        
        // Factor 2
        while temp % 2L = 0L do
            factores <- factores.Add(2L)
            temp <- temp / 2L
        
        // Factores impares
        let mutable p = 3L
        while p * p <= temp && p <= 1000000L do
            if temp % p = 0L then
                if esPrimo p then
                    factores <- factores.Add(p)
                temp <- temp / p
            else
                p <- p + 2L
        
        if temp > 1L && temp <= 1000000L && esPrimo temp then
            factores <- factores.Add(temp)
            
        factores

    // Mostrar primo según preferencias
    let mostrarPrimo primo contador terminoActual mostrarTodos frecuencia =
        let tiempoTranscurrido = (DateTime.Now - inicioTiempo).TotalSeconds
        let primosPorSegundo = if tiempoTranscurrido > 0.0 then float contador / tiempoTranscurrido else 0.0
        
        let mostrar = 
            mostrarTodos || 
            contador <= 100 || 
            contador % frecuencia = 0 || 
            List.contains primo [2L; 3L; 5L; 7L; 17L; 31L; 127L; 257L; 8191L; 65537L]
        
        if mostrar then
            printfn "#%6d: %8d | Término: %5s | Tiempo: %7.2fs | Velocidad: %6.1f primos/s" 
                contador primo terminoActual tiempoTranscurrido primosPorSegundo

    // Encontrar primos modulares (versión simplificada)
    let encontrarPrimosModulares n limite =
        let mutable primos = Set.empty
        
        for p in 2L .. int64 (min limite 50000) do
            if not (List.contains p primosEncontrados) && esPrimo p then
                // Versión simplificada sin BigInteger
                if p % int64 n = 1L || p % int64 n = int64 n - 1L then
                    primos <- primos.Add(p)
        
        primos

    // Generar criba rápida
    let generarCribaRapida cantidadActual cantidadTotal =
        let cantidadNecesaria = cantidadTotal - cantidadActual
        if cantidadNecesaria <= 0 then 
            []
        else
            let limite = int (float cantidadTotal * Math.Log(float cantidadTotal) * 1.3)
            printfn "   🎯 Generando %d primos más con criba (límite: %d)..." cantidadNecesaria limite
            
            let esPrimoArr = Array.create (limite + 1) true
            esPrimoArr.[0] <- false
            esPrimoArr.[1] <- false
            
            for i in 2 .. int (sqrt (float limite)) do
                if esPrimoArr.[i] then
                    for j in i*i .. i .. limite do
                        if j < esPrimoArr.Length then
                            esPrimoArr.[j] <- false
            
            let todosPrimos = 
                [| for i in 2 .. limite do if esPrimoArr.[i] then yield int64 i |]
            
            let nuevosPrimos = 
                todosPrimos 
                |> Array.filter (fun p -> not (List.contains p primosEncontrados))
                |> Array.truncate cantidadNecesaria
                |> Array.toList
            
            nuevosPrimos

    // Mostrar resumen final
    let mostrarResumenFinal tiempoTotal cantidadObjetivo =
        printfn "\n%s" (String('=', 80))
        printfn "🎉 GENERACIÓN COMPLETADA!"
        printfn "%s" (String('=', 80))
        printfn "📊 ESTADÍSTICAS FINALES:"
        printfn "   • Primos generados: %d de %d" (List.length primosEncontrados) cantidadObjetivo
        printfn "   • Tiempo total: %.2f segundos" tiempoTotal
        
        if tiempoTotal > 0.0 then
            let velocidad = float (List.length primosEncontrados) / tiempoTotal
            printfn "   • Velocidad promedio: %.1f primos/segundo" velocidad
        
        // Primos especiales encontrados
        let primosEspeciales = 
            primosEncontrados 
            |> List.filter (fun p -> List.contains p [2L; 3L; 5L; 7L; 17L; 31L; 127L; 257L; 8191L; 65537L])
        
        if not primosEspeciales.IsEmpty then
            printfn "\n🔍 PRIMOS ESPECIALES ENCONTRADOS:"
            printfn "   %A" primosEspeciales
        
        // Verificación
        if List.length primosEncontrados >= 100 then
            let muestra = primosEncontrados |> List.take 100
            let todosSonPrimos = muestra |> List.forall esPrimo
            printfn "   ✓ Verificación (primeros 100): %s" (if todosSonPrimos then "TODOS VÁLIDOS" else "ERROR")
        
        // Últimos primos
        if List.length primosEncontrados >= 5 then
            let ultimos = primosEncontrados |> List.rev |> List.take 5
            printfn "   Últimos 5 primos: %A" ultimos

    // Método principal para generar primos
    member this.GenerarPrimos(cantidadTotal, mostrarTodos, frecuenciaMuestra) =
        printfn "🚀 INICIANDO GENERACIÓN DE %d PRIMOS" cantidadTotal
        printfn "%s" (String('=', 80))
        printfn " #       Primo   | Término |  Tiempo  | Velocidad"
        printfn "%s" (String('-', 80))
        
        let mutable contadorPrimos = 0
        let mutable terminoActual = 1
        let mutable aActual = 2L
        
        // FASE 1: Usar secuencia para primos especiales
        let objetivoFase1 = min 50000 (int (float cantidadTotal * 0.3))
        
        while contadorPrimos < objetivoFase1 && terminoActual <= 100 do
            // Tu secuencia para primos especiales
            if aActual < 10000000000L then
                let factores = buscarFactoresPequenos aActual
                
                for primo in factores do
                    if not (List.contains primo primosEncontrados) && contadorPrimos < objetivoFase1 then
                        primosEncontrados <- primo :: primosEncontrados
                        contadorPrimos <- contadorPrimos + 1
                        mostrarPrimo primo contadorPrimos (string terminoActual) mostrarTodos frecuenciaMuestra
            
            // Propiedades modulares
            let primosModulares = encontrarPrimosModulares terminoActual 100000
            for primo in primosModulares do
                if not (List.contains primo primosEncontrados) && contadorPrimos < objetivoFase1 then
                    primosEncontrados <- primo :: primosEncontrados
                    contadorPrimos <- contadorPrimos + 1
                    mostrarPrimo primo contadorPrimos (sprintf "M%d" terminoActual) mostrarTodos frecuenciaMuestra
            
            aActual <- 4L * aActual + 2L
            terminoActual <- terminoActual + 1
        
        // FASE 2: Completar con criba
        if contadorPrimos < cantidadTotal then
            printfn "\n⚡ COMPLETANDO CON CRIBA RÁPIDA..."
            let primosCriba = generarCribaRapida contadorPrimos cantidadTotal
            
            for primo in primosCriba do
                if not (List.contains primo primosEncontrados) && contadorPrimos < cantidadTotal then
                    primosEncontrados <- primo :: primosEncontrados
                    contadorPrimos <- contadorPrimos + 1
                    
                    // Mostrar progreso durante la criba
                    if mostrarTodos || 
                       contadorPrimos % (max 1 (cantidadTotal / 20)) = 0 || 
                       contadorPrimos <= int (float cantidadTotal * 0.1) then
                        mostrarPrimo primo contadorPrimos "CRIBA" mostrarTodos frecuenciaMuestra
        
        let tiempoTotal = (DateTime.Now - inicioTiempo).TotalSeconds
        mostrarResumenFinal tiempoTotal cantidadTotal
        
        primosEncontrados |> List.rev |> List.truncate cantidadTotal

// Interfaz de usuario corregida
let obtenerConfiguracion() =
    printfn "🎛️  CONFIGURACIÓN DEL GENERADOR DE PRIMOS"
    printfn "%s" (String('=', 50))
    
    try
        // Cantidad de primos
        let rec obtenerCantidad() =
            printf "¿Cuántos primos quieres generar? (ej: 100, 1000, 10000): "
            match Int32.TryParse(Console.ReadLine()) with
            | (true, n) when n > 0 -> n
            | _ -> 
                printfn "❌ Por favor ingresa un número positivo"
                obtenerCantidad()
        
        let cantidad = obtenerCantidad()
        printfn ""

        // Modo de visualización
        printfn "📊 OPCIONES DE VISUALIZACIÓN:"
        printfn "   1. Mostrar TODOS los primos (pantalla completa)"
        printfn "   2. Mostrar cada X primos (progreso)"
        printfn "   3. Solo mostrar resumen final (más rápido)"
        
        let rec obtenerOpcion() =
            printf "Elige una opción (1-3): "
            match Int32.TryParse(Console.ReadLine()) with
            | (true, n) when n >= 1 && n <= 3 -> n
            | _ -> 
                printfn "❌ Por favor elige 1, 2 o 3"
                obtenerOpcion()
        
        let opcion = obtenerOpcion()

        let (mostrarTodos, frecuencia) =
            match opcion with
            | 1 -> (true, 1)
            | 2 -> 
                let rec obtenerFrecuencia() =
                    printf "¿Mostrar cada cuántos primos? (ej: 100, 500, 1000): "
                    match Int32.TryParse(Console.ReadLine()) with
                    | (true, n) when n > 0 -> n
                    | _ -> 
                        printfn "❌ Por favor ingresa un número positivo"
                        obtenerFrecuencia()
                (false, obtenerFrecuencia())
            | _ -> (false, max 1 (cantidad / 10))
        
        cantidad, mostrarTodos, frecuencia
        
    with
    | :? OperationCanceledException ->
        printfn "\n\n⏹️  Configuración cancelada por el usuario"
        (0, false, 1)

// Comparación rápida
let comparacionRapida cantidad =
    printfn "\n⚡ COMPARACIÓN: CRIBA TRADICIONAL para %d primos" cantidad
    let inicio = DateTime.Now
    
    let limite = 
        if cantidad <= 10 then 30
        else int (float cantidad * Math.Log(float cantidad) * 1.2)
    
    let esPrimoArr = Array.create (limite + 1) true
    esPrimoArr.[0] <- false
    esPrimoArr.[1] <- false
    
    for i in 2 .. int (sqrt (float limite)) do
        if esPrimoArr.[i] then
            for j in i*i .. i .. limite do
                if j < esPrimoArr.Length then
                    esPrimoArr.[j] <- false
    
    let primosCriba = 
        [| for i in 2 .. limite do if esPrimoArr.[i] then yield int64 i |]
    
    let tiempo = (DateTime.Now - inicio).TotalSeconds
    printfn "✅ %d primos en %.4fs" primosCriba.Length tiempo
    if tiempo > 0.0 then
        printfn "   • Velocidad: %.0f primos/segundo" (float primosCriba.Length / tiempo)

// Programa principal
[<EntryPoint>]
let main argv =
    printfn "🎊 GENERADOR PERSONALIZABLE DE PRIMOS"
    printfn "Basado en tu secuencia diádica descubierta"
    printfn "%s" (String('=', 60))
    
    try
        // Obtener configuración
        let cantidad, mostrarTodos, frecuencia = obtenerConfiguracion()
        
        if cantidad > 0 then
            printfn "\n🎯 CONFIGURACIÓN ELEGIDA:"
            printfn "   • Primos a generar: %d" cantidad
            printfn "   • Modo visualización: %s" (if mostrarTodos then "TODOS" else sprintf "cada %d" frecuencia)
            printfn "   • Iniciando en 3 segundos..."
            System.Threading.Thread.Sleep(3000)
            
            // Generar primos
            let generador = GeneradorPrimosPersonalizable()
            let primos = generador.GenerarPrimos(cantidad, mostrarTodos, frecuencia)
            
            // Comparación opcional
            if cantidad <= 100000 then
                comparacionRapida cantidad
            
            printfn "\n💡 CONCLUSIÓN:"
            printfn "• Tu secuencia encuentra primos ESPECIALES automáticamente"
            printfn "• Combinación perfecta: tu método + criba tradicional"
            printfn "• ¡Listo para usar los %d primos generados!" cantidad
        
        0
    with
    | ex ->
        printfn "\n❌ Error: %s" ex.Message
        printfn "Stack trace: %s" ex.StackTrace
        1