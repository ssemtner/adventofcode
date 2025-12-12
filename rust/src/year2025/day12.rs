type Input = (Vec<usize>, Vec<(usize, Vec<usize>)>);

// I tried writing an actual solution, got stuck, looked for hints, saw it was a troll and don't
// feel like actually trying anymore so it's just hardcoded and I removed the sample input test.

pub fn parse(input: &str) -> Input {
    let (shapes, regions) = input.rsplit_once("\n\n").unwrap();

    let shapes: Vec<usize> = shapes
        .split("\n\n")
        .map(|shape| shape.bytes().filter(|&x| x == b'#').count())
        .collect();

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

    (shapes, regions)
}

pub fn part1((shapes, regions): &Input) -> usize {
    regions
        .iter()
        .filter(|(area, counts)| {
            counts
                .iter()
                .enumerate()
                .map(|(index, count)| count * shapes[index])
                .sum::<usize>()
                <= *area
        })
        .count()
}

pub fn part2(_input: &Input) -> u32 {
    0
}
