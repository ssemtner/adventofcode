#![allow(unstable_features)]
#![feature(test)]
extern crate test;

macro_rules! bench {
    ($year:tt, $($day:tt),*) => {
        mod $year {
            $(
                mod $day {
                    use adventofcode::$year::$day::*;
                    use std::fs::read_to_string;
                    use std::path::Path;
                    use std::sync::LazyLock;
                    use test::Bencher;

                    static INPUT: LazyLock<String> = LazyLock::new(|| {
                        let year = &stringify!($year)[4..];
                        let day = {
                            let day = &stringify!($day)[3..];
                            if day.starts_with("0") {
                                &day[1..]
                            } else {
                                day
                            }
                        };

                        let path = Path::new("..")
                            .join(year)
                            .join("data")
                            .join(format!("day{}.txt", day));
                        read_to_string(path).unwrap()
                    });

                    #[bench]
                    fn parse_bench(bencher: &mut Bencher) {
                        bencher.iter(|| parse(&INPUT));
                    }

                    #[bench]
                    fn part1_bench(bencher: &mut Bencher) {
                        let input = parse(&INPUT);
                        bencher.iter(|| part1(&input));
                    }

                    #[bench]
                    fn part2_bench(bencher: &mut Bencher) {
                        let input = parse(&INPUT);
                        bencher.iter(|| part2(&input));
                    }
                }
            )*
        }
    }
}

bench!(year2024, day01, day02, day03, day04, day05, day06, day07, day08);
bench!(year2025, day01, day02);
