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
  let test_part_1_lines = Aoc.read_lines "../data/sample/day1part1.txt" in
  let test_part_2_lines = Aoc.read_lines "../data/sample/day1part2.txt" in
  let lines = Aoc.read_lines "../data/day1.txt" in
  let part_1_test = part_1 test_part_1_lines in
  if part_1_test = 142
  then Printf.printf "Test 1 passed\nPart 1: %d\n" (part_1 lines)
  else Printf.printf "Test 1 failed\n";
  let part_2_test = part_2 test_part_2_lines in
  if part_2_test = 281
  then Printf.printf "Test 2 passed\nPart 2: %d\n" (part_2 lines)
  else Printf.printf "Test 2 failed\nExpected: %d, Got: %d\n" 281 part_2_test
;;
