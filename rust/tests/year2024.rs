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

    test_day!(year2024, day04,
        (sample_day4, part1: 18, part2: 9),
        (day4, part1: 2536, part2: 1875)
    );

    test_day!(year2024, day05,
        (sample_day5, part1: 143, part2: 123),
        (day5, part1: 5639, part2: 5273)
    );

    test_day!(year2024, day06,
        (sample_day6, part1: 41, part2: 6),
        (day6, part1: 4977, part2: 1729)
    );

    test_day!(year2024, day07,
        (sample_day7, part1: 3749, part2: 11387),
        (day7, part1: 1260333054159, part2: 162042343638683)
    );
}
