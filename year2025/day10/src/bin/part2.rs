use std::io::{stdin, BufRead};

use good_lp::{
    constraint, scip as solver, variable, Constraint, Expression, ProblemVariables,
    Solution, SolverModel,
};

fn parse_toggler(s: &str) -> Vec<usize> {
    s.strip_prefix('(')
        .unwrap()
        .strip_suffix(')')
        .unwrap()
        .split(',')
        .map(|d| d.parse().unwrap())
        .collect()
}

#[test]
fn test_parsing_toggler() {
    for (raw, expected) in [
        ("(1,3)", vec![1, 3]),
        ("(2)", vec![2]),
        ("(2,3)", vec![2, 3]),
        ("(0,2)", vec![0, 2]),
        ("(0,1)", vec![0, 1]),
    ] {
        assert_eq!(parse_toggler(raw), expected);
    }
}

fn parse_requirements(s: &str) -> Vec<i32> {
    s.strip_prefix('{')
        .unwrap()
        .strip_suffix('}')
        .unwrap()
        .split(',')
        .map(|el| el.parse().unwrap())
        .collect()
}

#[test]
fn test_parsing_requirements() {
    for (raw, expected) in [
        ("{3,5,4,7}", vec![3, 5, 4, 7]),
        ("{7,5,12,7,2}", vec![7, 5, 12, 7, 2]),
    ] {
        assert_eq!(parse_requirements(raw), expected);
    }
}

fn parse_togglers(raw_togglers: &[String], n_targets: usize) -> (Vec<Vec<usize>>, usize) {
    let mut target_to_source_togglers = vec![vec![]; n_targets];

    let togglers: Vec<_> = raw_togglers.iter().map(|s| parse_toggler(s)).collect();

    for (toggler_i, toggler) in togglers.iter().enumerate() {
        for target_i in toggler {
            let source_togglers = &mut target_to_source_togglers[*target_i];
            source_togglers.push(toggler_i);
        }
    }

    (target_to_source_togglers, togglers.len())
}

fn prepare_non_negative_variables(n_vars: usize) -> ProblemVariables {
    let mut lp_variables = ProblemVariables::new();

    for _ in 0..n_vars {
        lp_variables.add(variable().integer().min(0));
    }

    lp_variables
}

fn find_min_sum(lp_variables: ProblemVariables, constraints: Vec<Constraint>) -> f64 {
    let objective: Expression = lp_variables.iter_variables_with_def().map(|(v, _)| v).sum();
    let solution = lp_variables
        .minimise(&objective)
        .using(solver)
        .with_all(constraints)
        .solve()
        .unwrap();

    solution.eval(objective)
}

fn main() {
    let input_lines: Vec<Vec<String>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap())
        .map(|l| l.split(' ').map(|s| s.into()).collect())
        .collect();

    let mut sol = 0.0;

    // Element at 0 is ignored; the last element holds requirements. Between are the togglers
    for line in input_lines {
        let target_requirements = parse_requirements(line.last().unwrap());

        let (target_to_source_togglers, n_togglers) =
            parse_togglers(&line[1..line.len() - 1], target_requirements.len());

        let lp_variables = prepare_non_negative_variables(n_togglers);
        let variables_vec: Vec<_> = lp_variables
            .iter_variables_with_def()
            .map(|(v, _)| v)
            .collect();

        let mut constraints = vec![];
        for (target_i, source_togglers) in target_to_source_togglers.iter().enumerate() {
            let constraint_lhs = source_togglers
                .iter()
                .map(|toggler_i| variables_vec[*toggler_i])
                .sum::<Expression>();
            let constraint_rhs = target_requirements[target_i];
            constraints.push(constraint!(constraint_lhs == constraint_rhs));
        }

        sol += find_min_sum(lp_variables, constraints);
    }

    println!("{sol}");
}
