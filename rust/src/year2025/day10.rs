use std::collections::{HashMap, HashSet, VecDeque};

use microlp::{OptimizationDirection, Problem};

#[derive(Debug)]
pub struct Machine {
    lights: Vec<bool>,
    buttons: Vec<Vec<usize>>,
    joltage: Vec<u32>,
}

type Input = Vec<Machine>;

pub fn parse(input: &str) -> Input {
    input
        .lines()
        .map(|line| {
            let parts: Vec<_> = line.split_whitespace().collect();

            let target = parts[0];
            let buttons = &parts[1..parts.len() - 1];
            let joltage = parts[parts.len() - 1];

            Machine {
                lights: target
                    .chars()
                    .filter_map(|c| match c {
                        '.' => Some(false),
                        '#' => Some(true),
                        _ => None,
                    })
                    .collect(),
                buttons: buttons
                    .iter()
                    .map(|&button| {
                        button[1..button.len() - 1]
                            .split(",")
                            .map(|n| n.parse().unwrap())
                            .collect()
                    })
                    .collect(),
                joltage: joltage[1..joltage.len() - 1]
                    .split(",")
                    .map(|n| n.parse().unwrap())
                    .collect(),
            }
        })
        .collect()
}

pub fn part1(input: &Input) -> u32 {
    input.iter().map(lights_presses_required).sum()
}

fn lights_presses_required(machine: &Machine) -> u32 {
    let Machine {
        lights: target,
        buttons,
        joltage: _,
    } = machine;

    // just a simple bfs of states

    let mut seen: HashSet<Vec<bool>> = HashSet::new();
    let mut q = VecDeque::from([(vec![false; target.len()], 0)]);

    while let Some((state, count)) = q.pop_front() {
        if seen.contains(&state) {
            continue;
        }

        seen.insert(state.clone());

        if state == *target {
            return count;
        }

        for button in buttons {
            let mut new_state = state.clone();

            for &idx in button {
                new_state[idx] = !new_state[idx];
            }

            q.push_back((new_state, count + 1));
        }
    }
    unreachable!()
}

pub fn part2(input: &Input) -> u32 {
    input
        .iter()
        .map(
            |Machine {
                 buttons, joltage, ..
             }| {
                let mut problem = Problem::new(OptimizationDirection::Minimize);

                let mut constraints: HashMap<usize, Vec<usize>> = HashMap::new();
                for (id, button) in buttons.iter().enumerate() {
                    for &idx in button {
                        let vec = constraints.entry(idx).or_default();
                        vec.push(id);
                    }
                }

                let button_vars: Vec<_> = (0..buttons.len())
                    .map(|_| problem.add_integer_var(1.0, (0, i32::MAX)))
                    .collect();

                for (joltage_idx, button_ids) in constraints {
                    let target_joltage = joltage[joltage_idx];

                    let lhs: Vec<_> = button_ids.iter().map(|&i| (button_vars[i], 1.0)).collect();
                    problem.add_constraint(lhs, microlp::ComparisonOp::Eq, target_joltage as f64);
                }

                let solution = problem.solve().unwrap();

                button_vars
                    .iter()
                    .map(|&var| solution.var_value_rounded(var) as u32)
                    .sum::<u32>()
            },
        )
        .sum()
}
