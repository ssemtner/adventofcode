open Core

let parse lines =
  let rec aux cur acc = function
    | [] ->
      (match cur with
       | [] -> acc
       | cur -> Array.of_list cur :: acc)
    | "" :: tl -> aux [] (Array.of_list cur :: acc) tl
    | x :: xs ->
      aux
        (cur @ [ String.to_array x |> Array.map ~f:(fun x -> Char.( = ) x '#') ])
        acc
        xs
  in
  aux [] [] lines
;;

let rotate pattern =
  let new_pattern =
    Array.make_matrix
      ~dimx:(Array.length pattern.(0))
      ~dimy:(Array.length pattern)
      false
  in
  Array.iteri pattern ~f:(fun i row ->
    Array.iteri row ~f:(fun j x -> new_pattern.(j).(i) <- x));
  new_pattern
;;

let _print_pattern pattern =
  Array.fold pattern ~init:"" ~f:(fun acc row ->
    acc
    ^ "\n"
    ^ Array.fold row ~init:"" ~f:(fun acc x -> acc ^ if x then "#" else "."))
  |> print_endline
;;

let _print_row row =
  Array.fold row ~init:"" ~f:(fun acc x -> acc ^ if x then "#" else ".")
  |> print_endline
;;

let symetrical_on_row row pattern =
  let rec aux = function
    | i when row + i >= Array.length pattern -> true
    | i when row - i + 1 < 0 -> true
    | i ->
      let top = pattern.(row - i + 1) in
      let bottom = pattern.(row + i) in
      (match Array.equal Bool.equal top bottom with
       | true -> aux (i + 1)
       | false -> false)
  in
  aux 1
;;

let sum_symetrical ~row_f patterns =
  (List.fold patterns ~init:0 ~f:(fun acc pattern ->
     acc
     + Array.foldi pattern ~init:0 ~f:(fun i acc _ ->
       match i, row_f i pattern with
       | i, true when i >= 0 && i < Array.length pattern - 1 -> acc + i + 1
       | _ -> acc))
   * 100)
  + (List.map patterns ~f:rotate
     |> List.fold ~init:0 ~f:(fun acc pattern ->
       acc
       + Array.foldi pattern ~init:0 ~f:(fun i acc _ ->
         match i, row_f i pattern with
         | i, true when i >= 0 && i < Array.length pattern - 1 -> acc + i + 1
         | _ -> acc)))
;;

let part_1 lines =
  let patterns = parse lines in
  sum_symetrical ~row_f:symetrical_on_row patterns
;;

(* I just made a new func because I don't want to deal with a bunch of ifs *)
let symetrical_on_row_with_smudge row pattern =
  let rec aux smudged i =
    match i with
    | i when row + i >= Array.length pattern -> smudged
    | i when row - i + 1 < 0 -> smudged
    | i ->
      let top = pattern.(row - i + 1) in
      let bottom = pattern.(row + i) in
      (match
         ( Array.zip_exn top bottom
           |> Array.count ~f:(fun (a, b) -> Bool.( <> ) a b)
         , smudged )
       with
       | 0, _ -> aux smudged (i + 1)
       | 1, false -> aux true (i + 1)
       | _ -> false)
  in
  aux false 1
;;

let part_2 lines =
  let patterns = parse lines in
  sum_symetrical ~row_f:symetrical_on_row_with_smudge patterns
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day13.txt"
    ~test_path:"../data/sample/day13.txt"
    ~test_1_target:405
    ~test_2_target:400
    ()
  |> Command_unix.run
;;
