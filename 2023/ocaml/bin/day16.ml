open Core

let parse lines =
  Array.of_list_map lines ~f:(fun line -> line |> String.to_array)
;;

let next_directions dir c =
  match c with
  | '.' -> [ dir ]
  | '|' ->
    (match dir with
     | _, 0 -> [ dir ]
     | 0, _ -> [ 1, 0; -1, 0 ]
     | _ ->
       failwithf "Invalid direction (char %c): %d, %d" c (fst dir) (snd dir) ())
  | '-' ->
    (match dir with
     | 0, _ -> [ dir ]
     | _, 0 -> [ 0, 1; 0, -1 ]
     | _ ->
       failwithf "Invalid direction (char %c): %d, %d" c (fst dir) (snd dir) ())
  | '/' -> (fun (a, b) -> -b, -a) dir :: []
  | '\\' -> (fun (a, b) -> b, a) dir :: []
  | c -> failwithf "Invalid char: %c" c ()
;;

let horiz_or_vert dir =
  match dir with
  | 0, _ -> 'h'
  | _, 0 -> 'v'
  | _ ->
    failwithf
      "(horizontal_or_vertical) Invalid direction: %d, %d"
      (fst dir)
      (snd dir)
      ()
;;

let hash (row, col) dir =
  let c = horiz_or_vert dir in
  Printf.sprintf "%d,%d,%c" row col c
;;

module Point = struct
  module T = struct
    type t = int * int [@@deriving compare, hash, sexp_of]
  end

  include T
  include Comparator.Make (T)
end

module Point_dir = struct
  module T = struct
    type t = (int * int) * (int * int) [@@deriving compare, hash, sexp_of]
  end

  include T
  include Comparator.Make (T)
end

(* My attempt at doing this recursivly because I suck at function programming *)
let _energized_spaces grid =
  let rec aux row col dir set depth =
    printf
      "[d=%d] aux row: %d, col: %d, dir: (%d, %d) set len: %d\n"
      depth
      row
      col
      (fst dir)
      (snd dir)
      (Set.length set);
    let next_dirs = next_directions dir grid.(row).(col) in
    printf " next_dirs len: %d\n" (List.length next_dirs);
    List.fold next_dirs ~init:set ~f:(fun set dir ->
      printf "  [d=%d] dir: (%d, %d)\n" depth (fst dir) (snd dir);
      match Set.mem set ((row + fst dir, col + snd dir), dir) with
      | true ->
        printf "    \"%s\" already in set\n" (hash (row, col) dir);
        set
      | false ->
        printf "    adding \"%s\" to set\n" (hash (row, col) dir);
        let set = Set.add set ((row, col), dir) in
        printf "    calling aux\n";
        (match dir with
         | r, c when row + r < 0 || col + c < 0 ->
           print_endline "    oob";
           set
         | r, c
           when row + r >= Array.length grid || col + c >= Array.length grid.(0)
           ->
           print_endline "    oob";
           set
         | r, c -> aux (row + r) (col + c) dir set (depth + 1)))
  in
  let starting_directions = next_directions (0, 1) grid.(0).(0) in
  List.fold
    starting_directions
    ~init:(Set.empty (module Point_dir))
    ~f:(fun set (row, col) -> aux row col (row, col) set 0)
;;

let energized_spaces grid starting_configs =
  let points = Hash_set.create (module Point) in
  let configs = Hash_set.create (module Point_dir) in
  let queue = Queue.create () in
  List.iter starting_configs ~f:(fun config -> Queue.enqueue queue config);
  while not (Queue.is_empty queue) do
    let (row, col), dir = Queue.dequeue_exn queue in
    match Hash_set.mem configs ((row, col), dir) with
    | true -> ()
    | false ->
      Hash_set.add configs ((row, col), dir);
      Hash_set.add points (row, col);
      (match row + fst dir, col + snd dir with
       | r, c when r < 0 || c < 0 -> ()
       | r, c when r >= Array.length grid || c >= Array.length grid.(0) -> ()
       | r, c ->
         let next = grid.(r).(c) in
         let next_dirs = next_directions dir next in
         List.iter next_dirs ~f:(fun dir -> Queue.enqueue queue ((r, c), dir)))
  done;
  Hash_set.length points
;;

let _print_grid grid =
  Array.iter grid ~f:(fun row ->
    Array.iter row ~f:(fun c -> printf "%c" c);
    print_endline "")
;;

let _unique_points set =
  Set.fold
    set
    ~init:(Set.empty (module Point))
    ~f:(fun set (point, _c) -> Set.add set point)
;;

let part_1 lines =
  let grid = parse lines in
  let starting_directions = next_directions (0, 1) grid.(0).(0) in
  let starting_configs =
    List.map starting_directions ~f:(fun dir -> (0, 0), dir)
  in
  energized_spaces grid starting_configs
;;

let all_starting_configs grid =
  let rows = Array.length grid in
  let cols = Array.length grid.(0) in
  (* cringe non functional stuff is happening im tired *)
  let set = Hash_set.create (module Point_dir) in
  for row = 0 to rows - 1 do
    (* add with col = 0 *)
    Hash_set.add set ((row, 0), (0, 1));
    (* add with col = cols - 1 *)
    Hash_set.add set ((row, cols - 1), (0, -1))
  done;
  for col = 0 to cols - 1 do
    (* add with row = 0 *)
    Hash_set.add set ((0, col), (1, 0));
    (* add with row = rows - 1 *)
    Hash_set.add set ((rows - 1, col), (-1, 0))
  done;
  set
;;

let part_2 lines =
  let grid = parse lines in
  let starting_configs = all_starting_configs grid in
  Hash_set.to_list starting_configs
  |> List.map ~f:(fun config -> energized_spaces grid [ config ])
  |> List.max_elt ~compare:Int.compare
  |> Option.value_exn
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day16.txt"
    ~test_path:(Some "../data/sample/day16.txt")
    ~test_1_target:(Some 46)
    ~test_2_target:None
    ()
  |> Command_unix.run
;;
