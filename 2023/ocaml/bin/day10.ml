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
  | c -> failwithf "Invalid character %c" c ()
;;

let direction_list_to_char = function
  | [ Up; Down ] -> '|'
  | [ Left; Right ] -> '-'
  | [ Up; Left ] -> 'J'
  | [ Up; Right ] -> 'L'
  | [ Down; Left ] -> '7'
  | [ Down; Right ] -> 'F'
  | _ -> failwith "Invalid direction list"
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
  grid.(fst start).(snd start)
  <- [ Up; Down; Left; Right ]
     |> List.filter_map ~f:(fun dir ->
       let row', col' = add_direction start dir in
       try
         possible_directions grid.(row').(col')
         |> List.find ~f:(fun dir' ->
           direction_equals (reverse_direction dir) dir')
         |> function
         | Some _ -> Some dir
         | None -> None
       with
       | _ -> None)
     |> direction_list_to_char;
  let first_moves = possible_directions grid.(fst start).(snd start) in
  let first_move = List.hd_exn first_moves in
  let rec aux acc (row, col) last =
    match row, col with
    | row, col when row = fst start && col = snd start -> acc
    | row, col ->
      let c = grid.(row).(col) in
      let next = next_direction last c in
      let next_pos = add_direction (row, col) next in
      aux (((row, col), c) :: acc) next_pos next
  in
  aux
    [ start, grid.(fst start).(snd start) ]
    (add_direction start first_move)
    first_move
;;

let part_1 lines =
  let grid = parse_grid lines in
  let points = get_points grid in
  Printf.printf "points: %d\n" (List.length points);
  Float.round (List.length points // 2) |> Int.of_float
;;

let expand_grid grid points =
  let new_grid =
    Array.make_matrix
      ~dimx:(Array.length grid * 3)
      ~dimy:(Array.length grid.(0) * 3)
      '.'
  in
  List.iter points ~f:(fun ((i, j), c) ->
    let i' = (i * 3) + 1 in
    let j' = (j * 3) + 1 in
    new_grid.(i').(j') <- '#';
    possible_directions c
    |> List.iter ~f:(fun dir ->
      let i'', j'' = add_direction (i', j') dir in
      new_grid.(i'').(j'') <- '#'));
  new_grid
;;

let flood_fill grid =
  (* Maybe not the best way to copy *)
  let filled_grid =
    Array.make_matrix
      ~dimx:(Array.length grid)
      ~dimy:(Array.length grid.(0))
      '.'
  in
  Array.iteri grid ~f:(fun i row ->
    Array.iteri row ~f:(fun j c -> filled_grid.(i).(j) <- c));
  (* This feels very non functional but seems more efficiant than creating an entire new grid each time *)
  let rec aux pos =
    match pos with
    | row, col when row < 0 || col < 0 -> ()
    | row, col
      when row >= Array.length filled_grid
           || col >= Array.length filled_grid.(0) -> ()
    | row, col when Char.( <> ) filled_grid.(row).(col) '.' -> ()
    | row, col ->
      filled_grid.(row).(col) <- 'O';
      aux (row - 1, col);
      aux (row + 1, col);
      aux (row, col - 1);
      aux (row, col + 1)
  in
  aux (0, 0);
  filled_grid
;;

(* SHOULD BE 541 *)
let part_2 lines =
  let grid = parse_grid lines in
  let points = get_points grid in
  expand_grid grid points
  |> flood_fill
  |> Array.foldi ~init:0 ~f:(fun i acc row ->
    match i % 3 = 1 with
    | false -> acc
    | true ->
      acc + Array.counti row ~f:(fun j c -> j % 3 = 1 && Char.equal c '.'))
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
