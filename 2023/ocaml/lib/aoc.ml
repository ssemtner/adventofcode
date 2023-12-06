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
