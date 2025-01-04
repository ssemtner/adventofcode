use fxhash::FxHashMap;

type Input = (FxHashMap<u8, Vec<(usize, usize)>>, usize, usize);

pub fn parse(input: &str) -> Input {
    let mut antennas: FxHashMap<u8, Vec<(usize, usize)>> = FxHashMap::default();

    for (i, line) in input.lines().enumerate() {
        for (j, c) in line.chars().enumerate() {
            if c != '.' {
                antennas.entry(c as u8).or_default().push((i, j));
            }
        }
    }

    (
        antennas,
        input.lines().count(),
        input.lines().next().unwrap().chars().count(),
    )
}

pub fn part1(input: &Input) -> u32 {
    let (_, n, m) = input;
    solve(
        input,
        |antinodes: &mut Vec<Vec<bool>>, x: usize, y: usize, dx: isize, dy: isize| {
            if let Some(xx) = x.checked_add_signed(dx) {
                if let Some(yy) = y.checked_add_signed(dy) {
                    if xx < *n && yy < *m {
                        antinodes[xx][yy] = true;
                    }
                }
            }
        },
    )
}

pub fn part2(input: &Input) -> u32 {
    let (_, n, m) = input;
    solve(
        input,
        |antinodes: &mut Vec<Vec<bool>>, x: usize, y: usize, dx: isize, dy: isize| {
            let mut x = x as isize;
            let mut y = y as isize;
            while x >= 0 && y >= 0 && x < *n as isize && y < *m as isize {
                antinodes[x as usize][y as usize] = true;
                x += dx;
                y += dy;
            }
        },
    )
}

fn solve<F>((antennas, n, m): &Input, add: F) -> u32
where
    F: Fn(&mut Vec<Vec<bool>>, usize, usize, isize, isize),
{
    let mut antinodes = vec![vec![false; *m]; *n];

    for (_, positions) in antennas {
        for pos1 in positions {
            for pos2 in positions {
                if pos1 != pos2 {
                    let (x1, y1) = *pos1;
                    let (x2, y2) = *pos2;

                    let dx = x1 as isize - x2 as isize;
                    let dy = y1 as isize - y2 as isize;

                    add(&mut antinodes, x1, y1, dx, dy);
                    add(&mut antinodes, x2, y2, -dx, -dy);
                }
            }
        }
    }

    antinodes.into_iter().flatten().filter(|&x| x).count() as u32
}
