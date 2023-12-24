open Core

module Node = struct
  type t = int [@@deriving sexp, compare, hash, equal]
end

module Edge = struct
  type t = string [@@deriving sexp, compare, hash]

  let default = ""
end

module G = Graph.Persistent.Digraph.ConcreteBidirectionalLabeled (Node) (Edge)
module M1 = Graph.Traverse.Bfs (G)

module Dot = Graph.Graphviz.Dot (struct
    include G (* use the graph module from above *)

    let edge_attributes (_, e, _) = [ `Label e; `Color 4711 ]
    let default_edge_attributes _ = []
    let get_subgraph _ = None
    let vertex_attributes _ = [ `Shape `Box ]
    let vertex_name v = string_of_int v
    let default_vertex_attributes _ = []
    let graph_attributes _ = []
  end)

let () =
  let g = G.empty in
  let v1 = G.V.create 1 in
  let g = G.add_vertex g v1 in
  let v2 = G.V.create 2 in
  let g = G.add_vertex g v2 in
  let g = G.add_vertex g (G.V.create 3) in
  let g = G.add_vertex g (G.V.create 4) in
  let g = G.add_edge g 1 2 in
  let g = G.add_edge g 2 3 in
  let g = G.add_edge g 3 4 in
  let g = G.add_edge g 2 4 in
  M1.iter (fun v -> printf "%d\n" v) g;
  ()
;;

let part_1 _lines = 0
let part_2 _lines = 0

let () =
  Aoc.command
    part_1
    part_2
    ~path:"../data/day20.txt"
    ~test_path:"../data/sample/day20.txt"
    ~test_1_target:0
    ()
  |> Command_unix.run
;;
