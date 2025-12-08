use std::io::{stdin, BufRead};

fn add(x: i64, y: i64) -> i64 {
    x + y
}

fn mul(x: i64, y: i64) -> i64 {
    x * y
}

fn transpose(m: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut transposed = vec![];
    for j in 0..m[0].len() {
        let mut t_row = vec![];
        for i in 0..m.len() {
            t_row.push(m[i][j]);
        }

        transposed.push(t_row)
    }

    transposed
}

fn chars_to_num_str(chars: &[char]) -> String {
    chars.iter().filter(|c| c.is_digit(10)).collect()
}

fn main() {
    let grid: Vec<Vec<char>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap().bytes().map(|b| b as char).collect())
        .collect();

    let grid = transpose(&grid);

    let operator_i = grid[0].len() - 1;
    let n_digits = grid[0].len() - 1;

    let mut res_sum = 0;

    let mut i = 0;
    let n_rows = grid.len();
    while i < n_rows {
        let chars = &grid[i][..n_digits];
        let operator_symbol = grid[i][operator_i];

        i += 1;
        let mut eq_res = chars_to_num_str(chars).parse().unwrap();

        let operator: fn(_, _) -> _ = match operator_symbol {
            '+' => add,
            '*' => mul,
            invalid => panic!("Invalid operator symbol: {invalid}"),
        };

        while i < n_rows {
            let operand_raw = chars_to_num_str(&grid[i]);
            i += 1;
            if operand_raw == "" {
                // End of equation
                break;
            }

            let operand = operand_raw.parse().unwrap();
            eq_res = operator(eq_res, operand);
        }

        res_sum += eq_res;
    }

    println!("{res_sum}");
}
