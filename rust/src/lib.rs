macro_rules! lib {
    ($year:tt, $($day:tt),*) => {
        pub mod $year {$(pub mod $day;)*}
    }
}

lib!(year2024, day01, day02, day03, day04, day05, day06, day07, day08);
lib!(year2025, day01, day02, day03, day04, day05, day06);
