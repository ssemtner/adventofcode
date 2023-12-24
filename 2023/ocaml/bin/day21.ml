open Core

module Plot = struct
  type t =
    | Start
    | Rock
    | Reachable of int
  [@@deriving equal]
end

let parse lines =
  List.foldi
    lines
    ~init:(Set.empty (module Aoc.Point), (0, 0))
    ~f:(fun i acc line ->
      List.foldi (String.to_list line) ~init:acc ~f:(fun j (rocks, start) c ->
        match c with
        | '#' -> Set.add rocks (i, j), start
        | 'S' -> rocks, (i, j)
        | _ -> rocks, start))
;;

let _print_grid rocks points lines =
  List.iteri lines ~f:(fun i line ->
    List.iteri (String.to_list line) ~f:(fun j c ->
      match Set.mem rocks (i, j), Set.mem points (i, j) with
      | false, false -> printf "%c" c
      | true, false -> printf "#"
      | false, true -> printf "O"
      | true, true -> printf "*");
    printf "\n");
  printf "\n"
;;

let part_1 steps lines =
  let rocks, start = parse lines in
  let rec aux rocks points steps =
    if steps <= 0
    then points
    else (
      let points =
        Set.fold
          points
          ~init:(Set.empty (module Aoc.Point))
          ~f:(fun acc (x, y) ->
            [ -1, 0; 1, 0; 0, -1; 0, 1 ]
            |> List.fold ~init:acc ~f:(fun acc (dx, dy) ->
              let x' = dx + x
              and y' = dy + y in
              if Set.mem rocks (x', y')
                 || x' < 0
                 || y' < 0
                 || x' >= List.length lines
                 || y' >= String.length (List.hd_exn lines)
              then acc
              else Set.add acc (x', y')))
      in
      aux rocks points (steps - 1))
  in
  let points = aux rocks (Set.of_list (module Aoc.Point) [ start ]) steps in
  Set.length points
;;

let part_2 steps lines =
  let n = List.length lines in
  (* create larger grid *)
  let grid, start =
    List.foldi
      lines
      ~init:(Map.empty (module Aoc.Point), (0, 0))
      ~f:(fun i acc line ->
        String.foldi line ~init:acc ~f:(fun j (map, start) c ->
          let start = if Char.(c = 'S') then i + n, j + n else start in
          ( List.range 0 3
            |> List.fold ~init:map ~f:(fun map a ->
              List.range 0 3
              |> List.fold ~init:map ~f:(fun map b ->
                Map.add_exn
                  map
                  ~key:(i + (a * n), j + (b * n))
                  ~data:
                    (match c, (a, b) with
                     | 'S', (a, b) when a <> 1 && b <> 1 -> '.'
                     | c, _ -> c)))
          , start )))
  in
  let queue = Queue.create () in
  Queue.enqueue queue start;
  let rec aux distances visited =
    match Queue.dequeue queue with
    | None -> distances, visited
    | Some (x, y) ->
      let distances, visited =
        [ -1, 0; 1, 0; 0, -1; 0, 1 ]
        |> List.fold
             ~init:(distances, visited)
             ~f:(fun (distances, visited) (dx, dy) ->
               let x' = dx + x
               and y' = dy + y in
               if x' < 0
                  || y' < 0
                  || x' >= n * 3
                  || y' >= n * 3
                  || Set.mem visited (x', y')
                  || Map.find_exn grid (x', y') |> Char.equal '#'
               then distances, visited
               else (
                 Queue.enqueue queue (x', y');
                 ( Map.set
                     distances
                     ~key:(x', y')
                     ~data:
                       (Map.find distances (x, y)
                        |> function
                        | None -> 1
                        | Some v -> v + 1)
                 , Set.add visited (x', y') )))
      in
      aux distances visited
  in
  let distances, visited =
    aux (Map.empty (module Aoc.Point)) (Set.empty (module Aoc.Point))
  in
  (* This took 14 seconds with map and fold *)
  (* let dp =
     List.range ~stride:(-1) steps (-1)
     |> List.fold
     ~init:(Map.empty (module Int))
     ~f:(fun acc i ->
     Map.add_exn
     acc
     ~key:i
     ~data:
     ((i % 2 = steps % 2 |> Bool.to_int)
     + (2
       * (Map.find acc (i + n)
       |> function
       | None -> 0
       | Some x -> x))

     - (Map.find acc (i + (2 * n))
       |> function
       | None -> 0
       | Some x -> x)))
       in *)

  (* But only 2 seconds with an array lol *)
  (* (idk how to use functional stuff efficiently yet) *)
  let dp = Array.create ~len:(steps + 1000) 0 in
  List.range ~stride:(-1) steps (-1)
  |> List.iter ~f:(fun i ->
    dp.(i)
    <- (i % 2 = steps % 2 |> Bool.to_int) + (2 * dp.(i + n)) - dp.(i + (2 * n)));
  List.range 0 (n * 3)
  |> List.fold ~init:0 ~f:(fun acc i ->
    List.range 0 (n * 3)
    |> List.fold ~init:acc ~f:(fun acc j ->
      if Set.mem visited (i, j)
      then (
        let dx = i - fst start
        and dy = j - snd start in
        if dx >= -n && dx < n && dy >= -n && dy < n
        then (Map.find_exn distances (i, j) |> Array.get dp) + acc
        else acc)
      else acc))
;;

let () =
  Aoc.command
    (part_1 64)
    (part_2 26501365)
    ~test_part_1:(part_1 6)
    ~test_part_2:(part_2 1180148)
    ~path:"../data/day21.txt"
    ~test_path:"../data/sample/day21.txt"
    ~test_path_2:"../data/sample/day21part2.txt"
    ~test_1_target:16
    ~test_2_target:1185525742508
    ()
  |> Command_unix.run
;;
