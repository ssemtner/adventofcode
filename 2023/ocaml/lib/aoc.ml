open Core

let read_lines file =
  Stdio.In_channel.with_file file ~f:(fun chan ->
    let x = In_channel.input_all chan in
    String.split_lines x)
;;

let read_file file =
  Stdio.In_channel.with_file file ~f:(fun chan ->
    let x = In_channel.input_all chan in
    x)
;;

let print_list l = List.iter l ~f:(fun x -> Stdio.printf "%s\n" x)

let command
  part_1
  part_2
  ~path
  ?(test_path = None)
  ?(test_path_2 = None)
  ?(test_1_target = None)
  ?(test_2_target = None)
  ()
  =
  Command.basic
    ~summary:"Advent Of Code (ssemtner)"
    (let%map_open.Command test = flag "-t" no_arg ~doc:"test"
     and part = flag "-p" (optional int) ~doc:"part [optional]" in
     fun () ->
       let lines part =
         (match test with
          | true ->
            (match part with
             | 1 ->
               (match test_path with
                | Some p -> p
                | None -> path)
             | 2 ->
               (match test_path_2 with
                | Some p -> p
                | None ->
                  (match test_path with
                   | Some p -> p
                   | None -> path))
             | _ -> path)
          | false -> path)
         |> read_lines
       in
       let print_result part target result time =
         match target with
         | Some target ->
           if result = target
           then Printf.printf "Part %d: %d (ok) (%f ms)\n" part result time
           else
             Printf.printf
               "Part %d: %d (failed, expected %d) (%f ms)\n"
               part
               result
               target
               time
         | None -> Printf.printf "Part %d: %d (%f ms)\n" part result time
       in
       let execute_part part =
         let f, lines', target =
           match part with
           | 1 -> part_1, lines 1, test_1_target
           | 2 -> part_2, lines 2, test_2_target
           | _ -> raise (Invalid_argument "Invalid part")
         in
         let target =
           match target with
           | Some target ->
             (match test with
              | true -> Some target
              | false -> None)
           | None -> None
         in
         let t = Time_float.now () in
         let result = f lines' in
         Time_float.diff (Time_float.now ()) t
         |> Time_float.Span.to_ms
         |> print_result part target result;
         ()
       in
       match part with
       | Some 1 -> execute_part 1
       | Some 2 -> execute_part 2
       | Some _ | None ->
         execute_part 1;
         execute_part 2)
;;
