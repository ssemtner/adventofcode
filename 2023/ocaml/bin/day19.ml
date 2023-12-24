open Core

(* I way overwrote this day *)
(* there is also a lot of duplicated code I could clean up like *)
(*   between the greaterthan and lessthan cases but I don't feel like it rn *)

module Workflow = struct
  type result =
    | Accept
    | Reject
    | Workflow of string

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
  end

  module Rule = struct
    type t =
      | Accept
      | Reject
      | GreaterThan of Key.t * int * result
      | LessThan of Key.t * int * result
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
             | "A" -> Workflow.Accept
             | "R" -> Workflow.Reject
             | workflow -> Workflow.Workflow workflow
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

let rec process_part_workflow workflow part =
  match workflow with
  | [] -> failwith "empty workflow"
  | [ x ] ->
    (match x with
     | Workflow.Rule.Accept -> Workflow.Accept
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
          if value >= value' then process_part_workflow xs part else result)
     | Workflow.Rule.LessThan (key, value, result) ->
       (match Map.find part key with
        | None -> failwith "invalid key"
        | Some value' ->
          if value <= value' then process_part_workflow xs part else result)
     | Workflow.Rule.Workflow workflow -> Workflow workflow)
;;

let rec process_part workflows cur_workflow part =
  let workflow = Map.find_exn workflows cur_workflow in
  match process_part_workflow workflow part with
  | Accept -> true
  | Reject -> false
  | Workflow workflow -> process_part workflows workflow part
;;

let part_value part =
  Map.fold part ~init:0 ~f:(fun ~key:_ ~data acc -> acc + data)
;;

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
    match process_part workflows "in" part with
    | true -> acc + part_value part
    | false -> acc)
;;

let parts_in_range range =
  Map.fold range ~init:1 ~f:(fun ~key:_ ~data:(low, high) acc ->
    acc * (high - low + 1))
;;

let rec process_part_range_workflow workflow part_range accepted =
  match workflow with
  | [] -> failwith "empty workflow"
  | [ x ] ->
    (match x with
     | Workflow.Rule.Accept -> accepted + parts_in_range part_range, []
     | Workflow.Rule.Reject -> accepted, []
     | Workflow.Rule.Workflow workflow -> accepted, [ workflow, part_range ]
     | _ -> failwith "invalid workflow")
  | x :: xs ->
    (match x with
     | Workflow.Rule.Accept -> accepted + parts_in_range part_range, []
     | Workflow.Rule.Reject -> accepted, []
     | Workflow.Rule.Workflow workflow -> accepted, [ workflow, part_range ]
     | Workflow.Rule.GreaterThan (key, value, result) ->
       let low, high = Map.find_exn part_range key in
       (* if outside of range *)
       if value > high || value < low
       then process_part_range_workflow xs part_range accepted
       else (
         let yes_range = Map.set part_range ~key ~data:(value + 1, high) in
         let no_range = Map.set part_range ~key ~data:(low, value) in
         match result with
         | Workflow.Accept ->
           process_part_range_workflow
             xs
             no_range
             (accepted + parts_in_range yes_range)
         | Workflow.Reject -> process_part_range_workflow xs no_range accepted
         | Workflow.Workflow workflow ->
           let gt_accepted, gt_to_check =
             process_part_range_workflow xs no_range accepted
           in
           gt_accepted, (workflow, yes_range) :: gt_to_check)
     | Workflow.Rule.LessThan (key, value, result) ->
       let low, high = Map.find_exn part_range key in
       (* if outside of range *)
       if value > high || value < low
       then process_part_range_workflow xs part_range accepted
       else (
         let yes_range = Map.set part_range ~key ~data:(low, value - 1) in
         let no_range = Map.set part_range ~key ~data:(value, high) in
         match result with
         | Workflow.Accept ->
           process_part_range_workflow
             xs
             no_range
             (accepted + parts_in_range yes_range)
         | Workflow.Reject -> process_part_range_workflow xs no_range accepted
         | Workflow.Workflow workflow ->
           let lt_accepted, lt_to_check =
             process_part_range_workflow xs no_range accepted
           in
           lt_accepted, (workflow, yes_range) :: lt_to_check))
;;

let rec process_part_range workflows cur_workflow part_range accepted =
  let workflow = Map.find_exn workflows cur_workflow in
  match process_part_range_workflow workflow part_range accepted with
  | accepted, [] -> accepted
  | accepted, todo ->
    List.fold todo ~init:accepted ~f:(fun acc (workflow, part_range) ->
      acc + process_part_range workflows workflow part_range 0)
;;

let initial_part_range () =
  Map.of_alist_exn
    (module Workflow.Key)
    [ Workflow.Key.X, (1, 4000)
    ; Workflow.Key.M, (1, 4000)
    ; Workflow.Key.A, (1, 4000)
    ; Workflow.Key.S, (1, 4000)
    ]
;;

let part_2 lines =
  let workflows =
    List.take_while lines ~f:(fun line -> not (String.is_empty line))
    |> List.fold
         ~init:(Map.empty (module String))
         ~f:(fun acc line ->
           let name, workflow = parse_workflow line in
           Map.add_exn acc ~key:name ~data:workflow)
  in
  process_part_range workflows "in" (initial_part_range ()) 0
;;

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day19.txt"
    ~test_path:"../data/sample/day19.txt"
    ~test_1_target:19114
    ~test_2_target:167409079868000
    ()
  |> Command_unix.run
;;
