type Input = Vec<(u64, Vec<u64>)>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            let (target, rest) = line.split_once(": ").unwrap();
            let target = target.parse().unwrap();
            let nums = rest
                .split_whitespace()
                .map(|n| n.parse().unwrap())
                .collect();

            (target, nums)
        })
        .collect()
}

pub fn part1(input: &Input) -> u64 {
    input
        .into_iter()
        .filter(|(target, nums)| solvable(target, nums, false, 0, 0))
        .map(|(target, _)| target)
        .sum()
}

pub fn part2(input: &Input) -> u64 {
    input
        .into_iter()
        .filter(|(target, nums)| solvable(target, nums, true, 0, 0))
        .map(|(target, _)| target)
        .sum()
}

fn solvable(target: &u64, nums: &[u64], part2: bool, total: u64, i: usize) -> bool {
    if i == nums.len() {
        return total == *target;
    }

    let product = total * nums[i];
    let sum = total + nums[i];
    let concat = format!("{}{}", total, nums[i]).parse::<u64>().unwrap();

    solvable(target, nums, part2, sum, i + 1)
        || (product <= *target && solvable(target, nums, part2, product, i + 1))
        || (part2 && concat <= *target && solvable(target, nums, part2, concat, i + 1))
}
