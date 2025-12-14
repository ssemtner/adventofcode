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
        .iter()
        .filter(|(target, nums)| solvable(*target, nums, false))
        .map(|(target, _)| target)
        .sum()
}

pub fn part2(input: &Input) -> u64 {
    input
        .iter()
        .filter(|(target, nums)| solvable(*target, nums, true))
        .map(|(target, _)| target)
        .sum()
}

fn solvable(target: u64, nums: &[u64], allow_concat: bool) -> bool {
    if nums.len() == 1 {
        return nums[0] == target;
    }

    let n = nums[nums.len() - 1];
    let remaining = &nums[0..nums.len() - 1];

    let q = target / n;
    let r = target % n;

    if r == 0 && solvable(q, remaining, allow_concat) {
        true
    } else if allow_concat
        && (target.wrapping_sub(n)) % 10u64.pow(n.ilog10() + 1) == 0
        && solvable(
            target / (10u64.pow(n.ilog10() + 1)),
            remaining,
            allow_concat,
        )
    {
        true
    } else {
        solvable(target.wrapping_sub(n), remaining, allow_concat)
    }
}
