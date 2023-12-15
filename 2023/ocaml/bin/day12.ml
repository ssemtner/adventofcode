open Core

let parse_row line =
  let split = String.split line ~on:' ' in
  let springs = List.hd_exn split |> String.to_list in
  let counts =
    List.nth_exn split 1 |> String.split ~on:',' |> List.map ~f:Int.of_string
  in
  springs, counts
;;

let valid counts springs =
  let rec aux acc springs counts =
    match springs, counts with
    | [], [] -> true
    | _, [] -> List.for_all springs ~f:(Char.( <> ) '#')
    | [], _ ->
      (match acc = List.hd_exn counts && List.length counts = 1 with
       | true -> true
       | _ -> false)
    | s :: springs, c :: ctail ->
      (match s with
       | '.' ->
         (match acc = c with
          | false when acc = 0 -> aux 0 springs counts
          | true -> aux 0 springs ctail
          | false -> false)
       | '#' -> aux (acc + 1) springs counts
       | _ -> failwithf "invalid spring %s" (Char.to_string s) ())
  in
  aux 0 springs counts
;;

let _contains_unknown str = List.exists str ~f:(fun x -> Char.equal x '?')

let all_combinations springs =
  let rec aux acc = function
    | [] ->
      (* Printf.printf "returning acc: %s\n" (String.of_char_list acc); *)
      [ acc ]
    | x :: xs ->
      (* Printf.printf "acc: %s\n" (String.of_char_list acc); *)
      (match x with
       | '?' ->
         let p1 = aux [] ('.' :: xs) in
         let p2 = aux [] ('#' :: xs) in
         p1 @ p2 |> List.map ~f:(fun a -> acc @ a)
       | _ ->
         (* Printf.printf "adding %s to acc\n" (Char.to_string x); *)
         let acc' = acc @ [ x ] in
         aux acc' xs)
  in
  aux [] springs
;;

let part_1 lines =
  let rows = List.map lines ~f:parse_row in
  List.fold rows ~init:0 ~f:(fun acc (springs, counts) ->
    all_combinations springs
    |> List.count ~f:(fun springs -> valid counts springs)
    |> ( + ) acc)
;;

let unfold_row row =
  let rec repeat_springs n l =
    match n with
    | 1 -> l
    | _ -> l @ [ '?' ] @ repeat_springs (n - 1) l
  in
  let rec repeat_counts n l =
    match n with
    | 0 -> []
    | _ -> l @ repeat_counts (n - 1) l
  in
  repeat_springs 5 (fst row), repeat_counts 5 (snd row)
;;

module M = Map.Make (struct
    type t = int * int * int [@@deriving sexp, compare]
  end)

let ways (springs, counts) =
  let dp = ref M.empty in
  let rec aux springs counts i bi current =
    let key = i, bi, current in
    match Map.find !dp key with
    | Some v -> v
    | None ->
      (match List.length springs = i with
       | true ->
         (match List.length counts, current with
          | len, 0 when len = bi -> 1
          | len, current when len = bi + 1 && current = List.nth_exn counts bi
            -> 1
          | _ -> 0)
       | false ->
         let ans =
           [ '.'; '#' ]
           |> List.fold ~init:0 ~f:(fun acc c ->
             match List.nth_exn springs i with
             | ch when Char.( = ) ch c || Char.( = ) ch '?' ->
               (match
                  ( c
                  , current
                  , bi < List.length counts && List.nth_exn counts bi = current
                  )
                with
                | '.', 0, _ -> acc + aux springs counts (i + 1) bi 0
                | '.', current, true when current > 0 ->
                  acc + aux springs counts (i + 1) (bi + 1) 0
                | '#', _, _ -> acc + aux springs counts (i + 1) bi (current + 1)
                | _ -> acc)
             | _ -> acc)
         in
         dp := Map.set !dp ~key ~data:ans;
         ans)
  in
  let ans = aux springs counts 0 0 0 in
  ans
;;

let part_2 lines =
  let rows = List.map lines ~f:(fun row -> parse_row row |> unfold_row) in
  List.map rows ~f:(fun row -> ways row) |> List.fold ~init:0 ~f:( + )
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day12.txt"
    ~test_path:
      (Some "/Users/sjsem/Developer/adventofcode/2023/data/sample/day12.txt")
    ~test_1_target:(Some 21)
    ~test_2_target:(Some 525152)
    ()
  |> Command_unix.run
;;
