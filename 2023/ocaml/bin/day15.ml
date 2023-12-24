open Core

let hash str =
  let rec aux acc = function
    | [] -> acc
    | x :: xs -> aux ((acc + Char.to_int x) * 17 % 256) xs
  in
  aux 0 (String.to_list str)
;;

let part_1 lines =
  List.hd_exn lines
  |> String.split ~on:','
  |> List.fold ~init:0 ~f:(fun acc x -> acc + hash x)
;;

let part_2 lines =
  let instructions = List.hd_exn lines |> String.split ~on:',' in
  let rec do_init_sequence boxes = function
    | [] -> boxes
    | x :: xs ->
      let parts = String.split_on_chars x ~on:[ '-'; '=' ] in
      let label = List.hd_exn parts in
      let box_id = hash label in
      let box =
        match Map.find boxes box_id with
        | Some box -> box
        | None -> []
      in
      let box' =
        match String.contains x '-' with
        | true ->
          List.filter box ~f:(fun (label', _) -> String.(label <> label'))
        | false ->
          let focal_length = List.nth_exn parts 1 |> Int.of_string in
          (match
             List.find box ~f:(fun (label', _) -> String.(label = label'))
           with
           | Some _ ->
             List.map box ~f:(fun (label', focal_length') ->
               match String.(label = label') with
               | true -> label, focal_length
               | false -> label', focal_length')
           | None -> box @ [ label, focal_length ])
      in
      do_init_sequence (Map.set boxes ~key:box_id ~data:box') xs
  in
  let boxes = do_init_sequence (Map.empty (module Int)) instructions in
  Map.fold boxes ~init:0 ~f:(fun ~key:box_idx ~data:box acc ->
    List.foldi box ~init:acc ~f:(fun i acc (_label, focal_length) ->
      acc + ((box_idx + 1) * (i + 1) * focal_length)))
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day15.txt"
    ~test_path:"../data/sample/day15.txt"
    ~test_1_target:1320
    ~test_2_target:145
    ()
  |> Command_unix.run
;;
