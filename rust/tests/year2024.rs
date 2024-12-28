#[macro_use]
mod test;

mod year2024 {
    test_day!(year2024, day01,
        (sample_day1, part1: 11, part2: 31),
        (day1, part1: 1834060, part2: 21607792)
    );

    test_day!(year2024, day02,
        (sample_day2, part1: 2, part2: 4),
        (day2, part1: 472, part2: 520)
    );

    test_day!(year2024, day03,
        (sample_day3part1, part1: 161),
        (sample_day3part2, part2: 48),
        (day3, part1: 163931492, part2: 76911921)
    );
}
