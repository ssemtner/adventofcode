use fxhash::FxHashSet;

type Input = (Vec<Vec<bool>>, (usize, usize));

pub fn parse(input: &str) -> Input {
    let mut start = (0, 0);
    let grid = input
        .lines()
        .enumerate()
        .map(|(i, line)| {
            line.chars()
                .enumerate()
                .map(|(j, c)| {
                    if c == '^' {
                        start = (i, j);
                    }
                    c == '#'
                })
                .collect()
        })
        .collect();

    (grid, start)
}

pub fn part1((grid, start): &Input) -> usize {
    simulate(grid, start)
        .0
        .iter()
        .flatten()
        .filter(|&&b| b)
        .count()
}

fn simulate(grid: &Vec<Vec<bool>>, start: &(usize, usize)) -> (Vec<Vec<bool>>, bool) {
    const DIRS: [(i32, i32); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let (mut i, mut j) = *start;
    let mut d = 3;

    let mut visited = FxHashSet::default();
    let mut squares = vec![vec![false; m as usize]; n as usize];

    loop {
        if visited.contains(&(i, j, d)) {
            return (squares, true);
        }

        visited.insert((i, j, d));
        squares[i][j] = true;

        let ii = i as i32 + DIRS[d].0;
        let jj = j as i32 + DIRS[d].1;

        if ii >= 0 && ii < n && jj >= 0 && jj < m {
            if grid[ii as usize][jj as usize] {
                d = (d + 1) % 4;
            } else {
                i = ii as usize;
                j = jj as usize;
            }
        } else {
            return (squares, false);
        }
    }
}

pub fn part2((grid, start): &Input) -> usize {
    let (possible, _) = simulate(grid, start);

    grid.iter()
        .enumerate()
        .map(|(i, row)| {
            let i = &i;
            row.iter()
                .enumerate()
                .filter_map(|(j, _)| {
                    if possible[*i][j] && !grid[*i][j] {
                        let mut copy = grid.clone();
                        copy[*i][j] = true;
                        Some(simulate(&copy, start).1 as usize)
                    } else {
                        None
                    }
                })
                .sum::<usize>()
        })
        .sum()
}
