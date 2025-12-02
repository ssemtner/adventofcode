use itertools::Itertools;

type Input = Vec<(u64, u64)>;

pub fn parse(input: &str) -> Input {
    input
        .split(",")
        .map(|part| {
            part.split("-")
                .map(|num| num.trim().parse().unwrap())
                .collect_tuple()
        })
        .collect::<Option<_>>()
        .unwrap()
}

// I stole this answer from this smart person
// I did brute force to actually solve it day of, but this was a fun syntax exercise
// https://github.com/jimm89/AdventOfCode2025/blob/main/Day%202/Day%202.ipynb

pub fn part1(input: &Input) -> u64 {
    input.iter().fold(0, |acc_outer, (lo, hi)| {
        let lo_len = lo.to_string().len();
        let hi_len = hi.to_string().len();
        (lo_len..=hi_len).fold(acc_outer, |acc, length| {
            if length & 1 == 1 {
                return acc;
            }

            let lo_half = 10u64.pow(length as u32 / 2 - 1);
            let hi_half = 10 * lo_half - 1;

            let min = if length > lo_len {
                lo_half
            } else {
                let m = lo / (lo_half * 10);
                if (m * (10 * lo_half + 1)) < *lo {
                    m + 1
                } else {
                    m
                }
            };

            let max = if length < hi_len {
                hi_half
            } else {
                let m = hi / (lo_half * 10);
                if (m * (10 * lo_half + 1)) > *hi {
                    m - 1
                } else {
                    m
                }
            };

            acc + ((max * (max + 1) / 2) - ((min - 1) * min / 2)) * (10 * lo_half + 1)
        })
    })
}

pub fn part2(input: &Input) -> u64 {
    input.iter().fold(0, |acc_outer, (lo, hi)| {
        let lo_len = lo.to_string().len();
        let hi_len = hi.to_string().len();
        (lo_len..=hi_len).fold(acc_outer, |acc, length| {
            let rep_counts = (1..=length / 2)
                .map(|rep_len| {
                    if length % rep_len != 0 {
                        0
                    } else {
                        let rep = (length / rep_len) as u32;

                        let lo_rep = 10u64.pow(length as u32 / rep - 1);
                        let hi_rep = 10 * lo_rep - 1;

                        let min = if length > lo_len {
                            lo_rep
                        } else {
                            let m = lo / (lo_rep * 10).pow(rep - 1);
                            let mut tmp = m;

                            for _ in 0..(rep - 1) {
                                tmp = tmp * (10 * lo_rep) + m
                            }
                            if tmp < *lo {
                                m + 1
                            } else {
                                m
                            }
                        };

                        let max = if length < hi_len {
                            hi_rep
                        } else {
                            let m = hi / (lo_rep * 10).pow(rep - 1);
                            let mut tmp = m;

                            for _ in 0..(rep - 1) {
                                tmp = tmp * (10 * lo_rep) + m
                            }
                            if tmp > *hi {
                                m - 1
                            } else {
                                m
                            }
                        };

                        let range_sum = (max * (max + 1) / 2) - ((min - 1) * min / 2);
                        (0..(rep - 1)).fold(range_sum, |ret, _| ret * (10 * lo_rep) + range_sum)
                    }
                })
                .collect::<Vec<_>>();

            acc + rep_counts
                .iter()
                .enumerate()
                .map(|(index, val)| (index + 1, val))
                .filter(|(rep_len, _)| length % rep_len == 0)
                .map(|(rep_len, count)| {
                    count
                        - (1..rep_len)
                            .filter(|l| rep_len % l == 0)
                            .map(|l| rep_counts[l - 1])
                            .sum::<u64>()
                })
                .sum::<u64>()
        })
    })
}
