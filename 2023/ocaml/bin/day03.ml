open Core

let prepare lines =
  let contents = String.concat lines ~sep:"\n" in
  let rec aux row col num nums symbols = function
    | [] -> nums, symbols
    | x :: xs ->
      (match x with
       | '.' | '\n' ->
         (* end of number *)
         let nums' =
           match num with
           | 0 -> nums
           | _ -> (row, col, num) :: nums
         in
         let row', col' =
           match x with
           | '\n' -> row + 1, 0
           | _ -> row, col + 1
         in
         aux row' col' 0 nums' symbols xs
       | '0' .. '9' ->
         aux
           row
           (col + 1)
           ((num * 10) + Char.to_int x - Char.to_int '0')
           nums
           symbols
           xs
       | _ ->
         (* symbol *)
         aux row (col + 1) num nums ((row, col, x) :: symbols) xs)
  in
  aux 0 0 0 [] [] (String.to_list contents)
;;

let adjacent (num_row, num_col, num) (sym_row, sym_col, _symbol) =
  let row_diff = abs (num_row - sym_row) in
  let num_digits = Float.log10 (Float.of_int num) |> Float.to_int in
  row_diff <= 1 && num_col - num_digits - 2 <= sym_col && sym_col <= num_col + 2
;;

let part_1 lines =
  let nums, symbols = prepare lines in
  List.map nums ~f:(fun (row, col, num) ->
    Printf.sprintf "%d (%d, %d)" num row col)
  |> Aoc.print_list;
  List.map symbols ~f:(fun (row, col, symbol) ->
    Printf.sprintf "%c (%d, %d)" symbol row col)
  |> Aoc.print_list;
  let rec aux acc = function
    | [] -> acc
    | (row, col, num) :: xs ->
      let valid = List.exists symbols ~f:(adjacent (row, col, num)) in
      (match valid with
       | true -> aux (acc + num) xs
       | false ->
         Printf.printf "Invalid number: %d (%d, %d)\n" num row col;
         aux acc xs)
  in
  aux 0 nums
;;

let part_2 _lines = 0

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day3.txt"
    ~test_path:(Some "../data/sample/day3.txt")
    ()
  |> Command_unix.run
;;
