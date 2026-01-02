open System
open System.Collections.Generic
open System.Text
open System.Diagnostics

type NodoCollatz = {
    Desplazamiento: bigint
    Progresion: bigint
    Ruta: string
    Nivel: int
    EsDuplicado: bool
} with
    override x.ToString() = 
        let mark = if x.EsDuplicado then "#" else "*"
        sprintf "%-32s (>%AN%A%s)" x.Ruta x.Desplazamiento x.Progresion mark

let collatz (n: bigint) =
    if n % 2I = 0I then (n / 2I, "R")
    else (3I * n + 1I, "L")

let detectarPatron (valores: bigint list) =
    match valores with
    | v0 :: v1 :: _ ->
        let salto = v1 - v0
        let rec check (list: bigint list) =
            match list with
            | a :: b :: rest -> if b - a = salto then check (b :: rest) else false
            | _ -> true
        if check valores then Some(v0, salto) else None
    | _ -> None

let generarArbol (nodoInicio: NodoCollatz) (niveles: int) (semillasCount: int) (seconMode: bool) =
    let arbol = List<Dictionary<string, NodoCollatz>>()
    arbol.Add(Dictionary<string, NodoCollatz>(dict [("N", nodoInicio)]))
    
    let historialPatrones = HashSet<bigint * bigint>()
    let historialResultados = Dictionary<bigint * bigint, (bigint * bigint) option * (bigint * bigint) option>()

    for q1 in 0 .. niveles - 1 do
        let actual = arbol.[q1]
        let proximo = Dictionary<string, NodoCollatz>()

        for kvp in actual do
            let ruta, nodo = kvp.Key, kvp.Value
            let llave = (nodo.Desplazamiento, nodo.Progresion)

            let procesarFunc (res: (bigint * bigint) option) (letra: string) =
                match res with
                | Some (d, p) ->
                    let isDup = historialPatrones.Contains((d, p))
                    if not isDup then historialPatrones.Add((d, p)) |> ignore
                    proximo.[ruta + letra] <- { Desplazamiento = d; Progresion = p; Ruta = ruta + letra; Nivel = q1 + 1; EsDuplicado = isDup }
                | None -> ()
            let d, p = llave
            if seconMode then
                match (d % 2I = 0I, p % 2I = 0I) with
                | (true, true)   ->
                    procesarFunc (Some(d / 2I, p / 2I))  "R"
                | (true, false)  ->
                    let newDL = (d * 3I) + (p * 3I) + 1I
                    let newPL= (p * 3I) * 2I
                    procesarFunc (Some( newDL, newPL))  "L"
                    let newDR = d / 2I
                    let newPR= p
                    procesarFunc (Some( newDR, newPR))  "R"
                | (false, true)  ->
                    printfn "IP"
                | (false, false) ->
                    let newDL= (d*3I) + 1I
                    let newPL=(p * 3I) * 2I
                    procesarFunc (Some( newDL, newPL))  "L"
                    let newDR=(d+p)/ 2I
                    let newPR= p
                    procesarFunc (Some( newDR, newPR))  "R"
            else
                match historialResultados.TryGetValue(llave) with
                | true, (resR, resL) ->
                    procesarFunc resR "R"
                    procesarFunc resL "L"
                | _ ->
                    let mutable rVals = []
                    let mutable lVals = []
                    for i in 0 .. semillasCount - 1 do
                        let s = nodo.Progresion * bigint(i) + nodo.Desplazamiento
                        let v, b = collatz s
                        if b = "R" then rVals <- v :: rVals else lVals <- v :: lVals
                
                    let resR = detectarPatron (List.rev rVals)
                    let resL = detectarPatron (List.rev lVals)
                    historialResultados.[llave] <- (resR, resL)
                    procesarFunc resR "R"
                    procesarFunc resL "L"
        arbol.Add(proximo)
    arbol
let revisarIsDuplicateMal (arbol: List<Dictionary<string, NodoCollatz>>) (objetivo: bigint * bigint) (nivelFallo: int) =
    let d_obj, p_obj = objetivo
    printfn "--- AUDITORÍA DE DUPLICADO para (%A, %A) ---" d_obj p_obj
    let mutable encontrado = false
    for i in 0 .. nivelFallo do
        let dictNivel = arbol.[i]
        for kvp in dictNivel do
            let nodo = kvp.Value
            if nodo.Desplazamiento = d_obj && nodo.Progresion = p_obj then
                if not encontrado then
                    printfn "ORIGINAL ENCONTRADO en Nivel %d, Ruta: %s" i nodo.Ruta
                    encontrado <- true
                else
                    printfn "OTRA APARICIÓN en Nivel %d, Ruta: %s" i nodo.Ruta
    if not encontrado then 
        printfn "Raro: El patrón no existe en niveles anteriores. El 'true' podría estar mal."
    printfn "-------------------------------------------"
let compararArboles (arbol1: List<Dictionary<string, NodoCollatz>>) (arbol2: List<Dictionary<string, NodoCollatz>>) =
    if arbol1.Count <> arbol2.Count then
        printfn "Fallo: Los árboles tienen diferentes niveles (%d vs %d)" arbol1.Count arbol2.Count
        false
    else
        let mutable todoEsIgual = true
        
        for i in 0 .. arbol1.Count - 1 do
            let dict1 = arbol1.[i]
            let dict2 = arbol2.[i]
            
            if dict1.Count <> dict2.Count then
                printfn "Fallo en Nivel %d: Diferente número de nodos (%d vs %d)" i dict1.Count dict2.Count
                todoEsIgual <- false
            else
                let llaves1 = dict1.Keys |> Seq.sort |> Seq.toList
                let llaves2 = dict2.Keys |> Seq.sort |> Seq.toList
                
                if llaves1 <> llaves2 then
                    printfn "Fallo en Nivel %d: Las rutas (llaves) no coinciden" i
                    todoEsIgual <- false
                else
                    for ruta in llaves1 do
                        let nodo1 = dict1.[ruta]
                        let nodo2 = dict2.[ruta]
                        if nodo1 <> nodo2 then
                            printfn "Fallo en Nivel %d, Ruta %s: Los datos del nodo son distintos" i ruta
                            printfn "nodo1 %A" nodo1
                            printfn "nodo2 %A" nodo2
                            
                            printfn "zzzzzzzzzzzz"
                            revisarIsDuplicateMal arbol1 (nodo1.Desplazamiento, nodo1.Progresion) nodo2.Nivel
                            printfn "zzzzzzzzzzzz"
                            todoEsIgual <- false
        todoEsIgual

[<EntryPoint>]
let main argv =
    let nivelesTarget = 15
    let semillas = 32
    let nodoInicial = { Desplazamiento = 1I; Progresion = 1I; Ruta = "N"; Nivel = 0; EsDuplicado = false }

    // Benchmark de tiempo por nivel (como tu bucle de Python)
    //let sw = Stopwatch.StartNew()
    //let res = generarArbol nodoInicial nivelesTarget semillas
    //sw.Stop()
    //printfn "%d %f" nivelesTarget sw.Elapsed.TotalSeconds

    let finalRes = generarArbol nodoInicial nivelesTarget semillas true
    let finalRes2 = generarArbol nodoInicial nivelesTarget semillas false

    let sonIguales = compararArboles finalRes finalRes2

    //Environment.Exit(0)
    let sb = StringBuilder()
    let resumenSimetria = List<string>()

    for i in 0 .. finalRes.Count - 1 do
        sb.AppendLine(sprintf "\nNIVEL %d %s" i (String('-', 50))) |> ignore
        let nivel = finalRes.[i]
        let mutable rutasR = 0
        
        // Ordenar llaves para consistencia
        let sortedKeys = nivel.Keys |> Seq.sort
        for ruta in sortedKeys do
            let nodo = nivel.[ruta]
            if ruta.StartsWith("NR") then
                rutasR <- rutasR + 1
            else
                sb.AppendLine(nodo.ToString()) |> ignore
        
        if rutasR > 0 then
            let msg = sprintf "NIVEL %d-1 (Simetría R) Rutas: %d" i rutasR
            sb.AppendLine(msg) |> ignore
            resumenSimetria.Add(sprintf "NIVEL%d %16d" i rutasR)
    Console.Write(sb.ToString())
    printfn "\nRESUMEN DE SIMETRÍA:"
    for line in resumenSimetria do printfn "%s" line
    0