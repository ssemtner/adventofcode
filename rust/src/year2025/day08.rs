use crate::util::sample::is_sample;
use itertools::Itertools;
use std::collections::HashMap;

type Input = (HashMap<usize, (i64, i64, i64)>, Vec<(i64, usize, usize)>);

// disjoint set
struct Circuit {
    parent: usize,
    size: usize,
}

fn find(target: usize, circuits: &mut [Circuit]) -> usize {
    if circuits[target].parent != target {
        circuits[target].parent = find(circuits[target].parent, circuits);
        return circuits[target].parent;
    }
    target
}

fn union(a: usize, b: usize, circuits: &mut [Circuit]) {
    let mut a = find(a, circuits);
    let mut b = find(b, circuits);
    if a == b {
        return;
    }
    if circuits[a].size < circuits[b].size {
        std::mem::swap(&mut a, &mut b);
    }
    circuits[b].parent = a;
    circuits[a].size += circuits[b].size;
}

pub fn parse(input: &str) -> Input {
    let boxes: Vec<(usize, (i64, i64, i64))> = input
        .lines()
        .enumerate()
        .map(|(i, line)| {
            let pos = line
                .split(",")
                .map(|n| n.parse().unwrap())
                .collect_tuple()
                .unwrap();

            (i, pos)
        })
        .collect();

    let pairs: Vec<_> = boxes
        .iter()
        .tuple_combinations()
        .map(|(a, b)| {
            let dist =
                (a.1 .0 - b.1 .0).pow(2) + (a.1 .1 - b.1 .1).pow(2) + (a.1 .2 - b.1 .2).pow(2);

            (a, b, dist)
        })
        .map(|((a, _), (b, _), dist)| (dist, *a, *b))
        .collect();

    (boxes.into_iter().collect(), pairs)
}

pub fn part1((boxes, pairs): &Input) -> usize {
    let mut circuits: Vec<_> = (0..boxes.len())
        .map(|i| Circuit { parent: i, size: 1 })
        .collect();

    let todo = if is_sample() { 10 } else { 1000 };

    for &(_, id1, id2) in pairs.iter().k_smallest(todo) {
        let set1 = find(id1, &mut circuits);
        let set2 = find(id2, &mut circuits);
        if set1 != set2 {
            union(set1, set2, &mut circuits);
        }
    }

    circuits
        .iter()
        .map(|set| set.size)
        .sorted()
        .rev()
        .take(3)
        .product()
}

pub fn part2((boxes, pairs): &Input) -> usize {
    let mut circuits: Vec<_> = (0..boxes.len())
        .map(|i| Circuit { parent: i, size: 1 })
        .collect();

    let mut count = boxes.len();

    for &(_, id1, id2) in pairs.iter().sorted_unstable() {
        let set1 = find(id1, &mut circuits);
        let set2 = find(id2, &mut circuits);
        if set1 != set2 {
            union(set1, set2, &mut circuits);
            count -= 1;
            if count == 1 {
                return (boxes[&id1].0 * boxes[&id2].0) as usize;
            }
        }
    }

    unreachable!()
}
