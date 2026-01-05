open System
open System.Collections.Generic
open System.Diagnostics
open System.Text
open System.Numerics
open System.IO
open File1
let collatz (n: BigInteger) =
    if n % 2I = 0I then (n / 2I, "R")
    else (3I * n + 1I, "L")

let detectarPatron (valores: BigInteger list) =
    match valores with
    | v0 :: v1 :: _ ->
        let salto = v1 - v0
        let rec check (list: BigInteger list) =
            match list with
            | a :: b :: rest -> if b - a = salto then check (b :: rest) else false
            | _ -> true
        if check valores then Some(v0, salto) else None
    | _ -> None
let verificarYImprimir (vPP: BigInteger) (vPI: BigInteger) (vIP: BigInteger) (vII: BigInteger) (vPP2: BigInteger) (vPI2: BigInteger) (vIP2: BigInteger) (vII2: BigInteger) (exponenteActual: int) =
    let total = vPP + vPI + vIP + vII + vPP2 + vPI2 + vIP2 + vII2
    let umbralActual = BigInteger.Pow(BigInteger(2), exponenteActual)
    if total >= umbralActual then
        printfn "2^%d PP=%A PI=%-6A IP=%-6A II=%-6A PP2=%-6A PI2=%-6A IP2=%-6A II2=%-6A | Total=%A" exponenteActual vPP vPI vIP vII vPP2 vPI2 vIP2 vII2 total
        exponenteActual + 1
    else
        exponenteActual

let Imprimir (vPP: BigInteger) (vPI: BigInteger) (vIP: BigInteger) (vII: BigInteger) (vPP2: BigInteger) (vPI2: BigInteger) (vIP2: BigInteger) (vII2: BigInteger) =
    let total = vPP + vPI + vIP + vII + vPP2 + vPI2 + vIP2 + vII2
    //let fmt (n: bigint) = n.ToString().PadRight(8) // Ajusta el 8 según qué tan grande sea el número
    printfn "PP=%s + %s PI=%s + %s IP=%s + %s II=%s + %s Total=%A" 
        (vPP.ToString().PadRight(5)) (vPP2.ToString().PadRight(8))
        (vPI.ToString().PadRight(5)) (vPI2.ToString().PadRight(8))
        (vIP.ToString().PadRight(0)) (vIP2.ToString().PadRight(0))
        (vII.ToString().PadRight(5)) (vII2.ToString().PadRight(8))
        total
    //printfn "PP=%-6A + %-8A | PI=%-6A + %-8A | IP=%-6A + %-8A | II=%-6A + %-8A | Total=%-10A" vPP vPP2 vPI vPI2 vIP vIP2 vII vII2 total
    //printfn "PP=%4d + %-5d | PI=%4d + %-5d | IP=%4d + %-5d | II=%4d + %-5d | Total=%-7d" vPP vPP2 vPI vPI2 vIP vIP2 vII vII2 total
    //printfn "PP=%3A+%-5A PI=%3A+%-5A IP=%3A+%-5A II=%3A+%-5A Total=%-6A" vPP vPP2 vPI vPI2 vIP vIP2 vII vII2 total
    //printfn "PP=%A+%A\tPI=%A+%A\tIP=%A+%A\tII=%A+%A\tTotal=%A" vPP vPP2 vPI vPI2 vIP vIP2 vII vII2 total
let generarArbol (nodoInicio: NodoCollatz) (niveles: int) (semillasCount: int) (seconMode: bool) =
    
    let arbol = List<Dictionary<string, NodoCollatz>>()
    arbol.Add(Dictionary<string, NodoCollatz>(dict [("N", nodoInicio)]))
    
    let historialPatrones = HashSet<BigInteger * BigInteger>()
    let historialResultados = Dictionary<BigInteger * BigInteger, (BigInteger * BigInteger) option * (BigInteger * BigInteger) option>()
    let mutable vPP = 0I
    let mutable vII = 0I
    let mutable vPI = 0I
    let mutable vIP = 0I
    let mutable vPP2 = 0I
    let mutable vII2 = 0I
    let mutable vPI2 = 0I
    let mutable vIP2 = 0I
    let mutable exponenteObjetivo = 1
    for q1 in 0 .. niveles - 1 do
        let actual = arbol.[q1]
        let proximo = Dictionary<string, NodoCollatz>()
        //exponenteObjetivo <- verificarYImprimir vPP vPI vIP vII vPP2 vPI2 vIP2 vII2 exponenteObjetivo
        Imprimir vPP vPI vIP vII vPP2 vPI2 vIP2 vII2

        for kvp in actual do
            let ruta, nodo = kvp.Key, kvp.Value
            let llave = (nodo.Desplazamiento, nodo.Progresion)

            let procesarFunc (res: (BigInteger * BigInteger) option) (letra: string) =
                match res with
                | Some (d, p) ->
                    match (d % 2I = 0I, p % 2I = 0I) with
                    | (true, true)   ->
                        vPP2 <- vPP2 + 1I
                    | (true, false)  ->
                        vPI2 <- vPI2 + 1I
                    | (false, true)  ->
                        vIP2 <- vIP2 + 1I
                    | (false, false) ->
                        vII2 <- vII2 + 1I
                    let isDup = historialPatrones.Contains((d, p))
                    if not isDup then historialPatrones.Add((d, p)) |> ignore
                    proximo.[ruta + letra] <- { Desplazamiento = d; Progresion = p; Ruta = ruta + letra; Nivel = q1 + 1; EsDuplicado = isDup }
                | None -> ()
            if seconMode then
                let d, p = llave
                match historialResultados.TryGetValue(llave) with
                | true, (resR, resL) ->
                    procesarFunc resR "R"
                    procesarFunc resL "L"
                | _ ->
                    match (d % 2I = 0I, p % 2I = 0I) with
                    | (true, true)   ->
                        let newDR = d / 2I
                        let newPR = p / 2I
                        let resultadoR = Some(newDR, newPR)
                        procesarFunc resultadoR "R"
                        let resultadoL = None
                        historialResultados.[llave] <- (resultadoR, resultadoL)
                        vPP <- vPP + 1I
                    | (true, false)  ->
                        let newDR = d / 2I
                        let newPR= p
                        let resultadoR = Some(newDR, newPR)
                        procesarFunc resultadoR "R"
                        let newDL = (d * 3I) + (p * 3I) + 1I
                        let newPL= (p * 3I) * 2I
                        let resultadoL = Some(newDL, newPL)
                        procesarFunc resultadoL "L"
                        historialResultados.[llave] <- (resultadoR, resultadoL)
                        vPI <- vPI + 1I
                    | (false, true)  ->
                        printfn "IP"
                        vIP <- vIP + 1I
                    | (false, false) ->
                        let newDR=(d+p)/ 2I
                        let newPR= p
                        let resultadoR = Some(newDR, newPR)
                        procesarFunc resultadoR "R"
                        let newDL= (d*3I) + 1I
                        let newPL=(p * 3I) * 2I
                        let resultadoL = Some(newDL, newPL)
                        procesarFunc resultadoL "L"
                        historialResultados.[llave] <- (resultadoR, resultadoL)
                        vII <- vII + 1I
            else
                match historialResultados.TryGetValue(llave) with
                | true, (resR, resL) ->
                    procesarFunc resR "R"
                    procesarFunc resL "L"
                | _ ->
                    let mutable rVals = []
                    let mutable lVals = []
                    for i in 0 .. semillasCount - 1 do
                        let s = nodo.Progresion * BigInteger(i) + nodo.Desplazamiento
                        let v, b = collatz s
                        if b = "R" then rVals <- v :: rVals else lVals <- v :: lVals
                
                    let resR = detectarPatron (List.rev rVals)
                    let resL = detectarPatron (List.rev lVals)
                    historialResultados.[llave] <- (resR, resL)
                    procesarFunc resR "R"
                    procesarFunc resL "L"
        arbol.Add(proximo)
    arbol

let calcularSurrealDiadico (ruta: string) =
    let limpia = ruta.Replace("N", "")
    if String.IsNullOrEmpty(limpia) then "0 / 2^0"
    else
        let n = limpia.Length
        let denominador = bigint.Pow(2I, n - 1)
        let mutable numerador = 0I
        if limpia.[0] = 'L' then numerador <- -denominador
        else numerador <- denominador
        for i in 1 .. n - 1 do
            let peso = bigint.Pow(2I, n - 1 - i)
            if limpia.[i] = 'L' then
                numerador <- numerador - peso
            else
                numerador <- numerador + peso
        let exp = n - 1
        let valorDecimal = 
            if exp = 0 then 0.0 
            else float numerador / float denominador
        sprintf "%A / 2^%d %-16A" numerador (n - 1) valorDecimal
[<EntryPoint>]
let main argv =
    let nivelesTarget = 8
    let semillas = 32
    let nodoInicial = { Desplazamiento = 1I; Progresion = 1I; Ruta = "N"; Nivel = 0; EsDuplicado = false }

    let sw = Stopwatch.StartNew()
    let finalRes = generarArbol nodoInicial nivelesTarget semillas true
    sw.Stop()
    printfn "%d %f" nivelesTarget sw.Elapsed.TotalSeconds

    //let sw = Stopwatch.StartNew()
    //let finalRes2 = generarArbol nodoInicial nivelesTarget semillas false
    //sw.Stop()
    //printfn "%d %f" nivelesTarget sw.Elapsed.TotalSeconds

    //let sonIguales = compararArboles finalRes1 finalRes2
    //if (sonIguales) then
    //    printfn "Equals"
    //Environment.Exit(0)
    let sb = StringBuilder()
    let resumenSimetria = List<string>()

    for i in 0 .. finalRes.Count - 1 do
        sb.AppendLine(sprintf "\nNIVEL %d %s" i (String('-', 50))) |> ignore
        let nivel = finalRes.[i]
        let mutable rutasNR = 0
        let mutable rutasNLRRR = 0

        let sortedKeys = nivel.Keys |> Seq.sort
        let mutable isduplicateL = 0
        for ruta in sortedKeys do
            let nodo = nivel.[ruta]
            let fraccionDiadica = calcularSurrealDiadico ruta
            let lineaNodo = sprintf "%-16s \t%s"  (nodo.ToString())  fraccionDiadica
            if ruta.StartsWith("NR") then
                rutasNR <- rutasNR + 1
                //sb.AppendLine(lineaNodo) |> ignore
            elif ruta.StartsWith("NLRRR") then
                rutasNLRRR <- rutasNLRRR + 1
                //sb.AppendLine(lineaNodo) |> ignore
            else
                if (nodo.EsDuplicado) then isduplicateL <- isduplicateL + 1
                sb.AppendLine(lineaNodo) |> ignore
        if rutasNLRRR > 0 then
            let msg = sprintf "NIVEL %d-2 (Simetría NLRRR) Rutas: %d" i rutasNLRRR
            sb.AppendLine(msg) |> ignore
        if rutasNR > 0 then
            let msg = sprintf "NIVEL %d-1 (Simetría NR) Rutas: %d" i rutasNR
            sb.AppendLine(msg) |> ignore
        resumenSimetria.Add(sprintf "NIVEL %-4d NR: %-8d NLRRR: %-8d NL*: %-8d Total: %-8d" i rutasNR rutasNLRRR isduplicateL (isduplicateL+rutasNR+rutasNLRRR))
    printfn "%A" sb
    sb.AppendLine("\n" + String('=', 60)) |> ignore
    sb.AppendLine("RESUMEN DE SIMETRÍA:") |> ignore
    for line in resumenSimetria do
        sb.AppendLine(line) |> ignore
    //let nombreArchivo = "ResultadoCollatz.txt"
    //try
    //    File.WriteAllText(nombreArchivo, sb.ToString())
    //    printfn "Archivo guardado exitosamente: %s" nombreArchivo
    //with
    //| ex -> printfn "Error al guardar el archivo: %s" ex.Message
    //printfn "\nRESUMEN DE SIMETRÍA (Copia de seguridad en consola):"
    for line in resumenSimetria do printfn "%s" line
    0
