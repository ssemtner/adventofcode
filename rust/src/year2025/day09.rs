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

pub fn part2(input: &Input) -> u64 {
    let lines: Vec<(_, _)> = input
        .iter()
        .circular_tuple_windows::<(_, _)>()
        .map(|window| [window.0, window.1].into_iter().collect_tuple().unwrap())
        .collect();

    let mut res = 0;
    for ((x1, y1), (x2, y2)) in input.iter().copied().tuple_combinations() {
        if is_inside(&lines, x1, x2, y1, y2) {
            let new_size = (x1.abs_diff(x2) + 1) * (y1.abs_diff(y2) + 1);
            if new_size > res {
                res = new_size;
            }
        }
    }

    res
}

fn is_inside(lines: &[(&(u64, u64), &(u64, u64))], x1: u64, x2: u64, y1: u64, y2: u64) -> bool {
    let miny = y1.min(y2);
    let maxy = y1.max(y2);
    let minx = x1.min(x2);
    let maxx = x1.max(x2);

    for (&(lx1, ly1), &(lx2, ly2)) in lines {
        let lminy = ly1.min(ly2);
        let lmaxy = ly1.max(ly2);
        let lminx = lx1.min(lx2);
        let lmaxx = lx1.max(lx2);
        if ly1 == ly2 {
            if miny < ly1
                && ly1 < maxy
                && ((lminx <= minx && minx < lmaxx) || (lminx < maxx && maxx <= lmaxx))
            {
                return false;
            }
        } else if lx1 == lx2 {
            if minx < lx1
                && lx1 < maxx
                && ((lminy <= miny && miny < lmaxy) || (lminy < maxy && maxy <= lmaxy))
            {
                return false;
            }
        } else {
            unreachable!();
        }
    }

    true
}
