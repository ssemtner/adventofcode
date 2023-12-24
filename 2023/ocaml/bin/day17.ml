open Core

let parse lines =
  Array.of_list_map lines ~f:(fun line ->
    line
    |> String.to_array
    |> Array.map ~f:(fun c -> String.of_char c |> Int.of_string))
;;

(* Love to implement my own data structures :) *)
(* CSE 12 here I come *)
(* http://typeocaml.com/2015/03/12/heap-leftist-tree/ *)
module Leftist = struct
  type 'a t =
    | Leaf
    | Node of 'a t * 'a * 'a t * int

  let empty = Leaf
  let singleton k = Node (Leaf, k, Leaf, 1)

  let rank = function
    | Leaf -> 0
    | Node (_, _, _, r) -> r
  ;;

  (* O(log n) *)
  let rec merge t1 t2 =
    match t1, t2 with
    | Leaf, t | t, Leaf -> t
    (* This is kinda gross because the type is hardcoded *)
    (* I have no clue how to do polymorphism in ocaml *)
    | Node (l, k1, r, _), Node (_, k2, _, _) ->
      if let _, _, _, v1 = k1
         and _, _, _, v2 = k2 in
         v1 > v2
      then merge t2 t1
      else (
        let merged = merge r t2 in
        let rank_left = rank l
        and rank_right = rank merged in
        if rank_left >= rank_right
        then Node (l, k1, merged, rank_right + 1)
        else Node (merged, k1, l, rank_left + 1))
  ;;

  (* O(log n) *)
  let insert t x = merge (singleton x) t

  (* O(1) *)
  let get_min = function
    | Leaf -> None
    | Node (_, k, _, _) -> Some k
  ;;

  (* O (log n) *)
  let delete_min = function
    | Leaf -> Leaf
    | Node (l, _, r, _) -> merge l r
  ;;
end

module State = struct
  module T = struct
    type t = (int * int) * int * (int * int) [@@deriving hash, compare, sexp_of]
  end

  include T
  include Comparator.Make (T)
end

let min_heat_loss grid min_run max_run =
  let rec aux tree ~set =
    match Leftist.get_min tree with
    | None -> failwith "No solution"
    | Some ((i, j), _, _, heat_loss)
      when i = Array.length grid - 1 && j = Array.length grid.(0) - 1 ->
      heat_loss
    | Some ((i, j), run, dir, heat_loss) ->
      let tree = Leftist.delete_min tree in
      (match Set.mem set ((i, j), run, dir) with
       | true -> aux tree ~set
       | false ->
         let set = Set.add set ((i, j), run, dir) in
         (* Hash_set.add visited ((i, j), run, dir); *)
         [ 0, 1; 0, -1; 1, 0; -1, 0 ]
         |> List.fold ~init:tree ~f:(fun tree (di, dj) ->
           let i', j' = i + di, j + dj in
           (* This might be the uglyist thing I've ever written *)
           match
             ( i' < 0
               || j' < 0
               || i' >= Array.length grid
               || j' >= Array.length grid.(0)
             , fst dir = di
             , snd dir = dj
             , run >= max_run
             , fst dir = -di
             , snd dir = -dj
             , run < min_run )
           with
           | true, _, _, _, _, _, _ -> tree
           | _, true, true, true, _, _, _ -> tree
           | _, _, _, _, true, true, _ -> tree
           | _, false, false, _, _, _, true -> tree
           | _, same_i, same_j, _, _, _, _ ->
             let heat_loss' = heat_loss + grid.(i').(j') in
             let run' =
               match same_i, same_j with
               | true, true -> run + 1
               | _ -> 1
             in
             Leftist.insert tree ((i', j'), run', (di, dj), heat_loss'))
         |> aux ~set)
  in
  (* init the tree with starting directions *)
  let tree =
    [ 0, 1; 0, -1; 1, 0; -1, 0 ]
    |> List.fold ~init:Leftist.empty ~f:(fun tree dir ->
      Leftist.insert tree ((0, 0), 0, dir, 0))
  in
  aux tree ~set:(Set.empty (module State))
;;

let part_1 lines =
  let grid = parse lines in
  min_heat_loss grid 0 3
;;

let part_2 lines =
  let grid = parse lines in
  min_heat_loss grid 4 10
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day17.txt"
    ~test_path:"../data/sample/day17.txt"
    ~test_1_target:102
    ~test_2_target:94
    ()
  |> Command_unix.run
;;
