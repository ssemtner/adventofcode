open Core

type direction =
  | Up
  | Down
  | Left
  | Right

let direction_equals a b =
  match a, b with
  | Up, Up -> true
  | Down, Down -> true
  | Left, Left -> true
  | Right, Right -> true
  | _ -> false
;;

(* Returns direction in (row, col) format *)
let get_direction = function
  | Up -> -1, 0
  | Down -> 1, 0
  | Left -> 0, -1
  | Right -> 0, 1
;;

let possible_directions = function
  | '|' -> [ Up; Down ]
  | '-' -> [ Left; Right ]
  | 'J' -> [ Up; Left ]
  | 'L' -> [ Up; Right ]
  | '7' -> [ Down; Left ]
  | 'F' -> [ Down; Right ]
  | _ -> failwith "Invalid character"
;;

let reverse_direction = function
  | Up -> Down
  | Down -> Up
  | Left -> Right
  | Right -> Left
;;

let next_direction prev c =
  let reversed = reverse_direction prev in
  let possible = possible_directions c in
  List.filter possible ~f:(fun dir -> not (direction_equals dir reversed))
  |> List.hd_exn
;;

let _print_grid grid =
  Array.map grid ~f:(fun row ->
    Array.map row ~f:(fun c -> Char.to_string c)
    |> Array.to_list
    |> String.concat ~sep:"")
  |> Array.to_list
  |> String.concat ~sep:"\n"
  |> Printf.printf "%s\n"
;;

let parse_grid lines =
  Array.of_list_map lines ~f:(fun line -> Array.of_list (String.to_list line))
;;

let find_start grid =
  List.filter_mapi (Array.to_list grid) ~f:(fun row_idx row ->
    List.filter_mapi (Array.to_list row) ~f:(fun col_idx c ->
      match c with
      | 'S' -> Some (row_idx, col_idx)
      | _ -> None)
    |> List.hd)
  |> List.hd_exn
;;

let add_direction (row, col) dir =
  let row', col' = get_direction dir in
  row + row', col + col'
;;

let get_points grid =
  let start = find_start grid in
  let first_move =
    [ Up; Down; Left; Right ]
    |> List.filter_map ~f:(fun dir ->
      let row', col' = add_direction start dir in
      try
        possible_directions grid.(row').(col')
        |> List.find ~f:(fun dir' ->
          not (direction_equals (reverse_direction dir) dir'))
      with
      | _ -> None)
  in
  let last = List.hd_exn first_move in
  let rec aux acc (row, col) last =
    match grid.(row).(col) with
    | 'S' -> acc
    | c ->
      let next = next_direction last c in
      let next_pos = add_direction (row, col) next in
      aux (next_pos :: acc) next_pos next
  in
  aux [] (add_direction start last) last
;;

let part_1 lines =
  let grid = parse_grid lines in
  let points = get_points grid in
  Float.round (List.length points // 2) |> Int.of_float
;;

let count_inversions line j =
  (Array.slice line 0 (j + 1) |> Array.count ~f:(fun x -> x))
  +
  match j, line with
  | 0, line when line.(0) -> 1
  | _ -> 0
;;

(* SHOULD BE 541 *)
let part_2 lines =
  let grid = parse_grid lines in
  let points = get_points grid in
  let inversions_grid =
    Array.make_matrix
      ~dimx:(List.length lines)
      ~dimy:(String.length (List.hd_exn lines))
      false
  in
  List.iter points ~f:(fun (row, col) ->
    match grid.(row).(col) with
    | 'J' | 'L' | '|' -> inversions_grid.(row).(col) <- true
    | _ -> ());
  Array.map inversions_grid ~f:(fun row ->
    Array.map row ~f:(fun c -> if c then "|" else ".")
    |> Array.to_list
    |> String.concat ~sep:"")
  |> Array.to_list
  |> String.concat ~sep:"\n"
  |> Printf.printf "%s\n";
  Array.foldi inversions_grid ~init:0 ~f:(fun i acc row ->
    Array.foldi row ~init:acc ~f:(fun j acc' _ ->
      match
        List.exists points ~f:(fun (row', col') -> row' = i && col' = j)
      with
      | true -> acc'
      | false ->
        (match Int.rem (count_inversions row j) 2 with
         | 0 -> acc'
         | _ -> acc' + 1)))
;;

(* print grid *)

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day10.txt"
    ~test_path:(Some "../data/sample/day10.txt")
    ~test_path_2:(Some "../data/sample/day10part2.txt")
    ~test_1_target:(Some 8)
    ~test_2_target:(Some 10)
    ()
  |> Command_unix.run
;;
