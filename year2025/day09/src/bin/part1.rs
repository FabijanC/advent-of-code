use std::io::{stdin, BufRead};

fn main() {
    let pairs: Vec<Vec<u64>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap())
        .map(|l| {
            let pair: Vec<_> = l.split(',').map(|n| n.parse().unwrap()).collect();
            assert_eq!(pair.len(), 2);
            pair
        })
        .collect();

    let n_pairs = pairs.len();
    let mut max_area = 0;
    for i in 0..n_pairs {
        for j in (1 + 1)..n_pairs {
            let area = (pairs[i][0].abs_diff(pairs[j][0]) + 1) * (pairs[i][1].abs_diff(pairs[j][1]) + 1);
            if area > max_area {
                max_area = area;
            }
        }
    }

    println!("{max_area}");
}
