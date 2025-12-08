use std::io::{stdin, BufRead};

fn add(x: i64, y: i64) -> i64 {
    x + y
}

fn mul(x: i64, y: i64) -> i64 {
    x * y
}

fn main() {
    let grid: Vec<Vec<String>> = stdin()
        .lock()
        .lines()
        .map(|l| {
            l.unwrap()
                .trim()
                .split_ascii_whitespace()
                .map(|s| s.to_string())
                .collect()
        })
        .collect();

    let n_operands = grid.len();
    let operator_i = grid.len() - 1;
    let n_equations = grid[0].len();

    let mut res_sum = 0;
    for eq_i in 0..n_equations {
        let operator_symbol = grid[operator_i][eq_i].as_str();
        let (mut eq_res, operator): (_, fn(_, _) -> _) = match operator_symbol {
            "+" => (0, add),
            "*" => (1, mul),
            invalid => panic!("Invalid operator symbol: {invalid}"),
        };

        for operand_i in 0..n_operands - 1 {
            let operand = grid[operand_i][eq_i].parse().unwrap();
            eq_res = operator(eq_res, operand);
        }

        res_sum += eq_res;
    }

    println!("{res_sum}");
}
