open Core

let prepare contents =
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

let adjacent (num_row, num_col, _num) (sym_row, sym_col, _symbol) =
  let start_row = num_row - 1 in
  let start_col = num_col - 1 in
  let end_row = num_row + 4 in
  let end_col = num_col + 1 in
  sym_row >= start_row
  && sym_row <= end_row
  && sym_col >= start_col
  && sym_col <= end_col
;;

let part_1 contents =
  let nums, symbols = prepare contents in
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

let _part_2 _lines = 0

let () =
  let test_contents = Aoc.read_file "../data/sample/day3.txt" in
  let part_1_test = part_1 test_contents in
  Printf.printf "Test 1: %d\n" part_1_test;
  (* let test_lines = Aoc.read_lines "../data/sample/day3.txt" in
     let lines = Aoc.read_lines "../data/day3.txt" in

     let part_1_test = part_1 test_lines in

     if part_1_test = 4361 then
     Printf.printf "Test 1 passed\nPart 1: %d\n" (part_1 lines)
     else
     Printf.printf "Test 1 failed\nExpected: %d, Got: %d\n" 4361 part_1_test;

     let part_2_test = part_2 test_lines in

     if part_2_test = 467835 then
     Printf.printf "Test 2 passed\nPart 2: %d\n" (part_2 lines)
     else
     Printf.printf "Test 2 failed\nExpected: %d, Got: %d\n" 467835 part_2_test; *)
  ()
;;
