#[derive(Debug)]
pub enum Op {
    Sum,
    Product,
}

type Input = String; // parsing is so different for each part

pub fn parse(input: &str) -> Input {
    input.to_string()
}

fn solve(problems: Vec<(Op, Vec<u64>)>) -> u64 {
    problems
        .iter()
        .map(|(op, nums)| match op {
            Op::Sum => nums.iter().sum::<u64>(),
            Op::Product => nums.iter().product(),
        })
        .sum()
}

pub fn part1(input: &Input) -> u64 {
    let nums: Vec<Vec<_>> = input
        .lines()
        .map(|line| line.split(" ").filter_map(|n| n.parse().ok()).collect())
        .collect();

    let problems = input
        .lines()
        .last()
        .unwrap()
        .split_whitespace()
        .enumerate()
        .map(|(i, op)| {
            let col = nums
                .iter()
                .filter_map(|row| row.get(i).copied())
                .collect();

            let op = match op {
                "+" => Op::Sum,
                "*" => Op::Product,
                _ => unreachable!(),
            };

            (op, col)
        })
        .collect();

    solve(problems)
}

pub fn part2(input: &Input) -> u64 {
    let data: Vec<_> = input.lines().map(|line| line.as_bytes()).collect();

    let mut problems = Vec::new();
    let mut nums = Vec::new();

    for (i, c) in input
        .lines()
        .last()
        .unwrap()
        .as_bytes()
        .iter()
        .enumerate()
        .rev()
    {
        // collect num from lines above
        let mut num = 0u64;
        for j in 0..data.len() - 1 {
            if data[j][i] != b' ' {
                let x = data[j][i] - b'0';
                num = num * 10 + x as u64;
            }
        }

        if num != 0 {
            nums.push(num);
        } else {
            nums.clear();
        }

        match c {
            b'+' => problems.push((Op::Sum, nums.clone())),
            b'*' => problems.push((Op::Product, nums.clone())),
            _ => (),
        }
    }

    solve(problems)
}
