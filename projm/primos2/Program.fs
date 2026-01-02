open System
open System.IO
open System.Numerics
open Newtonsoft.Json
open System.Text.RegularExpressions
//******* Script1
let maxRepetitions = 31
let listRepeatedStrings = 
    [1..maxRepetitions] 
    |> List.map (fun n -> String.replicate n "10")
let initialValue = 2L
let rec nextValueFixed (currentValue, iteration) =
    if iteration > maxRepetitions then
        None
    else
        let nextV = 4L * currentValue + 2L
        Some (currentValue, (nextV, iteration + 1))
let listIntSequence =
    Seq.unfold nextValueFixed (initialValue, 1)
    |> List.ofSeq
listRepeatedStrings |> List.iter (printfn "%s")
listIntSequence |> List.iter (printfn "%A")
//******* Script2
let maxN = 27
let sieveOfEratosthenes maxLimit =
    let limit = int maxLimit
    let isPrime = Array.create (limit + 1) true 
    isPrime.[0] <- false
    if limit >= 1 then isPrime.[1] <- false
    let sqrtLimit = int (Math.Sqrt (float limit))

    for p in 2..sqrtLimit do
        if isPrime.[p] then
            let mutable multiple = p * p
            while multiple <= limit do
                isPrime.[multiple] <- false
                multiple <- multiple + p
    [ 2 .. limit ]
    |> List.filter (fun i -> isPrime.[i])
    |> List.map bigint
let findLastN () =
    let pattern = new Regex(@"2_(\d+)\.json")
    let files = Directory.GetFiles(Directory.GetCurrentDirectory(), "2_*.json")
    let nValues = 
        files
        |> Seq.fold (fun acc filePath ->
            let fileName = Path.GetFileName(filePath)
            let matchResult = pattern.Match(fileName)
            if matchResult.Success then
                let nString = matchResult.Groups.[1].Value
                let mutable n = 0
                match Int32.TryParse(nString, &n) with
                | true -> 
                    n :: acc 
                | false -> 
                    acc 
            else
                acc
        ) []
    match nValues with
    | [] -> 0
    | head :: tail -> head :: tail |> List.maxBy id
let generateAndSavePrimes maxN =
    let lastN = findLastN ()
    let startN = lastN + 1
    printfn "----------------------------------------------------"
    if startN > 1 then
        printfn "✅ Reanudando desde N = %i. El próximo archivo será 2_%i.json." lastN startN
    else
        printfn "🆕 No se encontraron archivos previos. Iniciando desde N = 1."
    printfn "----------------------------------------------------"
    if startN > maxN then
        printfn "Advertencia: El último N guardado (%i) es igual o mayor que el maxN configurado (%i). Proceso omitido." maxN maxN
    else
        let mutable currentLimit = bigint.One
        for _ in 1..lastN do
            currentLimit <- currentLimit * bigint.Parse("2")
        for n in startN..maxN do
            currentLimit <- currentLimit * bigint.Parse("2")
            printf "Procesando hasta 2^%i (%A)... " n currentLimit
            let primeList = sieveOfEratosthenes currentLimit 
            let settings = new JsonSerializerSettings(Formatting = Formatting.Indented)
            let jsonOutput = JsonConvert.SerializeObject(primeList, settings)
            let fileName = sprintf "2_%i.json" n
            File.WriteAllText(fileName, jsonOutput)
            printfn "Guardado en %s con %i primos encontrados." fileName (List.length primeList)
        printfn "----------------------------------------------------"
        printfn "Proceso finalizado."
generateAndSavePrimes maxN
//******************** Script3
let TARGET_PRIME_COUNT = 32
let fileName = "primes_pattern_results.json"
type PrimeResultString = { Item1: string; Item2: int }
type CombinationResult = {
    P_q1_Prime: string;
    TwoToQ3: string;
    P_q2_Prime: string;
    Result_Term1: string;
}
let xcvxcv () =
    if not (File.Exists(fileName)) then
        printfn "❌ Error: El archivo de primos %s no se encontró." fileName
        exit 1
    let jsonText = File.ReadAllText(fileName)
    let currentPrimes : list<bigint> = 
        JsonConvert.DeserializeObject<list<PrimeResultString>>(jsonText)
        |> List.map (fun item -> BigInteger.Parse(item.Item1))
    let listIntSequenceBigInt: list<bigint> = 
        listIntSequence 
        |> List.map BigInteger
    printfn "Se encontraron %i primos previamente." (List.length currentPrimes)
    let primesArray = currentPrimes |> List.toArray
    let listLength = primesArray.Length
    let mutable matchedCombinations: list<CombinationResult> = []
    printfn "--- Iniciando la búsqueda de coincidencias (%i combinaciones) ---" (listLength * listLength * 33)
    for q1 in 0 .. listLength - 1 do
        let pq1 = primesArray.[q1]
        for q2 in 0 .. listLength - 1 do
            let pq2 = primesArray.[q2]
            for q3 in 0 .. 32 do
                let twoToQ3 = bigint.Pow(2I, q3)
                let term1 = (pq1 * twoToQ3) - (pq2 * 2I)
                if listIntSequenceBigInt |> List.exists (fun x -> x = term1) then
                    printfn "✅ COINCIDENCIA: ((%s)(%s))-(%s * 2) = %s" 
                        (string pq1) 
                        (string twoToQ3)
                        (string pq2) 
                        (string term1)
                    let resultRecord = {
                        P_q1_Prime = string pq1;
                        TwoToQ3 = string twoToQ3;
                        P_q2_Prime = string pq2;
                        Result_Term1 = string term1;
                    }
                    matchedCombinations <- resultRecord :: matchedCombinations
    let outputFileName = "_combinations_results.json"
    let finalResults = matchedCombinations |> List.rev
    let settings = new JsonSerializerSettings(Formatting = Formatting.Indented)
    let jsonOutput = JsonConvert.SerializeObject(finalResults, settings)
    File.WriteAllText(outputFileName, jsonOutput)
    printfn "----------------------------------------------------"
    printfn "🎉 Proceso finalizado. %i coincidencias guardadas en %s" (List.length finalResults) outputFileName
xcvxcv()
let parseBinaryToBigInt (binaryString: string) : bigint =
    binaryString
    |> Seq.rev
    |> Seq.mapi (fun index bitChar ->
        match bitChar with
        | '1' ->
            bigint.Pow(2I, index) 
        | _ -> 
            0I
    )
    |> Seq.sum
let generatePatternValue n =
    if n < 1 then failwith "n debe ser mayor o igual a 1"
    let binaryString = String.replicate n "10" + "11"
    parseBinaryToBigInt binaryString
let esPrimoProbabilistico (n: BigInteger) (k: int) (basesFromFile: BigInteger array) =
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
        let bases = basesFromFile
        let mutable esPrimo = true
        for i in 0 .. (min (k - 1) (bases.Length - 1)) do
            if not (testWitness bases.[i]) then
                esPrimo <- false
        esPrimo
let loadPrimesFromFile (n: int) (maxBases: int) : BigInteger array =
    let fileName = sprintf "2_%i.json" n
    if not (File.Exists(fileName)) then
        printfn "❌ Error: El archivo de bases %s no se encontró. Usando bases por defecto." fileName
        [|2I; 3I; 5I; 7I; 11I; 13I; 17I; 19I; 23I; 29I; 31I; 37I|]
    else
        try
            let jsonText = File.ReadAllText(fileName)
            let allPrimes = JsonConvert.DeserializeObject<list<bigint>>(jsonText)
            allPrimes
            |> List.take maxBases
            |> List.toArray
        with ex ->
            printfn "Advertencia: Error al cargar las bases desde %s: %s. Usando bases por defecto." fileName ex.Message
            [|2I; 3I; 5I; 7I; 11I; 13I; 17I; 19I; 23I; 29I; 31I; 37I|]
let generatePatternPrimes (TARGET_PRIME_COUNT: int) =
    let fileName = "_primes_pattern_results.json"
    let bases = loadPrimesFromFile 27 100
    let mutable currentPrimes = []
    if File.Exists(fileName) then
        printfn "✅ Reanudando: Cargando primos previos..."
        try
            let jsonText = File.ReadAllText(fileName)
            currentPrimes <- JsonConvert.DeserializeObject<list<bigint * int>>(jsonText)
            printfn "Se encontraron %i primos previamente." (List.length currentPrimes)
        with ex ->
            printfn "Advertencia: No se pudo leer el archivo JSON: %s" ex.Message
    let mutable primesFound = List.length currentPrimes
    let mutable n =
        currentPrimes 
        |> List.tryPick (fun (_, index) -> Some index) 
        |> Option.defaultValue 0
    let mutable startN = n + 1
    printfn "----------------------------------------------------"
    if primesFound >= TARGET_PRIME_COUNT then
        printfn "🎯 Meta alcanzada: Ya se encontraron %i primos (TARGET = %i)." primesFound TARGET_PRIME_COUNT
    else
        printfn "Iniciando la búsqueda. Primos faltantes: %i. Comenzando patrón N = %i." 
            (TARGET_PRIME_COUNT - primesFound) startN
        printfn "----------------------------------------------------"
        n <- startN
        while primesFound < TARGET_PRIME_COUNT do
            let value = generatePatternValue n
            if esPrimoProbabilistico value 10 bases then
                printfn "  🌟 PRIMO #%i (N=%i): %A" (primesFound + 1) n value
                let newPrime = (value, n)
                currentPrimes <- newPrime :: currentPrimes
                primesFound <- primesFound + 1
                let settings = new JsonSerializerSettings(Formatting = Formatting.Indented)
                let serializablePrimes = currentPrimes |> List.rev |> List.map (fun (v, i) -> { Item1 = string v; Item2 = i })
                let jsonOutput = JsonConvert.SerializeObject(serializablePrimes, settings)
                File.WriteAllText(fileName, jsonOutput)
                
            else
                ()
            n <- n + 1 
        printfn "----------------------------------------------------"
        printfn "✅ ¡Éxito! Se encontraron %i primos. Resultados guardados en %s" primesFound fileName
generatePatternPrimes TARGET_PRIME_COUNT
System.Environment.Exit(0)
printfn "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
//type GeneradorPrimosPersonalizable() =
//    let mutable primosEncontrados = []
//    let inicioTiempo = DateTime.Now
    
//    // Test de primalidad optimizado
//    let esPrimo (n: int64) =
//        if n < 2L then false
//        elif n = 2L || n = 3L then true
//        elif n % 2L = 0L || n % 3L = 0L then false
//        else
//            let mutable i = 5L
//            let mutable resultado = true
//            while i * i <= n && resultado do
//                if n % i = 0L || n % (i + 2L) = 0L then
//                    resultado <- false
//                i <- i + 6L
//            resultado

//    // Encuentra factores primos pequeños
//    let buscarFactoresPequenos (n: int64) =
//        let mutable factores = Set.empty
//        let mutable temp = n
        
//        // Factor 2
//        while temp % 2L = 0L do
//            factores <- factores.Add(2L)
//            temp <- temp / 2L
        
//        // Factores impares
//        let mutable p = 3L
//        while p * p <= temp && p <= 1000000L do
//            if temp % p = 0L then
//                if esPrimo p then
//                    factores <- factores.Add(p)
//                temp <- temp / p
//            else
//                p <- p + 2L
        
//        if temp > 1L && temp <= 1000000L && esPrimo temp then
//            factores <- factores.Add(temp)
            
//        factores

//    // Mostrar primo según preferencias
//    let mostrarPrimo primo contador terminoActual mostrarTodos frecuencia =
//        let tiempoTranscurrido = (DateTime.Now - inicioTiempo).TotalSeconds
//        let primosPorSegundo = if tiempoTranscurrido > 0.0 then float contador / tiempoTranscurrido else 0.0
        
//        let mostrar = 
//            mostrarTodos || 
//            contador <= 100 || 
//            contador % frecuencia = 0 || 
//            List.contains primo [2L; 3L; 5L; 7L; 17L; 31L; 127L; 257L; 8191L; 65537L]
        
//        if mostrar then
//            printfn "#%6d: %8d | Término: %5s | Tiempo: %7.2fs | Velocidad: %6.1f primos/s" 
//                contador primo terminoActual tiempoTranscurrido primosPorSegundo

//    // Encontrar primos modulares (versión simplificada)
//    let encontrarPrimosModulares n limite =
//        let mutable primos = Set.empty
        
//        for p in 2L .. int64 (min limite 50000) do
//            if not (List.contains p primosEncontrados) && esPrimo p then
//                // Versión simplificada sin BigInteger
//                if p % int64 n = 1L || p % int64 n = int64 n - 1L then
//                    primos <- primos.Add(p)
        
//        primos

//    // Generar criba rápida
//    let generarCribaRapida cantidadActual cantidadTotal =
//        let cantidadNecesaria = cantidadTotal - cantidadActual
//        if cantidadNecesaria <= 0 then 
//            []
//        else
//            let limite = int (float cantidadTotal * Math.Log(float cantidadTotal) * 1.3)
//            printfn "   🎯 Generando %d primos más con criba (límite: %d)..." cantidadNecesaria limite
            
//            let esPrimoArr = Array.create (limite + 1) true
//            esPrimoArr.[0] <- false
//            esPrimoArr.[1] <- false
            
//            for i in 2 .. int (sqrt (float limite)) do
//                if esPrimoArr.[i] then
//                    for j in i*i .. i .. limite do
//                        if j < esPrimoArr.Length then
//                            esPrimoArr.[j] <- false
            
//            let todosPrimos = 
//                [| for i in 2 .. limite do if esPrimoArr.[i] then yield int64 i |]
            
//            let nuevosPrimos = 
//                todosPrimos 
//                |> Array.filter (fun p -> not (List.contains p primosEncontrados))
//                |> Array.truncate cantidadNecesaria
//                |> Array.toList
            
//            nuevosPrimos

//    // Mostrar resumen final
//    let mostrarResumenFinal tiempoTotal cantidadObjetivo =
//        printfn "\n%s" (String('=', 80))
//        printfn "🎉 GENERACIÓN COMPLETADA!"
//        printfn "%s" (String('=', 80))
//        printfn "📊 ESTADÍSTICAS FINALES:"
//        printfn "   • Primos generados: %d de %d" (List.length primosEncontrados) cantidadObjetivo
//        printfn "   • Tiempo total: %.2f segundos" tiempoTotal
        
//        if tiempoTotal > 0.0 then
//            let velocidad = float (List.length primosEncontrados) / tiempoTotal
//            printfn "   • Velocidad promedio: %.1f primos/segundo" velocidad
        
//        // Primos especiales encontrados
//        let primosEspeciales = 
//            primosEncontrados 
//            |> List.filter (fun p -> List.contains p [2L; 3L; 5L; 7L; 17L; 31L; 127L; 257L; 8191L; 65537L])
        
//        if not primosEspeciales.IsEmpty then
//            printfn "\n🔍 PRIMOS ESPECIALES ENCONTRADOS:"
//            printfn "   %A" primosEspeciales
        
//        // Verificación
//        if List.length primosEncontrados >= 100 then
//            let muestra = primosEncontrados |> List.take 100
//            let todosSonPrimos = muestra |> List.forall esPrimo
//            printfn "   ✓ Verificación (primeros 100): %s" (if todosSonPrimos then "TODOS VÁLIDOS" else "ERROR")
        
//        // Últimos primos
//        if List.length primosEncontrados >= 5 then
//            let ultimos = primosEncontrados |> List.rev |> List.take 5
//            printfn "   Últimos 5 primos: %A" ultimos

//    // Método principal para generar primos
//    member this.GenerarPrimos(cantidadTotal, mostrarTodos, frecuenciaMuestra) =
//        printfn "🚀 INICIANDO GENERACIÓN DE %d PRIMOS" cantidadTotal
//        printfn "%s" (String('=', 80))
//        printfn " #       Primo   | Término |  Tiempo  | Velocidad"
//        printfn "%s" (String('-', 80))
        
//        let mutable contadorPrimos = 0
//        let mutable terminoActual = 1
//        let mutable aActual = 2L
        
//        // FASE 1: Usar secuencia para primos especiales
//        let objetivoFase1 = min 50000 (int (float cantidadTotal * 0.3))
        
//        while contadorPrimos < objetivoFase1 && terminoActual <= 100 do
//            // Tu secuencia para primos especiales
//            if aActual < 10000000000L then
//                let factores = buscarFactoresPequenos aActual
                
//                for primo in factores do
//                    if not (List.contains primo primosEncontrados) && contadorPrimos < objetivoFase1 then
//                        primosEncontrados <- primo :: primosEncontrados
//                        contadorPrimos <- contadorPrimos + 1
//                        mostrarPrimo primo contadorPrimos (string terminoActual) mostrarTodos frecuenciaMuestra
            
//            // Propiedades modulares
//            let primosModulares = encontrarPrimosModulares terminoActual 100000
//            for primo in primosModulares do
//                if not (List.contains primo primosEncontrados) && contadorPrimos < objetivoFase1 then
//                    primosEncontrados <- primo :: primosEncontrados
//                    contadorPrimos <- contadorPrimos + 1
//                    mostrarPrimo primo contadorPrimos (sprintf "M%d" terminoActual) mostrarTodos frecuenciaMuestra
            
//            aActual <- 4L * aActual + 2L
//            terminoActual <- terminoActual + 1
        
//        // FASE 2: Completar con criba
//        if contadorPrimos < cantidadTotal then
//            printfn "\n⚡ COMPLETANDO CON CRIBA RÁPIDA..."
//            let primosCriba = generarCribaRapida contadorPrimos cantidadTotal
            
//            for primo in primosCriba do
//                if not (List.contains primo primosEncontrados) && contadorPrimos < cantidadTotal then
//                    primosEncontrados <- primo :: primosEncontrados
//                    contadorPrimos <- contadorPrimos + 1
                    
//                    // Mostrar progreso durante la criba
//                    if mostrarTodos || 
//                       contadorPrimos % (max 1 (cantidadTotal / 20)) = 0 || 
//                       contadorPrimos <= int (float cantidadTotal * 0.1) then
//                        mostrarPrimo primo contadorPrimos "CRIBA" mostrarTodos frecuenciaMuestra
        
//        let tiempoTotal = (DateTime.Now - inicioTiempo).TotalSeconds
//        mostrarResumenFinal tiempoTotal cantidadTotal
        
//        primosEncontrados |> List.rev |> List.truncate cantidadTotal

//// Interfaz de usuario corregida
//let obtenerConfiguracion() =
//    printfn "🎛️  CONFIGURACIÓN DEL GENERADOR DE PRIMOS"
//    printfn "%s" (String('=', 50))
    
//    try
//        // Cantidad de primos
//        let rec obtenerCantidad() =
//            printf "¿Cuántos primos quieres generar? (ej: 100, 1000, 10000): "
//            match Int32.TryParse(Console.ReadLine()) with
//            | (true, n) when n > 0 -> n
//            | _ -> 
//                printfn "❌ Por favor ingresa un número positivo"
//                obtenerCantidad()
        
//        let cantidad = obtenerCantidad()
//        printfn ""

//        // Modo de visualización
//        printfn "📊 OPCIONES DE VISUALIZACIÓN:"
//        printfn "   1. Mostrar TODOS los primos (pantalla completa)"
//        printfn "   2. Mostrar cada X primos (progreso)"
//        printfn "   3. Solo mostrar resumen final (más rápido)"
        
//        let rec obtenerOpcion() =
//            printf "Elige una opción (1-3): "
//            match Int32.TryParse(Console.ReadLine()) with
//            | (true, n) when n >= 1 && n <= 3 -> n
//            | _ -> 
//                printfn "❌ Por favor elige 1, 2 o 3"
//                obtenerOpcion()
        
//        let opcion = obtenerOpcion()

//        let (mostrarTodos, frecuencia) =
//            match opcion with
//            | 1 -> (true, 1)
//            | 2 -> 
//                let rec obtenerFrecuencia() =
//                    printf "¿Mostrar cada cuántos primos? (ej: 100, 500, 1000): "
//                    match Int32.TryParse(Console.ReadLine()) with
//                    | (true, n) when n > 0 -> n
//                    | _ -> 
//                        printfn "❌ Por favor ingresa un número positivo"
//                        obtenerFrecuencia()
//                (false, obtenerFrecuencia())
//            | _ -> (false, max 1 (cantidad / 10))
        
//        cantidad, mostrarTodos, frecuencia
        
//    with
//    | :? OperationCanceledException ->
//        printfn "\n\n⏹️  Configuración cancelada por el usuario"
//        (0, false, 1)

//// Comparación rápida
//let comparacionRapida cantidad =
//    printfn "\n⚡ COMPARACIÓN: CRIBA TRADICIONAL para %d primos" cantidad
//    let inicio = DateTime.Now
    
//    let limite = 
//        if cantidad <= 10 then 30
//        else int (float cantidad * Math.Log(float cantidad) * 1.2)
    
//    let esPrimoArr = Array.create (limite + 1) true
//    esPrimoArr.[0] <- false
//    esPrimoArr.[1] <- false
    
//    for i in 2 .. int (sqrt (float limite)) do
//        if esPrimoArr.[i] then
//            for j in i*i .. i .. limite do
//                if j < esPrimoArr.Length then
//                    esPrimoArr.[j] <- false
    
//    let primosCriba = 
//        [| for i in 2 .. limite do if esPrimoArr.[i] then yield int64 i |]
    
//    let tiempo = (DateTime.Now - inicio).TotalSeconds
//    printfn "✅ %d primos en %.4fs" primosCriba.Length tiempo
//    if tiempo > 0.0 then
//        printfn "   • Velocidad: %.0f primos/segundo" (float primosCriba.Length / tiempo)

//// Programa principal
//[<EntryPoint>]
//let main argv =
//    printfn "🎊 GENERADOR PERSONALIZABLE DE PRIMOS"
//    printfn "Basado en tu secuencia diádica descubierta"
//    printfn "%s" (String('=', 60))
    
//    try
//        // Obtener configuración
//        let cantidad, mostrarTodos, frecuencia = obtenerConfiguracion()
        
//        if cantidad > 0 then
//            printfn "\n🎯 CONFIGURACIÓN ELEGIDA:"
//            printfn "   • Primos a generar: %d" cantidad
//            printfn "   • Modo visualización: %s" (if mostrarTodos then "TODOS" else sprintf "cada %d" frecuencia)
//            printfn "   • Iniciando en 3 segundos..."
//            System.Threading.Thread.Sleep(3000)
            
//            // Generar primos
//            let generador = GeneradorPrimosPersonalizable()
//            let primos = generador.GenerarPrimos(cantidad, mostrarTodos, frecuencia)
            
//            // Comparación opcional
//            if cantidad <= 100000 then
//                comparacionRapida cantidad
            
//            printfn "\n💡 CONCLUSIÓN:"
//            printfn "• Tu secuencia encuentra primos ESPECIALES automáticamente"
//            printfn "• Combinación perfecta: tu método + criba tradicional"
//            printfn "• ¡Listo para usar los %d primos generados!" cantidad
        
//        0
//    with
//    | ex ->
//        printfn "\n❌ Error: %s" ex.Message
//        printfn "Stack trace: %s" ex.StackTrace
//        1