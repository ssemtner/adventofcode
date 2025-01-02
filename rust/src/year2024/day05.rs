use fxhash::{FxHashMap, FxHashSet};

type Input = (FxHashMap<u32, Vec<u32>>, Vec<Vec<u32>>);

pub fn parse(input: &str) -> Input {
    let (rules, updates) = input.split_once("\n\n").unwrap();

    let mut rules_map = FxHashMap::default();
    rules
        .lines()
        .map(|line| {
            let (from, to) = line.split_once("|").unwrap();
            (from.parse().unwrap(), to.parse().unwrap())
        })
        .for_each(|(from, to)| {
            rules_map.entry(to).or_insert_with(Vec::new).push(from);
        });

    let updates = updates
        .lines()
        .map(|line| line.split(",").map(|n| n.parse().unwrap()).collect())
        .collect();

    (rules_map, updates)
}

pub fn part1((rules, updates): &Input) -> u32 {
    updates
        .iter()
        .filter(|update| issue(rules, update).is_none())
        .map(|update| update[update.len() / 2])
        .sum()
}

pub fn part2((rules, updates): &Input) -> u32 {
    updates
        .iter()
        .filter(|update| issue(rules, update).is_some())
        .map(|update| {
            let mut update = update.clone();
            while let Some((a, b)) = issue(rules, &update) {
                let a_i = update.iter().position(|x| x == &a).unwrap();
                let b_i = update.iter().position(|x| x == &b).unwrap();
                update.swap(a_i, b_i);
            }

            update[update.len() / 2]
        })
        .sum()
}

fn issue(rules: &FxHashMap<u32, Vec<u32>>, update: &Vec<u32>) -> Option<(u32, u32)> {
    let s: FxHashSet<&u32> = FxHashSet::from_iter(update.into_iter());
    let mut seen = FxHashSet::default();

    for a in update {
        for b in rules.get(a).unwrap_or(&vec![]) {
            if s.contains(b) && !seen.contains(b) {
                return Some((*a, *b));
            }
        }
        seen.insert(a);
    }

    None
}
