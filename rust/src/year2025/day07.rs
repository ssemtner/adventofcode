type Input = (Vec<Vec<bool>>, (usize, usize));

pub fn parse(input: &str) -> Input {
    let mut start = (0, 0);
    let grid: Vec<Vec<_>> = input
        .lines()
        .enumerate()
        .map(|(i, line)| {
            line.chars()
                .enumerate()
                .map(|(j, char)| {
                    if char == 'S' {
                        start = (i, j);
                    }
                    char == '^'
                })
                .collect()
        })
        .collect();

    return (grid, start);
}

pub fn part1((grid, (start_i, start_j)): &Input) -> u32 {
    // just simulate and count the number of splits as they happen
    let mut splits = 0;

    let n = grid.len();
    let m = grid[0].len();
    let mut beams = vec![false; m];
    beams[*start_j] = true;
    for i in *start_i + 1..n {
        let mut new_beams = vec![false; m];
        for j in 0..m {
            if beams[j] && grid[i][j] {
                splits += 1;

                if j > 0 {
                    new_beams[j - 1] = true;
                }
                if j + 1 < m {
                    new_beams[j + 1] = true;
                }
            } else if beams[j] {
                new_beams[j] = true;
            }
        }
        beams = new_beams;
    }

    splits
}

pub fn part2((grid, (start_i, start_j)): &Input) -> u64 {
    // take part 1 solution and turn it into dp where beams[j] after loop iter i is number
    // of ways to get to the position with the particle at x=j, y=i, then sum

    let n = grid.len();
    let m = grid[0].len();
    let mut beams = vec![0; m];
    beams[*start_j] = 1;
    for i in *start_i + 1..n {
        let mut new_beams = vec![0; m];
        for j in 0..m {
            if beams[j] > 0 && grid[i][j] {
                if j > 0 {
                    new_beams[j - 1] += beams[j];
                }
                if j + 1 < m {
                    new_beams[j + 1] += beams[j];
                }
            } else if beams[j] > 0 {
                new_beams[j] += beams[j];
            }
        }
        beams = new_beams;
    }

    beams.iter().sum()
}
