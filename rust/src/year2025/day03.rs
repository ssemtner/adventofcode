type Input = Vec<Vec<u8>>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| line.as_bytes().iter().map(|b| b - b'0').collect())
        .collect()
}

fn solve(input: &Input, digits: usize) -> u64 {
    input
        .iter()
        .map(|vals| {
            (0..digits)
                .fold((0, 0), |(joltage, start), i| {
                    let next = vals[start..=(vals.len() - (digits - i))]
                        .iter()
                        .max()
                        .unwrap();
                    (
                        joltage * 10 + *next as u64,
                        vals[start..].iter().position(|val| val == next).unwrap() + start + 1,
                    )
                })
                .0
        })
        .sum()
}

pub fn part1(input: &Input) -> u64 {
    solve(input, 2)
}

pub fn part2(input: &Input) -> u64 {
    solve(input, 12)
}
