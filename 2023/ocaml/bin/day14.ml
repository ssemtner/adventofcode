open Core

let _print_grid grid =
  Printf.printf
    "%s\n"
    (String.concat ~sep:"\n" (List.map grid ~f:String.of_char_list))
;;

let transpose list =
  let rec aux = function
    | [] -> []
    | [] :: xss -> aux xss
    | (x :: xs) :: xss ->
      (x :: List.map ~f:List.hd_exn xss)
      :: aux (xs :: List.map ~f:List.tl_exn xss)
  in
  aux list
;;

let rotate grid = transpose grid |> List.map ~f:(fun row -> List.rev row)

(* tilts grid west *)
let tilt grid =
  let rec aux run cur acc row =
    match row with
    | [] -> acc @ cur
    | 'O' :: tl -> aux (run + 1) (cur @ [ 'O' ]) acc tl
    | '#' :: tl -> aux 0 [] (acc @ cur @ [ '#' ]) tl
    | _ :: tl -> aux run ('.' :: cur) acc tl
  in
  List.map grid ~f:(fun row -> aux 0 [] [] row)
;;

let cycle grid =
  let rec aux grid = function
    | 0 -> grid
    | n -> aux (rotate grid |> tilt) (n - 1)
  in
  aux grid 4
;;

let hash grid =
  List.map grid ~f:(fun row -> String.of_char_list row) |> String.concat ~sep:""
;;

let count_load grid =
  List.fold grid ~init:0 ~f:(fun acc row ->
    List.foldi row ~init:acc ~f:(fun i acc c ->
      match c with
      | 'O' -> acc + (i + 1)
      | _ -> acc))
;;

let part_1 lines =
  List.map lines ~f:String.to_list |> rotate |> tilt |> count_load
;;

let part_2 lines =
  let rec aux i prev_cycles states grid =
    match Map.find prev_cycles (hash grid) with
    | Some prev_i ->
      let period = i - prev_i in
      printf "cycle detected at i=%d, period is %d\n" i period;
      let end_state_idx = ((1000000000 - 1 - prev_i) mod period) + prev_i in
      (* I have no idea where the +1 comes from but it works... *)
      let end_state = Map.find_exn states (end_state_idx + 1) in
      end_state |> rotate |> count_load
    | None ->
      let prev_cycles' = Map.set prev_cycles ~key:(hash grid) ~data:i in
      let states' = Map.set states ~key:i ~data:grid in
      aux (i + 1) prev_cycles' states' (cycle grid)
  in
  aux
    0
    (Map.empty (module String))
    (Map.empty (module Int))
    (List.map lines ~f:String.to_list)
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day14.txt"
    ~test_path:(Some "../data/sample/day14.txt")
    ~test_1_target:(Some 136)
    ~test_2_target:(Some 64)
    ()
  |> Command_unix.run
;;
