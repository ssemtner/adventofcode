open Core

let parse_cards lines =
  List.map lines ~f:(fun line ->
    let parts =
      String.split (List.nth_exn (String.split line ~on:':') 1) ~on:'|'
    in
    let split_cards str =
      List.filter_map (String.split str ~on:' ') ~f:Int.of_string_opt
    in
    split_cards (List.hd_exn parts), split_cards (List.nth_exn parts 1))
;;

let card_matches cards =
  List.map cards ~f:(fun (winning_cards, cards) ->
    List.filter cards ~f:(fun card -> List.mem winning_cards card ~equal:( = ))
    |> List.length)
;;

let part_1 lines =
  let cards = parse_cards lines in
  card_matches cards
  |> List.map ~f:(function
    | 0 -> 0
    | n -> Int.pow 2 (n - 1))
  |> List.fold ~init:0 ~f:( + )
;;

let part_2 lines =
  let cards = parse_cards lines in
  let values = card_matches cards |> List.to_array in
  let counts = Array.create ~len:(List.length cards) 1 in
  let rec aux counts = function
    | i when i = Array.length counts -> counts
    | i ->
      let num_to_increase = values.(i) in
      let increase_by = counts.(i) in
      let counts' =
        (* Doing this with mapi means that i is never out of bounds *)
        Array.mapi counts ~f:(fun i' count ->
          match i' with
          | i' when i' > i && i' < i + num_to_increase + 1 ->
            count + increase_by
          | _ -> count)
      in
      aux counts' (i + 1)
  in
  aux counts 0 |> Array.fold ~init:0 ~f:( + )
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day4.txt"
    ~test_path:(Some "../data/sample/day4.txt")
    ~test_1_target:(Some 13)
    ~test_2_target:(Some 30)
    ()
  |> Command_unix.run
;;
