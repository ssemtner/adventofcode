open Core

let prepare ?gears_only lines =
  let contents = String.concat lines ~sep:"\n" in
  let rec aux row col num nums symbols = function
    | [] -> nums, symbols
    | x :: xs ->
      (match x with
       | '0' .. '9' ->
         aux
           row
           (col + 1)
           ((num * 10) + Char.to_int x - Char.to_int '0')
           nums
           symbols
           xs
       | _ ->
         (* end of number *)
         let nums' =
           match num with
           | 0 -> nums
           | _ -> (row, col, num) :: nums
         in
         (match x with
          | '\n' -> aux (row + 1) 0 0 nums' symbols xs
          | '.' -> aux row (col + 1) 0 nums' symbols xs
          | '*' -> aux row (col + 1) 0 nums' ((row, col, x) :: symbols) xs
          | _ ->
            (match gears_only with
             | Some true -> aux row (col + 1) 0 nums' symbols xs
             | _ -> aux row (col + 1) 0 nums' ((row, col, x) :: symbols) xs)))
  in
  aux 0 0 0 [] [] (String.to_list contents)
;;

let sides (start_row, start_col, len) =
  let digits = String.length (Int.to_string len) in
  let rec aux acc row col =
    match col with
    | col when col = start_col ->
      (match row with
       | row when row = start_row + 1 -> (row, col) :: acc
       | _ -> aux ((row, col) :: acc) (row + 1) (start_col - digits - 1))
    | col when col = start_col - digits - 1 ->
      aux ((row, col) :: acc) row (col + 1)
    | _ ->
      (match row with
       | row when row = start_row -> aux acc row (col + 1)
       | _ -> aux ((row, col) :: acc) row (col + 1))
  in
  aux [] (start_row - 1) (start_col - digits - 1)
;;

let symbol_exists_at symbols (row, col) =
  List.find symbols ~f:(fun (r, c, _) -> r = row && c = col)
  |> function
  | Some _ -> true
  | None -> false
;;

let positions = [ 1, 1; 1, 0; 1, -1; 0, 1; 0, -1; -1, 1; -1, 0; -1, -1 ]
let connected_numbers nums (row, col) = 
  let rec aux acc = function
    | [] -> acc
    | (r, c) :: xs ->
      (match List.find nums ~f:(fun (r', c', _) -> r' = row + r && c' = col + c) with
       | Some (_, _, num) -> aux (Set.add acc num) xs
       | None -> aux acc xs)

let part_1 lines =
  let nums, symbols = prepare lines in
  let rec aux acc nums = function
    | [] -> acc
    | (row, col, num) :: xs ->
      let valid =
        sides (row, col, num)
        |> List.exists ~f:(fun (r, c) -> symbol_exists_at symbols (r, c))
      in
      (match valid with
       | true -> aux (acc + num) (num :: nums) xs
       | false -> aux acc nums xs)
  in
  aux 0 [] nums
;;

let part_2 lines =
  let nums, gears = prepare ~gears_only:true lines in
  let rec aux acc = function
    | [] -> acc
    | (row, col, _) :: xs ->
      Printf.printf "row: %d, col: %d\n" row col;
      let connected = connected_numbers nums (row, col) in
      (match Set.length connected with
       | 2 ->
         Printf.printf
           "connected: %s %d\n"
           (Set.fold connected ~init:"" ~f:(fun acc v ->
              acc ^ Int.to_string v ^ " "))
           (Set.fold connected ~init:1 ~f:( * ));
         aux (acc + Set.fold connected ~init:1 ~f:( * )) xs
       | _ ->
         Set.iter connected ~f:(fun v -> Printf.printf "%d " v);
         Printf.printf "not connected\n";
         aux acc xs)
  in
  aux 0 gears
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day3.txt"
    ~test_path:(Some "../data/sample/day3.txt")
    ~test_1_target:(Some 4361)
    ~test_2_target:(Some 467835)
    ()
  |> Command_unix.run
;;
