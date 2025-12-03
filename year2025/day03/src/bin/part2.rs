use std::io::{stdin, BufRead};

fn get_max_joltage(bank: &str, n_batteries: u32) -> u64 {
    let length = bank.len();
    let joltages: Vec<u64> = bank
        .chars()
        .map(|d| d.to_digit(10).unwrap() as u64)
        .collect();

    let mut max_bank_joltage = 0_u64;
    let mut start_i = 0 as usize;

    for batteries_remaining in (0..n_batteries).rev() {
        let mut new_max_joltage = 0;
        let mut new_max_i = 0;

        for i in start_i..(length - batteries_remaining as usize) {
            let joltage = joltages[i];
            if joltage > new_max_joltage {
                new_max_joltage = joltage;
                new_max_i = i;
            }
        }

        start_i = new_max_i + 1;
        max_bank_joltage = max_bank_joltage * 10 + new_max_joltage;
    }

    max_bank_joltage
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Expected CLI argument: <N_BATTERIES>");
        std::process::exit(1);
    }

    let n_batteries = match args[1].parse() {
        Ok(n) => n,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(2);
        }
    };

    let sol: u64 = stdin()
        .lock()
        .lines()
        .map(|line| get_max_joltage(&line.unwrap(), n_batteries))
        .sum();
    println!("{sol}");
}
