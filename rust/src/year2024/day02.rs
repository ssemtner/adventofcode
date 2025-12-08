type Input = Vec<Vec<u32>>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .filter_map(|s| s.parse::<u32>().ok())
                .collect()
        })
        .collect()
}

fn safe(levels: &Vec<u32>) -> bool {
    let mut last = levels[0];
    let inc = levels[1] > last;
    for &level in levels.iter().skip(1) {
        let diff = level.abs_diff(last);
        if !(1..4).contains(&diff) || (inc && level <= last) || (!inc && level >= last) {
            return false;
        }
        last = level;
    }
    true
}

pub fn part1(input: &Input) -> usize {
    input.iter().filter(|levels| safe(levels)).count()
}

pub fn part2(input: &Input) -> usize {
    input
        .iter()
        .filter(|&levels| {
            safe(levels)
                || (0..levels.len()).any(|i| {
                    let mut levels = levels.clone();
                    levels.remove(i);
                    safe(&levels)
                })
        })
        .count()
}
