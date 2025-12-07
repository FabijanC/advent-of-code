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

    // The rest of input can be ignored.

    ranges.sort();

    let mut merged_ranges = vec![];

    // Start with the first range. Iterate over ranges and merge them into the current one if they
    // overlap.
    let mut current_range = ranges[0];
    for new_range in ranges.iter().skip(1) {
        if current_range.1 < new_range.0 {
            merged_ranges.push(current_range);
            current_range = *new_range;
        } else {
            current_range.1 = std::cmp::max(current_range.1, new_range.1);
        }
    }

    // Also covers the case if no elements in joint_ranges, i.e. if last() is None
    if merged_ranges.last() != Some(&current_range) {
        merged_ranges.push(current_range);
    }

    let sol: i64 = merged_ranges
        .iter()
        .map(|(lower, upper)| upper - lower + 1)
        .sum();
    println!("{sol}");
}
