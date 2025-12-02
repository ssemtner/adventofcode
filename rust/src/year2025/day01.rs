type Input = Vec<i32>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            let val: i32 = (&line[1..]).parse().unwrap();
            val * (match line.chars().next() {
                Some('L') => -1,
                Some('R') => 1,
                _ => unreachable!(),
            })
        })
        .collect()
}

pub fn part1(input: &Input) -> u32 {
    input
        .iter()
        .fold((50, 0), |(p, acc), val| {
            let pos = (p + val) % 100;
            if pos == 0 {
                (pos, acc + 1)
            } else {
                (pos, acc)
            }
        })
        .1
}

pub fn part2(input: &Input) -> u32 {
    input
        .iter()
        .fold((50, 0), |(p, acc), val| {
            let pos = p + val;
            (
                pos.rem_euclid(100),
                acc + (pos.div_euclid(100)).unsigned_abs(),
            )
        })
        .1
}
