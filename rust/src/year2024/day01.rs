use fxhash::FxHashMap;
use itertools::Itertools;

type Input = (Vec<u32>, Vec<u32>);

pub fn parse(input: &str) -> Input {
    let a = input
        .split_whitespace()
        .filter_map(|s| s.parse::<u32>().ok())
        .collect_vec();
    a.chunks_exact(2).map(|l| (l[0], l[1])).unzip()
}

pub fn part1(input: &Input) -> u32 {
    let mut a = input.0.clone();
    let mut b = input.1.clone();
    a.sort_unstable();
    b.sort_unstable();
    a.iter().zip(b.iter()).map(|(a, &b)| a.abs_diff(b)).sum()
}

pub fn part2((a, b): &Input) -> u32 {
    let mut counts = FxHashMap::with_capacity_and_hasher(b.len(), Default::default());
    for &x in b {
        counts.entry(x).and_modify(|e| *e += 1).or_insert(1);
    }

    a.iter().map(|&x| counts.get(&x).unwrap_or(&0) * x).sum()
}
