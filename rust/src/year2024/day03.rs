use regex::Regex;

type Input<'a> = Vec<regex::Captures<'a>>;

pub fn parse(input: &str) -> Input<'_> {
    let re = Regex::new(r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)").unwrap();
    re.captures_iter(input).collect::<Vec<_>>()
}

pub fn part1(input: &Input) -> u32 {
    let mut sum = 0;
    for cap in input {
        if cap.get(1).is_some() {
            let a = cap.get(1).unwrap().as_str().parse::<u32>().unwrap();
            let b = cap.get(2).unwrap().as_str().parse::<u32>().unwrap();
            sum += a * b;
        }
    }

    sum
}

pub fn part2(input: &Input) -> u32 {
    let mut sum = 0;
    let mut enabled = true;
    for cap in input {
        if enabled && cap.get(1).is_some() {
            let a = cap.get(1).unwrap().as_str().parse::<u32>().unwrap();
            let b = cap.get(2).unwrap().as_str().parse::<u32>().unwrap();
            sum += a * b;
        } else if cap.get(3).is_some() {
            enabled = true;
        } else if cap.get(4).is_some() {
            enabled = false;
        }
    }

    sum
}
