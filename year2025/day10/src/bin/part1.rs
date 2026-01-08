use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

fn parse_expected_config(s: &str) -> u32 {
    assert!(s.starts_with('['));
    assert!(s.ends_with(']'));

    let mut expected = 0b0;
    let mut mask = 0b1;
    for c in s.chars().skip(1).take_while(|c| c != &']') {
        match c {
            '.' => (),
            '#' => expected |= mask,
            _ => panic!("Invalid char {c} in {s}"),
        }

        mask <<= 1;
    }

    expected
}

#[test]
fn test_parsing_expected_config() {
    for (raw, expected) in [
        ("[.##.]", 0b0110),
        ("[...#.]", 0b01000),
        ("[.###.#]", 0b101110),
    ] {
        assert_eq!(parse_expected_config(raw), expected);
    }
}

fn parse_toggler(s: &str) -> u32 {
    let mut config = 0b0;
    for d in s
        .strip_prefix('(')
        .unwrap()
        .strip_suffix(')')
        .unwrap()
        .split(',')
        .map(|d| d.parse::<u8>().unwrap())
    {
        config |= 1 << d;
    }

    config
}

#[test]
fn test_parsing_toggler() {
    for (raw, expected) in [
        ("(1,3)", 0b1010),
        ("(2)", 0b100),
        ("(2,3)", 0b1100),
        ("(0,2)", 0b101),
        ("(0,1)", 0b11),
    ] {
        assert_eq!(parse_toggler(raw), expected);
    }
}

fn calculate_push_counts(togglers: &[u32], push_counter: &mut HashMap<u32, u32>) {
    if togglers.is_empty() {
        return;
    }

    let toggler = togglers[0];
    let old_configs: Vec<_> = push_counter.keys().cloned().collect();
    for old_config in old_configs {
        let new_config = old_config ^ toggler; // Turn on what is off and vice versa
        let old_count = push_counter.get(&old_config).unwrap();
        let new_count = old_count + 1;

        match push_counter.get(&new_config) {
            Some(old_count) => {
                if &new_count < old_count {
                    push_counter.insert(new_config, new_count);
                }
            }
            None => {
                push_counter.insert(new_config, new_count);
            }
        }
    }

    calculate_push_counts(&togglers[1..], push_counter);
}

fn main() {
    let input_lines: Vec<Vec<String>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap())
        .map(|l| l.split(' ').map(|s| s.into()).collect())
        .collect();

    let mut total_pushes = 0;
    for input_line in input_lines {
        let expected_config = parse_expected_config(&input_line[0]);

        let mut togglers = vec![];

        // Ignoring the last input token
        for i in 1..input_line.len() - 1 {
            let toggler = parse_toggler(&input_line[i]);
            togglers.push(toggler);
        }

        let mut config_to_push_count = HashMap::new();
        config_to_push_count.insert(0b0, 0); // All initially off; no pushing applied
        calculate_push_counts(&togglers, &mut config_to_push_count);

        total_pushes += config_to_push_count[&expected_config];
    }

    println!("{total_pushes}");
}
