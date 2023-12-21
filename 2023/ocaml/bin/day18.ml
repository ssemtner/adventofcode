open Core

let parse_line line =
  let direction, length, color =
    String.split line ~on:' '
    |> function
    | [ direction; length; color ] -> direction, length, color
    | _ -> failwith "invalid line"
  in
  let color =
    String.chop_suffix_exn color ~suffix:")"
    |> String.chop_prefix_exn ~prefix:"(#"
  in
  Char.of_string direction, Int.of_string length, color
;;

(* This is fancy math that I found online *)
let calculate_area corners =
  let l, r =
    List.fold2_exn
      corners
      (List.tl_exn corners @ [ List.hd_exn corners ])
      ~init:(0, 0)
      ~f:(fun (l, r) (x1, y1) (x2, y2) -> l + (x1 * y2), r + (y1 * x2))
  in
  let area = abs (l - r) / 2 in
  let perimiter =
    List.fold2_exn
      (List.drop_last_exn corners)
      (List.tl_exn corners)
      ~init:0
      ~f:(fun acc (x1, y1) (x2, y2) -> acc + abs (x2 - x1) + abs (y2 - y1))
  in
  area + (perimiter / 2) + 1
;;

let steps_to_corners steps =
  List.fold
    (* adding another step to make sure the last position is counted *)
    (steps @ [ 'U', 0, "" ])
    ~init:([], (0, 0))
    ~f:(fun (acc, (x, y)) (direction, length, _color) ->
      let acc = (x, y) :: acc in
      match direction with
      | 'U' -> acc, (x, y + length)
      | 'D' -> acc, (x, y - length)
      | 'L' -> acc, (x - length, y)
      | 'R' -> acc, (x + length, y)
      | _ -> failwith "invalid direction")
  |> fst
;;

let part_1 lines =
  List.map lines ~f:parse_line |> steps_to_corners |> calculate_area
;;

let part_2 lines =
  List.map lines ~f:(fun line ->
    let _, _, color = parse_line line in
    let direction =
      match String.get color (String.length color - 1) with
      | '0' -> 'R'
      | '1' -> 'D'
      | '2' -> 'L'
      | '3' -> 'U'
      | _ -> failwith "invalid direction code"
    in
    let length =
      "0x" ^ (color |> String.sub ~pos:0 ~len:(String.length color - 1))
      |> Int.of_string
    in
    direction, length, color)
  |> steps_to_corners
  |> calculate_area
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day18.txt"
    ~test_path:(Some "../data/sample/day18.txt")
    ~test_1_target:(Some 62)
    ~test_2_target:(Some 952408144115)
    ()
  |> Command_unix.run
;;
