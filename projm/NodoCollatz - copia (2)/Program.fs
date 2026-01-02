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

let generarArbol (nodoInicio: NodoCollatz) (niveles: int) (semillasCount: int) (seconMode: bool) =
    let arbol = List<Dictionary<string, NodoCollatz>>()
    arbol.Add(Dictionary<string, NodoCollatz>(dict [("N", nodoInicio)]))
    
    let historialPatrones = HashSet<BigInteger * BigInteger>()
    let historialResultados = Dictionary<BigInteger * BigInteger, (BigInteger * BigInteger) option * (BigInteger * BigInteger) option>()

    for q1 in 0 .. niveles - 1 do
        let actual = arbol.[q1]
        let proximo = Dictionary<string, NodoCollatz>()

        for kvp in actual do
            let ruta, nodo = kvp.Key, kvp.Value
            let llave = (nodo.Desplazamiento, nodo.Progresion)

            let procesarFunc (res: (BigInteger * BigInteger) option) (letra: string) =
                match res with
                | Some (d, p) ->
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
                    | (false, true)  ->
                        printfn "IP"
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
[<EntryPoint>]
let main argv =
    let nivelesTarget = 16
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
            if ruta.StartsWith("NR") then
                rutasNR <- rutasNR + 1
            elif ruta.StartsWith("NLRRR") then
                rutasNLRRR <- rutasNLRRR + 1
            else
                if (nodo.EsDuplicado) then isduplicateL <- isduplicateL + 1
                sb.AppendLine(nodo.ToString()) |> ignore
        if rutasNLRRR > 0 then
            let msg = sprintf "NIVEL %d-2 (Simetría NLRRR) Rutas: %d" i rutasNLRRR
            sb.AppendLine(msg) |> ignore
        if rutasNR > 0 then
            let msg = sprintf "NIVEL %d-1 (Simetría NR) Rutas: %d" i rutasNR
            sb.AppendLine(msg) |> ignore
        resumenSimetria.Add(sprintf "NIVEL %-4d NR: %-8d NLRRR: %-8d NL_Duplicate: %-8d Total: %-8d" i rutasNR rutasNLRRR isduplicateL (isduplicateL+rutasNR+rutasNLRRR))
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

    printfn "\nRESUMEN DE SIMETRÍA (Copia de seguridad en consola):"
    for line in resumenSimetria do printfn "%s" line
    0