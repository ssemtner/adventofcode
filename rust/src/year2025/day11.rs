use fxhash::FxHashMap;

type Input = (FxHashMap<String, usize>, FxHashMap<usize, Vec<usize>>);

pub fn parse(input: &str) -> Input {
    let mut keys = FxHashMap::default();
    let mut next = 0;
    let mut key = |key: &str| {
        let entry = keys.entry(key.to_string()).or_insert_with(|| {
            next += 1;
            next
        });
        *entry
    };
    let adj = input
        .lines()
        .map(|line| {
            line.split_once(": ")
                .map(|(from, to)| (key(from), to.split_whitespace().map(|x| key(x)).collect()))
                .unwrap()
        })
        .collect();
    (keys, adj)
}

fn dfs(adj: &FxHashMap<usize, Vec<usize>>, counts: &mut FxHashMap<usize, u64>, node: &usize) {
    let mut ways = 0;

    if adj.contains_key(&node) {
        for child in adj[&node].iter() {
            if !counts.contains_key(child) {
                dfs(adj, counts, child);
            }
            ways += counts.get(child).unwrap();
        }
    }

    counts.insert(*node, ways);
}

fn ways((keys, adj): &Input, from: &str, to: &str) -> u64 {
    let mut counts: FxHashMap<usize, u64> = FxHashMap::from_iter([(keys[to], 1)]);

    dfs(adj, &mut counts, &keys[from]);

    *counts.get(&keys[from]).unwrap()
}

pub fn part1(input: &Input) -> u64 {
    ways(input, "you", "out")
}

pub fn part2(input: &Input) -> u64 {
    let option1 = ways(input, "dac", "fft");
    let option2 = ways(input, "fft", "dac");

    match (option1, option2) {
        (val, 0) => ways(input, "svr", "dac") * val * ways(input, "fft", "out"),
        (0, val) => ways(input, "svr", "fft") * val * ways(input, "dac", "out"),
        _ => unreachable!(),
    }
}
