use clap::arg;
use clap::command;
use clap::value_parser;
use regex::Regex;
use std::fs;
use std::fs::read_to_string;
use std::iter::empty;
use std::path::Path;
use std::path::PathBuf;
use std::process::Command;
use std::time::Duration;
use std::time::Instant;

fn main() {
    let cmd = command!()
        .propagate_version(true)
        .arg_required_else_help(true)
        .subcommand(
            command!("scaffold")
                .arg(arg!([year]).value_parser(value_parser!(u32)).required(true))
                .arg(arg!([day]).value_parser(value_parser!(u32)).required(true)),
        )
        .subcommand(command!("all"))
        .arg(arg!([year]).value_parser(value_parser!(u32)))
        .arg(arg!([day]).value_parser(value_parser!(u32)));

    let matches = cmd.get_matches();

    match matches.subcommand() {
        Some(("scaffold", args)) => {
            scaffold_puzzle(
                *args.get_one("year").unwrap(),
                *args.get_one("day").unwrap(),
            );
        }
        Some(("all", _)) => run_puzzles(None, None),
        _ => run_puzzles(matches.get_one("year"), matches.get_one("day")),
    }
}

fn scaffold_puzzle(year: u32, day: u32) {
    let year = if year < 2000 { year + 2000 } else { year };

    // Make sure we are in the right place
    if !Path::new("Cargo.toml").exists() {
        eprintln!("Not in a cargo project");
        return;
    }

    // Create src/year{year} from cargo root if it doesn't exis
    let src = Path::new("src").join(format!("year{}", year));
    if !src.exists() {
        std::fs::create_dir(&src).unwrap();
    }

    // Create src/year{year}/day{day}.rs if it doesn't exist
    let src = src.join(format!("day{:02}.rs", day));
    if !src.exists() {
        std::fs::write(
            &src,
            r#"type Input = ();

pub fn parse(input: &str) -> Input {}

pub fn part1(input: &Input) -> u32 {
    unimplemented!()
}

pub fn part2(input: &Input) -> u32 {
    unimplemented!()
}
"#,
        )
        .unwrap();
    }

    let bench = Path::new("benches").join("bench.rs");
    let test = Path::new("tests").join(format!("year{year}.rs"));
    let main = Path::new("src").join("main.rs");
    let lib = Path::new("src").join("lib.rs");

    let day_str = format!("day{:02}", day);
    let day_replace = format!(", {})", day_str);

    // create test file if needed
    if !test.exists() {
        std::fs::write(
            &test,
            format!("#[macro_use]\nmod test;\n\nmod year{year} {{}}"),
        )
        .unwrap()
    }

    update_macro(
        &bench,
        &format!(
            r"(bench!\([ \t]*\n?[ \t]*year{},?[\s\S]*?)[ \t]*\n?[ \t]*\)",
            year
        ),
        &day_replace,
        None,
        Some(&format!("bench!(year{year});\n")),
        Some(&format!(
            r"(bench!\([ \t]*\n?[ \t]*year{},[^)]*?{}[^)]*?)[ \t]*\n?[ \t]*\)",
            year, day_str
        )),
    );

    update_macro(
        &test,
        &format!(r"(mod year{} \{{[\s\S]*?)\}}", year),
        &format!(
            r#"
    test_day!(year{}, {},
        (sample_day{day}, part1: 0, part2: 0),
        (day{day}, part1: 0, part2: 0)
    );
}}"#,
            year, day_str,
        ),
        Some(&day_str),
        None,
        None,
    );

    update_macro(
        &main,
        &format!(
            r"(runner!\([ \t]*\n?[ \t]*year{},?[\s\S]*?)[ \t]*\n?[ \t]*\)",
            year
        ),
        &day_replace,
        None,
        Some(&format!("runner!(year{year});\n")),
        Some(&format!(
            r"(runner!\([ \t]*\n?[ \t]*year{},[^)]*?{}[^)]*?)[ \t]*\n?[ \t]*\)",
            year, day_str
        )),
    );

    update_macro(
        &lib,
        &format!(
            r"(lib!\([ \t]*\n?[ \t]*year{},?[\s\S]*?)[ \t]*\n?[ \t]*\)",
            year
        ),
        &day_replace,
        None,
        Some(&format!("lib!(year{year});\n")),
        Some(&format!(
            r"(lib!\([ \t]*\n?[ \t]*year{},[^)]*?{}[^)]*?)[ \t]*\n?[ \t]*\)",
            year, day_str
        )),
    );

    update_macro(
        &main,
        &format!(r"(all_puzzles!\(year\d{{4}}(?:,\s*year\d{{4}})*)\)"),
        &format!(", year{year})"),
        None,
        None,
        Some(&format!(r"(all_puzzles!\([^)]*?year{}[^)]*?)\)", year)),
    );

    let status = Command::new("cargo").arg("fmt").status().unwrap();
    if !status.success() {
        eprintln!("Failed to run cargo fmt");
    }
}

fn update_macro(
    file: &PathBuf,
    regex: &str,
    new_arg: &str,
    alt_check: Option<&str>,
    new_template: Option<&str>,
    must_not_match: Option<&str>,
) {
    let mut text = read_to_string(file).unwrap();
    let re = Regex::new(regex).unwrap();

    if !re.is_match(&text) && new_template.is_some() {
        text.push_str(new_template.unwrap());
    }

    if must_not_match.is_some()
        && re.is_match(&text)
        && Regex::new(must_not_match.unwrap()).unwrap().is_match(&text)
    {
        return;
    }

    let updated = re.replace_all(&text, |caps: &regex::Captures| {
        let matched = &caps[0];
        if matched.contains(new_arg)
            || (alt_check.is_some() && matched.contains(alt_check.unwrap()))
        {
            return matched.to_string();
        } else {
            let group = &caps[1];

            format!("{}{}", group, new_arg)
        }
    });
    fs::write(file, updated.to_string()).unwrap();
}

macro_rules! all_puzzles {
    ($($year:ident),*) => {
        empty()
            $(.chain($year()))*
    }
}

fn run_puzzles(year: Option<&u32>, day: Option<&u32>) {
    let puzzles: Vec<_> = all_puzzles!(year2024, year2025)
        .filter(|puzzle: &Puzzle| {
            year.is_none_or(|year| {
                (*year == puzzle.year || *year + 2000 == puzzle.year)
                    && day.is_none_or(|day| *day == puzzle.day)
            })
        })
        .collect();

    let mut duration = Duration::ZERO;

    static BOLD: &str = "\x1b[1m";
    static RESET: &str = "\x1b[0m";
    static YELLOW: &str = "\x1b[33m";
    static RED: &str = "\x1b[31m";
    static WHITE: &str = "\x1b[37m";

    for Puzzle {
        year,
        day,
        path,
        exec,
    } in &puzzles
    {
        if let Ok(input) = read_to_string(path) {
            let start = Instant::now();
            let (part1, part2) = exec(&input);

            let time = start.elapsed();
            duration += time;

            println!("{BOLD}{YELLOW}{year} Day {day:02}{RESET}{YELLOW} in {time:?}{RESET}");
            println!("    Part 1: {part1}");
            println!("    Part 2: {part2}");
        } else {
            eprintln!("{BOLD}{RED}{year} Day {day:02}{RESET}");
            eprintln!("    Missing input");
            eprintln!("    Searched at {BOLD}{WHITE}{}{RESET}", path.display());
        }
    }
    println!("\n{BOLD}Total time: {duration:?}{RESET}");
}

struct Puzzle {
    year: u32,
    day: u32,
    path: PathBuf,
    exec: fn(&str) -> (String, String),
}

macro_rules! runner {
    ($year:ident, $($day:ident),*) => {
        fn $year() -> Vec<Puzzle> {
            vec![$({
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

                let exec = |input: &str| {
                    use adventofcode::$year::$day::*;

                    let input = parse(input);
                    (part1(&input).to_string(), part2(&input).to_string())
                };

                Puzzle {
                    year: year.parse().unwrap(),
                    day: day.parse().unwrap(),
                    path,
                    exec,
                }
            },)*]
        }
    }
}

runner!(year2024, day01, day02, day03, day04, day05, day06, day07, day08);
runner!(year2025, day01, day02, day03, day04, day05, day06, day07, day08);
