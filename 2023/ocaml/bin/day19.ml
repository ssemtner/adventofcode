open Core

(* I way overwrote this day sorry *)

module Workflow = struct
  module Key = struct
    module T = struct
      type t =
        | X
        | M
        | A
        | S
      [@@deriving hash, compare, sexp_of]
    end

    include T
    include Comparator.Make (T)

    let of_char_exn = function
      | 'x' -> X
      | 'm' -> M
      | 'a' -> A
      | 's' -> S
      | _ -> failwith "invalid key"
    ;;

    let to_string = function
      | X -> "X"
      | M -> "M"
      | A -> "A"
      | S -> "S"
    ;;
  end

  module Rule = struct
    module Condition_result = struct
      type t =
        | Accept
        | Reject
        | Workflow of string

      let to_string = function
        | Accept -> "Accept"
        | Reject -> "Reject"
        | Workflow workflow -> "Workflow " ^ workflow
      ;;
    end

    type t =
      | Accept
      | Reject
      | GreaterThan of Key.t * int * Condition_result.t
      | LessThan of Key.t * int * Condition_result.t
      | Workflow of string
  end
end

let parse_workflow line =
  let name, workflows = String.lsplit2_exn line ~on:'{' in
  let workflows, _ = String.lsplit2_exn workflows ~on:'}' in
  let workflows =
    String.split workflows ~on:','
    |> List.map ~f:(fun workflow ->
      match workflow with
      | "A" -> Workflow.Rule.Accept
      | "R" -> Workflow.Rule.Reject
      | workflow ->
        (match String.lsplit2 workflow ~on:':' with
         | Some (condition, result) ->
           let key = String.get condition 0 |> Workflow.Key.of_char_exn in
           let value = String.drop_prefix condition 2 |> Int.of_string in
           let result =
             match result with
             | "A" -> Workflow.Rule.Condition_result.Accept
             | "R" -> Workflow.Rule.Condition_result.Reject
             | workflow -> Workflow.Rule.Condition_result.Workflow workflow
           in
           (match String.get condition 1 with
            | '>' -> Workflow.Rule.GreaterThan (key, value, result)
            | '<' -> Workflow.Rule.LessThan (key, value, result)
            | _ -> failwith "invalid condition")
         | None -> Workflow.Rule.Workflow workflow))
  in
  name, workflows
;;

let parse_part line =
  let line = String.drop_prefix line 1 in
  let line = String.drop_suffix line 1 in
  String.split line ~on:','
  |> List.fold
       ~init:(Map.empty (module Workflow.Key))
       ~f:(fun acc c ->
         let key = String.get c 0 |> Workflow.Key.of_char_exn in
         let data = String.drop_prefix c 2 |> Int.of_string in
         Map.add_exn acc ~key ~data)
;;

type result =
  | Accept
  | Reject
  | Workflow of string

let rec process_part_workflow workflow part =
  match workflow with
  | [] -> failwith "empty workflow"
  | [ x ] ->
    (match x with
     | Workflow.Rule.Accept -> Accept
     | Workflow.Rule.Reject -> Reject
     | Workflow.Rule.Workflow workflow -> Workflow workflow
     | _ -> failwith "invalid workflow")
  | x :: xs ->
    (match x with
     | Workflow.Rule.Accept -> Accept
     | Workflow.Rule.Reject -> Reject
     | Workflow.Rule.GreaterThan (key, value, result) ->
       (match Map.find part key with
        | None -> failwith "invalid key"
        | Some value' ->
          if value >= value'
          then process_part_workflow xs part
          else (
            match result with
            | Workflow.Rule.Condition_result.Accept -> Accept
            | Workflow.Rule.Condition_result.Reject -> Reject
            | Workflow.Rule.Condition_result.Workflow workflow ->
              Workflow workflow))
     | Workflow.Rule.LessThan (key, value, result) ->
       (match Map.find part key with
        | None -> failwith "invalid key"
        | Some value' ->
          if value <= value'
          then process_part_workflow xs part
          else (
            match result with
            | Workflow.Rule.Condition_result.Accept -> Accept
            | Workflow.Rule.Condition_result.Reject -> Reject
            | Workflow.Rule.Condition_result.Workflow workflow ->
              Workflow workflow))
     | Workflow.Rule.Workflow workflow -> Workflow workflow)
;;

let rec process_part workflows cur_workflow part =
  let workflow = Map.find_exn workflows cur_workflow in
  match process_part_workflow workflow part with
  | Accept ->
    printf " accepted %s\n" cur_workflow;
    true
  | Reject ->
    printf " rejected %s\n" cur_workflow;
    false
  | Workflow workflow ->
    printf " to workflow %s\n" workflow;
    process_part workflows workflow part
;;

let part_value = Map.fold ~init:0 ~f:(fun ~key:_ ~data acc -> acc + data)

(* TODO: get 446935 *)
let part_1 _lines =
  let workflow_lines, part_lines =
    List.split_while _lines ~f:(fun line -> not (String.is_empty line))
  in
  let part_lines = List.drop part_lines 1 in
  let workflows =
    List.fold
      workflow_lines
      ~init:(Map.empty (module String))
      ~f:(fun acc line ->
        let name, workflow = parse_workflow line in
        Map.add_exn acc ~key:name ~data:workflow)
  in
  let parts = List.map part_lines ~f:parse_part in
  List.fold parts ~init:0 ~f:(fun acc part ->
    printf "process part with x=%d\n" (Map.find_exn part Workflow.Key.X);
    match process_part workflows "in" part with
    | true ->
      printf " accepted %d\n" (part_value part);
      acc + part_value part
    | false -> acc)
;;

(* printf "workflow length: %d\n" (List.length workflows);
   printf "parts length: %d\n" (List.length parts);
   let first_workflow = List.hd_exn _lines |> parse_workflow in
   printf "first workflow: %s\n" (fst first_workflow);
   List.iter (snd first_workflow) ~f:(fun w ->
   match w with
   | Workflow.Rule.Accept -> print_endline "Accept"
   | Workflow.Rule.Reject -> print_endline "Reject"
   | Workflow.Rule.GreaterThan (key, value, result) ->
   printf
   "GreaterThan %s %d (%s)\n"
   (Workflow.Key.to_string key)
   value
   (Workflow.Rule.Condition_result.to_string result)
   | Workflow.Rule.LessThan (key, value, result) ->
   printf
   "LessThan %s %d (%s)\n"
   (Workflow.Key.to_string key)
   value
   (Workflow.Rule.Condition_result.to_string result)
   | Workflow.Rule.Workflow workflow -> printf "Workflow %s\n" workflow); *)

let part_2 _lines = 0

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day19.txt"
    ~test_path:(Some "../data/sample/day19.txt")
    ~test_1_target:(Some 19114)
    ~test_2_target:None
    ()
  |> Command_unix.run
;;
