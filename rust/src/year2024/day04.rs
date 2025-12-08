use itertools::Itertools;

type Input = Vec<Vec<char>>;

pub fn parse(input: &str) -> Input {
    input.lines().map(|line| line.chars().collect()).collect()
}

pub fn part1(input: &Input) -> u32 {
    let mut stack = Vec::new();
    let mut count = 0;

    for (i, line) in input.iter().enumerate() {
        for (j, c) in line.iter().enumerate() {
            if *c == 'X' {
                for (di, dj) in (-1..=1).cartesian_product(-1..=1) {
                    stack.push((i as i32, j as i32, 0, di, dj));
                }
            }
        }
    }

    let n = input.len() as i32;
    let m = input[0].len() as i32;
    let chars = ['X', 'M', 'A', 'S'];

    while let Some((i, j, c, di, dj)) = stack.pop() {
        
        if i < 0 || i >= n || j < 0 || j >= m || input[i as usize][j as usize] != chars[c] {
            continue;
        }
        if c == 3 {
            count += 1;
            continue;
        }

        stack.push((i + di, j + dj, c + 1, di, dj));
    }

    count
}

pub fn part2(input: &Input) -> u32 {
    let n = input.len() as i32;
    let m = input[0].len() as i32;

    let eq = |i, j, c| i >= 0 && i < n && j >= 0 && j < m && input[i as usize][j as usize] == c;

    let mut count = 0;

    for i in 0..n {
        for j in 0..m {
            if input[i as usize][j as usize] == 'A'
                && ((eq(i - 1, j - 1, 'M') && eq(i + 1, j + 1, 'S'))
                    || (eq(i - 1, j - 1, 'S') && eq(i + 1, j + 1, 'M')))
                    && (eq(i - 1, j + 1, 'M') && eq(i + 1, j - 1, 'S'))
                        | (eq(i - 1, j + 1, 'S') && eq(i + 1, j - 1, 'M'))
                    {
                        count += 1;
                    }
        }
    }

    count
}
