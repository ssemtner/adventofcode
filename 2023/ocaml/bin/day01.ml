open Core

let part_1_find_digit line =
  let rec aux = function
    | [] -> 0
    | x :: xs ->
      Char.is_digit x
      |> (function
       | true -> Char.to_int x - Char.to_int '0'
       | false -> aux xs)
  in
  aux line
;;

let part_1 lines =
  let rec aux = function
    | [] -> 0
    | x :: xs ->
      (part_1_find_digit (String.to_list x) * 10)
      + part_1_find_digit (String.to_list_rev x)
      + aux xs
  in
  aux lines
;;

let digits =
  [ "one", 1
  ; "two", 2
  ; "three", 3
  ; "four", 4
  ; "five", 5
  ; "six", 6
  ; "seven", 7
  ; "eight", 8
  ; "nine", 9
  ]
;;

let contains_digit str =
  List.find_map digits ~f:(fun (digit, value) ->
    match String.substr_index str ~pattern:digit with
    | Some _ -> Some value
    | None -> None)
;;

let part_2_find_digit line rev =
  let rec aux str = function
    | [] -> 0
    | x :: xs ->
      contains_digit str
      |> (function
       | Some value -> value
       | None ->
         Char.is_digit x
         |> (function
          | true -> Char.to_int x - Char.to_int '0'
          | false ->
            aux
              (match rev with
               | true -> String.append (Char.to_string x) str
               | false -> String.append str (Char.to_string x))
              xs))
  in
  aux "" line
;;

let part_2 lines =
  let rec aux = function
    | [] -> 0
    | x :: xs ->
      (part_2_find_digit (String.to_list x) false * 10)
      + part_2_find_digit (String.to_list_rev x) true
      + aux xs
  in
  aux lines
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day1.txt"
    ~test_path:"../data/sample/day1part1.txt"
    ~test_path_2:"../data/sample/day1part2.txt"
    ~test_1_target:142
    ~test_2_target:281
    ()
  |> Command_unix.run
;;
