use std::io::{stdin, BufRead};

fn is_repeated(mut n: u64) -> bool {
    let mut digits = vec![];

    while n > 0 {
        let d = n % 10;
        digits.push(d);
        n /= 10;
    }

    let digits_len = digits.len();
    digits_len % 2 == 0 && digits[..digits_len / 2] == digits[digits_len / 2..]
}

fn sum_invalid(from: u64, to: u64) -> u64 {
    (from..=to).into_iter().filter(|n| is_repeated(*n)).sum()
}

fn main() {
    let mut line = String::new();
    stdin().lock().read_line(&mut line).unwrap();

    let sol: u64 = line
        .split(',')
        .map(|raw_range| {
            let range: Vec<u64> = raw_range.split('-').map(|n| n.parse().unwrap()).collect();
            assert_eq!(range.len(), 2);
            sum_invalid(range[0], range[1])
        })
        .sum();

    println!("{sol}");
}

#[cfg(test)]
mod test {
    use crate::is_repeated;

    #[test]
    fn test_is_repeated() {
        for n in [1, 2, 3, 111, 42, 24, 100, 2002] {
            assert!(!is_repeated(n))
        }
    }

    #[test]
    fn test_is_not_repeated() {
        for n in [11, 1111, 999999, 2424, 123123] {
            assert!(is_repeated(n))
        }
    }
}
