use std::collections::{HashMap, VecDeque};

use itertools::Itertools;

type Input = Vec<(u64, u64)>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            line.split(",")
                .map(|num| num.parse().unwrap())
                .collect_tuple()
                .unwrap()
        })
        .collect()
}

pub fn part1(input: &Input) -> u64 {
    input
        .iter()
        .tuple_combinations()
        .map(|(p1, p2)| (p1.0.abs_diff(p2.0) + 1) * (p1.1.abs_diff(p2.1) + 1))
        .max()
        .unwrap()
}

// Trying to use an enum here is probably a terrible idea
#[derive(Debug, Clone)]
enum Cell {
    Unknown,
    Inner,
    Outer,
    Prefix(u64),
}

macro_rules! prefix_unwrap {
    ($e:expr) => {
        match $e {
            Cell::Prefix(v) => v,
            Cell::Outer => &0,
            other => panic!("Expected Prefix, got {:?}", other),
        }
    };
}

pub fn part2(input: &Input) -> u64 {
    // Get compressed version of the grid
    let compressed_x = compress(&input, |(x, _)| x);
    let compressed_y = compress(&input, |(_, y)| y);
    let x_len = compressed_x.len();
    let y_len = compressed_y.len();
    let compressed: Vec<_> = input
        .iter()
        .map(|(x, y)| (compressed_x[x], compressed_y[y]))
        .collect();

    let mut grid = vec![vec![Cell::Unknown; y_len]; x_len];

    // Set all lines as inner
    for (p1, p2) in compressed.iter().circular_tuple_windows() {
        let (x0, y0, x1, y1) = min_max(p1, p2);

        for x in x0..=x1 {
            for y in y0..=y1 {
                grid[x][y] = Cell::Inner;
            }
        }
    }

    // Flood fill outside
    let mut todo = VecDeque::from([(0usize, 0usize)]);
    while let Some((x, y)) = todo.pop_front() {
        let neighbors = [
            (x.wrapping_sub(1), y),
            (x + 1, y),
            (x, y.wrapping_sub(1)),
            (x, y + 1),
        ];

        for (xx, yy) in neighbors {
            if xx < x_len && yy < y_len {
                if matches!(grid[xx][yy], Cell::Unknown) {
                    grid[xx][yy] = Cell::Outer;
                    todo.push_back((xx, yy));
                }
            }
        }
    }

    // Prefix sum: grid[x][y] = num cells from (1,1) to (x,y)
    for y in 1..y_len {
        for x in 1..x_len {
            let val = match grid[x][y] {
                Cell::Unknown => 1,
                Cell::Inner => 1,
                Cell::Outer => 0,
                Cell::Prefix(_) => unreachable!(),
            };

            grid[x][y] = Cell::Prefix(
                val + prefix_unwrap!(&grid[x][y - 1]) + prefix_unwrap!(&grid[x - 1][y])
                    - prefix_unwrap!(&grid[x - 1][y - 1]),
            );
        }
    }

    let mut area = 0;

    for ((i, p1), (j, p2)) in compressed.iter().enumerate().tuple_combinations() {
        let (x0, y0, x1, y1) = min_max(p1, p2);

        let math = ((x1 - x0 + 1) * (y1 - y0 + 1)) as u64;

        if let Some(prefix) = (prefix_unwrap!(&grid[x1][y1])
            + prefix_unwrap!(&grid[x0 - 1][y0 - 1]))
        .checked_sub(prefix_unwrap!(&grid[x0 - 1][y1]) + prefix_unwrap!(&grid[x1][y0 - 1]))
        {
            if math == prefix {
                let (x0, y0) = input[i];
                let (x1, y1) = input[j];
                area = area.max((x0.abs_diff(x1) + 1) * (y0.abs_diff(y1) + 1));
            }
        }
    }

    return area;
}

fn compress<F>(points: &[(u64, u64)], getter: F) -> HashMap<u64, usize>
where
    F: Fn(&(u64, u64)) -> &u64,
{
    points
        .iter()
        .map(getter)
        .chain(&[u64::MAX, u64::MIN])
        .sorted_unstable()
        .dedup()
        .enumerate()
        .map(|(i, &n)| (n, i))
        .collect()
}

fn min_max<T: Ord + Copy>((x1, y1): &(T, T), (x2, y2): &(T, T)) -> (T, T, T, T) {
    (
        (*x1).min(*x2),
        (*y1).min(*y2),
        (*x1).max(*x2),
        (*y1).max(*y2),
    )
}
