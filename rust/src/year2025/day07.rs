type Input = (u32, u64);

pub fn parse(input: &str) -> Input {
    let mut iter = input.lines().skip_while(|line| !line.contains("S"));
    let start_line = iter.next().unwrap();
    let m = start_line.len();

    let mut splits = 0;
    let mut beams = vec![0; m];
    beams[start_line.find('S').unwrap()] = 1;
    for line in iter {
        let mut new_beams = vec![0; m];
        for (j, c) in line.chars().enumerate() {
            if beams[j] > 0 && c == '^' {
                splits += 1;
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
    (splits, beams.iter().sum())
}

pub fn part1(input: &Input) -> u32 {
    input.0
}

pub fn part2(input: &Input) -> u64 {
    input.1
}
