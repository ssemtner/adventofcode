use std::collections::VecDeque;

pub enum Cell {
    Empty,
    Paper,
}

type Input = Vec<Vec<Cell>>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| {
                    use Cell::*;
                    match c {
                        '.' => Empty,
                        '@' => Paper,
                        _ => unreachable!(),
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>()
}

pub fn part1(grid: &Input) -> u32 {
    let mut res = 0;
    let n = grid.len();
    let m = grid[0].len();
    for i in 0..n {
        for j in 0..m {
            if !matches!(grid[i][j], Cell::Paper) {
                continue;
            }

            let mut adj = 0;

            let i0 = i.saturating_sub(1);
            let i1 = (i + 1).min(n - 1);
            let j0 = j.saturating_sub(1);
            let j1 = (j + 1).min(m - 1);

            for ii in i0..=i1 {
                for jj in j0..=j1 {
                    if (ii, jj) == (i, j) {
                        continue;
                    }
                    if matches!(grid[ii][jj], Cell::Paper) {
                        adj += 1;
                    }
                }
            }

            if adj < 4 {
                res += 1;
            }
        }
    }

    res
}

pub fn part2(grid: &Input) -> u32 {
    let n = grid.len();
    let m = grid[0].len();

    let mut adj = vec![vec![None; m as usize]; n as usize];

    let mut q = VecDeque::new();

    for i in 0..n {
        for j in 0..m {
            if !matches!(grid[i][j], Cell::Paper) {
                adj[i][j] = None;
                continue;
            }

            let i0 = i.saturating_sub(1);
            let i1 = (i + 1).min(n - 1);
            let j0 = j.saturating_sub(1);
            let j1 = (j + 1).min(m - 1);

            let mut count = 0;

            for ii in i0..=i1 {
                for jj in j0..=j1 {
                    if (ii, jj) == (i, j) {
                        continue;
                    }
                    if matches!(grid[ii][jj], Cell::Paper) {
                        count += 1;
                    }
                }
            }

            adj[i][j] = Some(count);
            if count < 4 {
                q.push_back((i, j));
            }
        }
    }

    let mut moved = 0;
    while let Some((i, j)) = q.pop_front() {
        if adj[i][j].is_none() {
            continue;
        }

        adj[i][j] = None;
        moved += 1;

        let i0 = i.saturating_sub(1);
        let i1 = (i + 1).min(n - 1);
        let j0 = j.saturating_sub(1);
        let j1 = (j + 1).min(m - 1);

        for ii in i0..=i1 {
            for jj in j0..=j1 {
                if (ii, jj) == (i, j) {
                    continue;
                }
                if let Some(prev) = adj[ii][jj] {
                    adj[ii][jj] = Some(prev - 1);
                    if prev - 1 < 4 {
                        q.push_back((ii, jj));
                    }
                }
            }
        }
    }

    moved
}
