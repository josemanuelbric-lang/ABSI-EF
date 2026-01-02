let GenerateParesAstaN (n: int) : List<Set<int>> =
    let todosLosPares = [2..2..n]
    let construirAcumuladas (subconjuntos: List<Set<int>>) (par: int) =
        let ultimoSubconjunto = 
            match subconjuntos with
            | [] -> Set.empty
            | h :: _ -> h
        let nuevoSubconjunto = Set.add par ultimoSubconjunto
        nuevoSubconjunto :: subconjuntos
    todosLosPares
    |> List.fold construirAcumuladas []
    |> List.rev
let CombinacionesAstaN (n: int) : List<Set<int>> =
    let nums = [1..n]
    let generate (currentSets: List<Set<int>>) (item: int) =
        let newSets = 
            currentSets
            |> List.map (fun set -> Set.add item set)
        currentSets @ newSets
    List.fold generate [Set.empty] nums
let posiblesSumas (data: Set<int>) (incluirMismos: bool) : Set<int> =
    let lista = Set.toList data
    let sumasDistintas =
        [
            for i in 0 .. lista.Length - 1 do
            for j in i + 1 .. lista.Length - 1 do
                yield lista.[i] + lista.[j]
        ]
        |> Set.ofList
    if incluirMismos then
        let sumasDeMismos =
            lista
            |> List.map (fun x -> x + x)
            |> Set.ofList
        Set.union sumasDistintas sumasDeMismos
    else
        sumasDistintas
[<EntryPoint>]
let main argv =
    let N_max = 6
    printfn "--- Análisis de Subconjuntos para N_max = %d ---" N_max
    let Pares = GenerateParesAstaN N_max
    printfn "Pares hasta N=%d: %A" N_max Pares
    let Combinaciones = CombinacionesAstaN N_max
    printfn "Total de Subconjuntos Generados: %d" (List.length Combinaciones)
    Combinaciones
        |> List.iter (fun parActual ->
            let combinacionesValidas = 
                posiblesSumas (parActual) (true)
            printfn "Par Objetivo: %A" parActual
            printf " Subconjuntos Válidos (%d en total):[" (combinacionesValidas.Count)
            combinacionesValidas
                |> Set.iter (fun sub -> printf " %A;" sub)
            printfn "]"
        )
    0