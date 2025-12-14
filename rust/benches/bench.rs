use criterion::{criterion_group, criterion_main, Criterion};
use std::fs::read_to_string;
use std::hint::black_box;
use std::path::Path;
use std::sync::LazyLock;

macro_rules! bench {
    ($c:expr, $year:tt, $($day:tt),*) => {
        mod $year {
            use super::*;

            $(
                pub mod $day {
                    use super::*;
                    use adventofcode::$year::$day::*;

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

                    pub fn bench(c: &mut Criterion) {
                        let mut group = c.benchmark_group(format!("{}/{}", stringify!($year), stringify!($day)));

                        group.bench_function("parse", |b| b.iter(|| black_box(parse(black_box(&INPUT)))));

                        let input = parse(&INPUT);

                        group.bench_function("part1", |b| b.iter(|| black_box(part1(black_box(&input)))));
                        group.bench_function("part2", |b| b.iter(|| black_box(part2(black_box(&input)))));

                        group.bench_function("total", |b| {
                            b.iter(|| {
                                let input = parse(black_box(&INPUT));
                                black_box((part1(&input), part2(&input)));
                            })
                        });

                        group.finish();
                    }

                    pub fn run_all() {
                        let input = parse(black_box(&INPUT));
                        black_box((part1(&input), part2(&input)));
                    }
                }
            )*

            pub fn bench_year(c: &mut Criterion) {
                $(
                    $day::bench(c);
                )*

                c.bench_function(stringify!($year), |b| b.iter(|| {
                    $(
                        $day::run_all();
                    )*
                }));
            }
        }

        $year::bench_year($c);
    }
}

fn aoc_benches(c: &mut Criterion) {
    bench!(c, year2024, day01, day02, day03, day04, day05, day06, day07, day08);
    bench!(
        c, year2025, day01, day02, day03, day04, day05, day06, day07, day08, day09, day10, day11,
        day12
    );
}

criterion_group!(benches, aoc_benches);
criterion_main!(benches);
