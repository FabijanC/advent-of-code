use std::io::{stdin, BufRead};

fn get_max_joltage(bank: &str) -> u32 {
    let length = bank.len();
    let joltages: Vec<u32> = bank.chars().map(|d| d.to_digit(10).unwrap()).collect();

    let mut max_i = 0;
    let mut max_joltage = 0;
    for (i, joltage) in joltages.iter().enumerate() {
        if i == length - 1 {
            continue;
        }

        // Must not be >=, we need the first occurrence
        if *joltage > max_joltage {
            max_joltage = *joltage;
            max_i = i;
        }
    }

    let max_right = joltages.iter().skip(max_i + 1).max().unwrap();

    max_joltage * 10 + max_right
}

fn main() {
    let sol: u32 = stdin()
        .lock()
        .lines()
        .map(|line| get_max_joltage(&line.unwrap()))
        .sum();
    println!("{sol}");
}
