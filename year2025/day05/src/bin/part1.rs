use std::io::{stdin, BufRead};

fn main() {
    let mut stdin_lock = stdin().lock();

    let mut ranges: Vec<(i64, i64)> = vec![];
    loop {
        let mut line = String::new();
        stdin_lock.read_line(&mut line).unwrap();

        if line == "\n" {
            break;
        }

        let raw_range: Vec<&str> = line.trim().split("-").collect();
        let range = match raw_range[..] {
            [lower, upper] => {
                assert!(lower <= upper, "{lower} <= {upper}");
                (lower.parse().unwrap(), upper.parse().unwrap())
            }
            _ => panic!("Invalid pattern: {raw_range:?}"),
        };

        ranges.push(range);
    }

    let mut sol = 0;
    loop {
        let mut line = String::new();
        if stdin_lock.read_line(&mut line).unwrap() == 0 {
            // EOF
            break;
        }

        let id: i64 = line.trim().parse().unwrap();

        for (lower, upper) in &ranges {
            if lower <= &id && &id <= upper {
                sol += 1;
                break; // count only once
            }
        }
    }

    println!("{sol}");
}
