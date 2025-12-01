use std::io::{stdin, BufRead};

fn main() {
    let lines: Vec<String> = stdin().lock().lines().map(|l| l.unwrap()).collect();
    let mut index: i32 = 50;
    let size = 100;
    let mut password = 0;
    for line in lines {
        let clicks: i32 = line[1..].parse().unwrap();
        if line.starts_with('L') {
            index = (index - clicks + size) % size;
        } else if line.starts_with('R') {
            index = (index + clicks) % size;
        } else {
            panic!("Invalid command: {line}")
        }

        if index == 0 {
            password += 1;
        }
    }

    println!("{password}");
}
