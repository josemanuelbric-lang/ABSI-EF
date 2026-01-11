open System
open System.Numerics
open System.IO

// =============================================
// CAZADOR DE PRIMOS INFINITO
// =============================================

type CazadorPrimosInfinito() =
    let mutable primoMasGrande = BigInteger.Zero
    let mutable terminoActual = 1
    let mutable aActual = BigInteger(2)
    let mutable inicioTiempo = DateTime.Now
    let mutable ultimoExponenteGuardado = 0
    let archivoResultados = "primos_gigantes.txt"

    // Crear archivo de resultados si no existe
    do
        if not (File.Exists(archivoResultados)) then
            File.WriteAllText(archivoResultados, 
                "=== REGISTRO DE PRIMOS GIGANTES ===\n" +
                "Fecha de inicio: " + DateTime.Now.ToString() + "\n" +
                "Secuencia: aₙ = 4aₙ₋₁ + 2\n" +
                "===================================\n\n")

    // Test de primalidad Miller-Rabin optimizado
    let esPrimoProbabilistico (n: BigInteger) (k: int) =
        if n < 2I then false
        elif n = 2I || n = 3I then true
        elif n % 2I = 0I then false
        else
            let mutable d = n - 1I
            let mutable r = 0
            while d % 2I = 0I do
                d <- d / 2I
                r <- r + 1
            
            let testWitness (a: BigInteger) =
                let mutable x = BigInteger.ModPow(a, d, n)
                if x = 1I || x = n - 1I then true
                else
                    let mutable continuar = true
                    let mutable resultado = false
                    for _ in 1 .. (r - 1) do
                        if continuar then
                            x <- BigInteger.ModPow(x, 2I, n)
                            if x = n - 1I then
                                resultado <- true
                                continuar <- false
                    resultado
            
            let bases = [|2I; 3I; 5I; 7I; 11I; 13I; 17I; 19I; 23I; 29I; 31I; 37I|]
            let mutable esPrimo = true
            
            for i in 0 .. (min (k - 1) (bases.Length - 1)) do
                if not (testWitness bases.[i]) then
                    esPrimo <- false
            esPrimo

    // Guardar primo en archivo si es mayor que 2^N
    let guardarPrimoSiEsGrande (primo: BigInteger) (termino: int) =
        let mutable exponente = ultimoExponenteGuardado + 1
        let mutable debeGuardar = false
        
        // Encontrar el mayor 2^N que sea menor que el primo
        while BigInteger.Pow(2I, exponente) <= primo do
            exponente <- exponente + 1
        
        // Si encontramos un nuevo exponente máximo, guardar
        if exponente - 1 > ultimoExponenteGuardado then
            ultimoExponenteGuardado <- exponente - 1
            debeGuardar <- true
            
            let tiempoTranscurrido = DateTime.Now - inicioTiempo
            let registro = 
                sprintf "\n🎯 NUEVO RÉCORD: Término %d\n" termino +
                sprintf "📅 Fecha: %s\n" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")) +
                sprintf "⏱️  Tiempo transcurrido: %02d:%02d:%02d\n" tiempoTranscurrido.Hours tiempoTranscurrido.Minutes tiempoTranscurrido.Seconds +
                sprintf "🔢 Primo: %s\n" (primo.ToString()) +
                sprintf "📏 Dígitos: %d\n" (primo.ToString().Length) +
                sprintf "⚡ Mayor que: 2^%d = %s\n" ultimoExponenteGuardado (BigInteger.Pow(2I, ultimoExponenteGuardado).ToString()) +
                sprintf "%s\n" (String('=', 80))
            
            File.AppendAllText(archivoResultados, registro)
            printfn "💾 GUARDADO EN ARCHIVO: Primo mayor que 2^%d" ultimoExponenteGuardado
        
        debeGuardar

    // Mostrar progreso en consola
    let mostrarProgreso (primo: BigInteger) (termino: int) (esNuevoRecord: bool) =
        let tiempoTranscurrido = DateTime.Now - inicioTiempo
        let digitos = primo.ToString().Length
        
        if esNuevoRecord then
            printfn "\n🎉 ¡NUEVO RÉCORD! Término %d" termino
            printfn "   🔢 Primo: %s" (primo.ToString())
            printfn "   📏 Dígitos: %d" digitos
            printfn "   ⏱️  Tiempo: %02d:%02d:%02d" 
                tiempoTranscurrido.Hours tiempoTranscurrido.Minutes tiempoTranscurrido.Seconds
            printfn "   ⚡ Mayor que: 2^%d" ultimoExponenteGuardado
            printfn "   %s" (String('~', 50))
        else
            printfn "📊 Término %6d | Dígitos: %6d | Tiempo: %02d:%02d:%02d" 
                termino digitos
                tiempoTranscurrido.Hours tiempoTranscurrido.Minutes tiempoTranscurrido.Seconds

    // Buscar primos en el término actual
    let buscarPrimosEnTermino (a_n: BigInteger) (termino: int) =
        let mutable primosEncontrados = []

        // Verificar si el término actual es primo
        if esPrimoProbabilistico a_n 8 then
            primosEncontrados <- a_n :: primosEncontrados

        // Verificar n-1 y n+1 (patrón común en la secuencia)
        let nMenos1 = a_n - 1I
        let nMas1 = a_n + 1I
        
        if esPrimoProbabilistico nMenos1 6 then
            primosEncontrados <- nMenos1 :: primosEncontrados
        
        if esPrimoProbabilistico nMas1 6 then
            primosEncontrados <- nMas1 :: primosEncontrados

        primosEncontrados

    // Ejecución infinita
    member this.IniciarBusquedaInfinita() =
        printfn "🚀 CAZADOR DE PRIMOS INFINITO"
        printfn "%s" (String('=', 70))
        printfn "🔍 Buscando primos más grandes que 2^N usando tu secuencia diádica"
        printfn "💾 Los resultados se guardan en: %s" archivoResultados
        printfn "⏰ Inicio: %s" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"))
        printfn "%s" (String('=', 70))
        
        // Escribir encabezado en archivo
        File.AppendAllText(archivoResultados, 
            sprintf "\n🚀 INICIO DE BÚSQUEDA INFINITA\n" +
            sprintf "📅 %s\n" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")) +
            sprintf "%s\n" (String('=', 60)))
        
        let mutable continuar = true
        
        try
            while continuar do
                // Calcular término actual: aₙ = 4aₙ₋₁ + 2
                if terminoActual = 1 then
                    aActual <- BigInteger(2)
                else
                    aActual <- 4I * aActual + 2I
                
                // Buscar primos en este término
                let primosEncontrados = buscarPrimosEnTermino aActual terminoActual
                printfn "%s====%A" (aActual.ToString()) (primosEncontrados)
                for primo in primosEncontrados do
                    if primo > primoMasGrande then
                        primoMasGrande <- primo
                        let esNuevoRecord = guardarPrimoSiEsGrande primo terminoActual
                        mostrarProgreso primo terminoActual esNuevoRecord
                
                // Mostrar progreso cada 100 términos
                if terminoActual % 100 = 0 then
                    if primoMasGrande > BigInteger.Zero then
                        mostrarProgreso primoMasGrande terminoActual false
                    else
                        let tiempoTranscurrido = DateTime.Now - inicioTiempo
                        printfn "📊 Término %6d | Sin primos encontrados aún | Tiempo: %02d:%02d:%02d" 
                            terminoActual
                            tiempoTranscurrido.Hours tiempoTranscurrido.Minutes tiempoTranscurrido.Seconds
                
                terminoActual <- terminoActual + 1
                
                // Pequeña pausa para no saturar la CPU
                if terminoActual % 1000 = 0 then
                    System.Threading.Thread.Sleep(10)
                    
        with
        | ex ->
            printfn "\n❌ ERROR: %s" ex.Message
            printfn "Stack trace: %s" ex.StackTrace
            File.AppendAllText(archivoResultados, 
                sprintf "\n❌ ERROR DETENIDO: %s\n" ex.Message +
                sprintf "📅 %s\n" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")))

    // Mostrar resumen actual
    member this.MostrarResumen() =
        let tiempoTotal = DateTime.Now - inicioTiempo
        printfn "\n%s" (String('=', 70))
        printfn "📊 RESUMEN ACTUAL"
        printfn "%s" (String('=', 70))
        printfn "   • Términos procesados: %d" (terminoActual - 1)
        printfn "   • Tiempo ejecución: %02d:%02d:%02d" 
            tiempoTotal.Hours tiempoTotal.Minutes tiempoTotal.Seconds
        printfn "   • Primo más grande: %s" (if primoMasGrande > BigInteger.Zero then primoMasGrande.ToString() else "Ninguno aún")
        printfn "   • Dígitos del primo más grande: %d" (if primoMasGrande > BigInteger.Zero then primoMasGrande.ToString().Length else 0)
        printfn "   • Mayor que: 2^%d" ultimoExponenteGuardado
        printfn "   • Archivo de resultados: %s" archivoResultados

// =============================================
// PROGRAMA PRINCIPAL
// =============================================

[<EntryPoint>]
let main argv =
    printfn "🎯 CAZADOR DE PRIMOS INFINITO - SECUENCIA DIÁDICA"
    printfn "%s" (String('=', 70))
    printfn "Este programa ejecutará indefinidamente buscando primos gigantes."
    printfn "Los resultados se guardarán automáticamente en 'primos_gigantes.txt'"
    printfn "%s" (String('=', 70))
    
    printfn "\n⚙️  CONFIGURACIÓN:"
    printfn "   • Sin límite de términos"
    printfn "   • Sin límite de dígitos"
    printfn "   • Ejecución continua"
    printfn "   • Guarda automáticamente primos > 2^N"
    
    printfn "\n🎯 OBJETIVO:"
    printfn "   Encontrar el primo más grande posible usando aₙ = 4aₙ₋₁ + 2"
    
    printfn "\n⏰ Iniciando en 5 segundos..."
    printfn "   Presiona Ctrl+C para detener la ejecución"
    
    for i in 1 .. -1 .. 1 do
        printfn "   %d..." i
        System.Threading.Thread.Sleep(1000)
    
    printfn "\n%s" (String('=', 70))
    printfn "🚀 INICIANDO BÚSQUEDA INFINITA..."
    printfn "%s" (String('=', 70))
    
    let cazador = CazadorPrimosInfinito()
    
    // Manejar Ctrl+C para mostrar resumen antes de salir
    Console.CancelKeyPress.Add(fun args ->
        args.Cancel <- true
        printfn "\n\n⏹️  DETENIENDO EJECUCIÓN..."
        cazador.MostrarResumen()
        printfn "\n👋 ¡Hasta luego!"
        Environment.Exit(0)
    )
    
    try
        cazador.IniciarBusquedaInfinita()
        0
    with
    | ex ->
        printfn "\n❌ ERROR CRÍTICO: %s" ex.Message
        printfn "Stack trace: %s" ex.StackTrace
        1