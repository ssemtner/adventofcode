use itertools::Itertools;

pub struct Input {
    ranges: Vec<(u64, u64)>,
    ids: Vec<u64>,
}

pub fn parse(input: &str) -> Input {
    let (ranges, ids) = input.split_once("\n\n").unwrap();

    let ranges: Vec<(u64, u64)> = ranges
        .split("\n")
        .map(|line| {
            line.split("-")
                .map(|s| s.parse().unwrap())
                .collect_tuple()
                .unwrap()
        })
        // merge ranges
        .sorted_by_key(|&(start, _end)| start)
        .fold(Vec::new(), |mut acc, (start, end)| {
            match acc.last_mut() {
                Some((_, e)) if start <= *e => {
                    *e = (*e).max(end);
                }
                _ => acc.push((start, end)),
            }
            acc
        });

    let ids = ids.trim().split("\n").map(|s| s.parse().unwrap()).collect();

    Input { ranges, ids }
}

pub fn part1(Input { ranges, ids }: &Input) -> usize {
    ids.iter()
        .filter(
            |&id| match ranges.binary_search_by_key(id, |&(start, _end)| start) {
                Ok(_) => true,
                Err(i) if i > 0 => {
                    let (start, end) = ranges[i - 1];
                    (start..=end).contains(id)
                }
                _ => false,
            },
        )
        .count()
}

pub fn part2(Input { ranges, ids: _ }: &Input) -> u64 {
    ranges.iter().map(|(start, end)| end - start + 1).sum()
}
