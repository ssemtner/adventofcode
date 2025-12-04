#[macro_use]
mod test;

mod year2025 {
    test_day!(year2025, day01,
        (sample_day1, part1: 3, part2: 6),
        (day1, part1: 1154, part2: 6819)
    );

    test_day!(year2025, day02,
        (sample_day2, part1: 1227775554, part2: 4174379265),
        (day2, part1: 24747430309, part2: 30962646823)
    );

    test_day!(year2025, day03,
        (sample_day3, part1: 357, part2: 3121910778619),
        (day3, part1: 16946, part2: 168627047606506)
    );

    test_day!(year2025, day04,
        (sample_day4, part1: 13, part2: 43),
        (day4, part1: 1363, part2: 8184)
    );
}
