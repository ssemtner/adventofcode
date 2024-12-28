#[macro_export]
macro_rules! run_test {
    ($year:ident, $file:ident, $expected:expr, $part:ident) => {
        let year = &stringify!($year)[4..];
        let path = format!(
            "../{}/data/{}.txt",
            year,
            stringify!($file).replace("_", "/")
        );
        let input = std::fs::read_to_string(path).unwrap();
        let input = parse(&input);
        assert_eq!($part(&input), $expected);
    };
}

#[macro_export]
macro_rules! test_day {
    ($year:ident, $day:ident, $(($file:ident $(, part1: $expected1:expr)? $(, part2: $expected2:expr)?)),+ $(,)?) => {
        mod $day {
            use adventofcode::$year::$day::*;

            $(

                mod $file {
                    use super::*;

                    $(
                        #[test]
                        fn test_part1() {
                            run_test!($year, $file, $expected1, part1);
                        }
                    )?

                    $(
                        #[test]
                        fn test_part2() {
                            run_test!($year, $file, $expected2, part2);
                        }
                    )?
                }
            )+

        }
    };
}
