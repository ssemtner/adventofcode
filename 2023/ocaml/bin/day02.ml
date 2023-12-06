open Core

let parse_draws line =
  List.map
    (String.split ~on:';' (List.nth_exn (String.split ~on:':' line) 1))
    ~f:(fun line ->
      List.fold
        ~init:(Map.empty (module String))
        (String.split ~on:',' line)
        ~f:(fun acc pair ->
          let split = String.split ~on:' ' (String.strip pair) in
          Map.set
            acc
            ~key:(List.nth_exn split 1)
            ~data:(int_of_string (List.nth_exn split 0))))
;;

let limits =
  Map.of_alist_exn (module String) [ "red", 12; "green", 13; "blue", 14 ]
;;

let possible_draw draws =
  List.for_all draws ~f:(fun draw ->
    Map.for_alli draw ~f:(fun ~key ~data ->
      match Map.find limits key with
      | Some limit -> data <= limit
      | None -> false))
;;

let part_1 lines =
  let rec aux n = function
    | [] -> 0
    | x :: xs ->
      (match possible_draw (parse_draws x) with
       | true -> n + 1 + aux (n + 1) xs
       | false -> aux (n + 1) xs)
  in
  aux 0 lines
;;

let minimum_bag draws =
  (* I have no clue how to not hardcode these 3. I have spent hours *)
  List.fold [ "red"; "green"; "blue" ] ~init:1 ~f:(fun acc key ->
    let maximum =
      List.fold draws ~init:0 ~f:(fun acc draw ->
        match Map.find draw key with
        | Some value -> max acc value
        | None -> acc)
    in
    acc * maximum)
;;

let part_2 lines =
  let rec aux = function
    | [] -> 0
    | x :: xs -> minimum_bag (parse_draws x) + aux xs
  in
  aux lines
;;

let () =
  let test_lines = Aoc.read_lines "../data/sample/day2.txt" in
  let lines = Aoc.read_lines "../data/day2.txt" in
  let part_1_test = part_1 test_lines in
  if part_1_test = 8
  then Printf.printf "Test 1 passed\nPart 1: %d\n" (part_1 lines)
  else Printf.printf "Test 1 failed\nExpected: %d, Got: %d\n" 8 part_1_test;
  let part_2_test = part_2 test_lines in
  if part_2_test = 2286
  then Printf.printf "Test 2 passed\nPart 2: %d\n" (part_2 lines)
  else Printf.printf "Test 2 failed\nExpected: %d, Got: %d\n" 2286 part_2_test
;;
