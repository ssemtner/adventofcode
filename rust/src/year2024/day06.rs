use fxhash::FxHashSet;

type Input = (Vec<Vec<bool>>, (usize, usize));

const DIRS: [(i32, i32); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

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
    guard_path(grid, start).len()
}

pub fn part2((grid, start): &Input) -> usize {
    let path = guard_path(grid, start);

    let next_walls = gen_next_walls(grid);

    let mut seen = FxHashSet::default();
    path.into_iter()
        .filter(|pos| {
            seen.clear(); // reusing the hash set went from 12ms -> 4ms
            is_cycle(&next_walls, &mut seen, *start, 3, pos)
        })
        .count()
}

fn guard_path(grid: &Vec<Vec<bool>>, start: &(usize, usize)) -> FxHashSet<(usize, usize)> {
    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let (mut i, mut j) = *start;
    let mut d = 3;

    let mut visited = FxHashSet::default();
    let mut path = FxHashSet::default();

    loop {
        if visited.contains(&(i, j, d)) {
            return path;
        }

        visited.insert((i, j, d));
        path.insert((i, j));

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
            return path;
        }
    }
}

struct NextWalls {
    up: Vec<Vec<i32>>,
    down: Vec<Vec<i32>>,
    left: Vec<Vec<i32>>,
    right: Vec<Vec<i32>>,
}

fn gen_next_walls(walls: &Vec<Vec<bool>>) -> NextWalls {
    let m = walls.len();
    let n = walls[0].len();

    let mut up = vec![vec![0; n]; m];
    let mut down = vec![vec![0; n]; m];
    let mut left = vec![vec![0; n]; m];
    let mut right = vec![vec![0; n]; m];

    for j in 0..n {
        let mut last = -1i32;
        for i in 0..m {
            if walls[i][j] {
                last = i as i32 + 1;
            }
            up[i][j] = last;
        }

        let mut last = m as i32;
        for i in (0..m).rev() {
            if walls[i][j] {
                last = i as i32 - 1;
            }
            down[i][j] = last;
        }
    }

    for i in 0..m {
        let mut last = -1i32;
        for j in 0..n {
            if walls[i][j] {
                last = j as i32 + 1;
            }
            left[i][j] = last;
        }

        let mut last = n as i32;
        for j in (0..n).rev() {
            if walls[i][j] {
                last = j as i32 - 1;
            }
            right[i][j] = last;
        }
    }

    NextWalls {
        up,
        down,
        left,
        right,
    }
}

fn is_cycle(
    next_walls: &NextWalls,
    seen: &mut FxHashSet<(i32, i32, usize)>,
    (i, j): (usize, usize),
    mut d: usize,
    obstacle: &(usize, usize),
) -> bool {
    let m = next_walls.up.len() as i32;
    let n = next_walls.up[0].len() as i32;

    let (mut i, mut j) = (i as i32, j as i32);

    let obstacle_i = obstacle.0 as i32;
    let obstacle_j = obstacle.1 as i32;

    while (0..m).contains(&i) && (0..n).contains(&j) {
        if !seen.insert((i, j, d)) {
            return true;
        }

        (i, j) = match d {
            3 => {
                // UP
                let next_i = next_walls.up[i as usize][j as usize];
                if j == obstacle_j && i > obstacle_i && obstacle_i >= next_i {
                    (obstacle_i + 1, obstacle_j)
                } else {
                    (next_i, j)
                }
            }

            1 => {
                // DOWN
                let next_i = next_walls.down[i as usize][j as usize];
                if j == obstacle_j && i < obstacle_i && obstacle_i <= next_i {
                    (obstacle_i - 1, obstacle_j)
                } else {
                    (next_i, j)
                }
            }

            2 => {
                // LEFT
                let next_j = next_walls.left[i as usize][j as usize];
                if i == obstacle_i && j > obstacle_j && obstacle_j >= next_j {
                    (obstacle_i, obstacle_j + 1)
                } else {
                    (i, next_j)
                }
            }
            0 => {
                // RIGHT
                let next_j = next_walls.right[i as usize][j as usize];
                if i == obstacle_i && j < obstacle_j && obstacle_j <= next_j {
                    (obstacle_i, obstacle_j - 1)
                } else {
                    (i, next_j)
                }
            }
            _ => unreachable!(),
        };

        d = (d + 1) % 4;
    }

    false
}
