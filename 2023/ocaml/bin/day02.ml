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
  Aoc.command
    part_1
    part_2
    ~path:"../data/day2.txt"
    ~test_path:"../data/sample/day2.txt"
    ~test_1_target:8
    ~test_2_target:2286
    ()
  |> Command_unix.run
;;
