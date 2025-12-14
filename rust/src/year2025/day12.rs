type Input = Vec<(usize, Vec<usize>)>;

pub fn parse(input: &str) -> Input {
    let (_shapes, regions) = input.rsplit_once("\n\n").unwrap();

    let regions = regions
        .lines()
        .map(|line| {
            let (size, counts) = line.split_once(":").unwrap();
            let area = size
                .split("x")
                .map(|val| val.parse::<usize>().unwrap())
                .product();
            let counts = counts
                .split_whitespace()
                .map(|val| val.parse().unwrap())
                .collect();
            (area, counts)
        })
        .collect();

    regions
}

pub fn part1(regions: &Input) -> usize {
    regions
        .iter()
        .filter(|(area, counts)| counts.iter().map(|count| count * 9).sum::<usize>() <= *area)
        .count()
}

pub fn part2(_input: &Input) -> u32 {
    0
}
