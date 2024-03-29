use regex::Regex;
use std::{
    cmp::max,
    collections::HashMap,
    io::{stdin, BufRead},
};

#[derive(Debug)]
struct Valve {
    rate: i32,
    children: Vec<u8>,
}

fn contains(storage: u64, value: u8) -> bool {
    storage & (1 << value) != 0
}

fn store(storage: &mut u64, value: u8) {
    *storage |= 1 << value
}

type Configuration = (u8, i32, u64);

fn find_max_pressure(
    valves: &HashMap<u8, Valve>,
    valve_id: u8,
    time_left: i32,
    open: u64,
    accumulated_rate: i32,
    memo: &mut HashMap<Configuration, i32>,
) -> i32 {
    if time_left <= 0 {
        return 0;
    }

    // this should check if number of opened valves equals the number of valves worth opening (those with rate > 0)
    // if open.count_ones() == 15 {
    //     return time_left * accumulated_rate;
    // }

    let configuration: Configuration = (valve_id, time_left, open);
    if memo.contains_key(&configuration) {
        return memo[&configuration];
    }

    let valve = &valves[&valve_id];
    let mut max_pressure = 0;

    // 1. option: if possible, open the valve
    if !contains(open, valve_id) && valve.rate > 0 && time_left >= 1 {
        let mut open = open;
        store(&mut open, valve_id);
        max_pressure = max(
            max_pressure,
            accumulated_rate
                + find_max_pressure(
                    valves,
                    valve_id,
                    time_left - 1,
                    open,
                    accumulated_rate + valve.rate,
                    memo,
                ),
        );
    }

    // 2. case: move to child valve
    for child_id in valve.children.iter() {
        max_pressure = max(
            max_pressure,
            accumulated_rate
                + find_max_pressure(
                    valves,
                    *child_id,
                    time_left - 1,
                    open,
                    accumulated_rate,
                    memo,
                ),
        );
    }

    memo.insert(configuration, max_pressure);
    return max_pressure;
}

/**
 * First used name will get id=0, etc.
 */
fn valve_name_to_id(name: &str, memo: &mut HashMap<String, u8>) -> u8 {
    match memo.get(name) {
        Some(id) => return *id,
        None => {
            let new_id = memo.len() as u8;
            memo.insert(name.to_string(), new_id);
            return new_id;
        }
    }
}

fn main() {
    let re =
        Regex::new("^Valve (.+) has flow rate=(.+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.+)$")
            .unwrap();

    // replace string name with u8 id for better performance
    let mut valve_name_to_id_memo: HashMap<String, u8> = HashMap::new();

    let valves: HashMap<u8, Valve> = stdin()
        .lock()
        .lines()
        .map(|line| line.expect("Could not read line"))
        .map(|line| {
            re.captures(line.as_str()).map(|caps| {
                // pairs of (name, valve) to construct a map
                let valve_name =
                    valve_name_to_id(caps.get(1).unwrap().as_str(), &mut valve_name_to_id_memo);
                (
                    valve_name,
                    Valve {
                        rate: caps.get(2).unwrap().as_str().parse().unwrap(),
                        children: caps
                            .get(3)
                            .unwrap()
                            .as_str()
                            .split(", ")
                            .map(|name| valve_name_to_id(name, &mut valve_name_to_id_memo))
                            .collect(),
                    },
                )
            })
        })
        .map(|name_and_valve| name_and_valve.unwrap())
        .collect();

    let start_id = valve_name_to_id("AA", &mut valve_name_to_id_memo);
    let time_left = 30;
    let open = 0u64;
    let accumulated_rate = 0;
    let mut memo: HashMap<Configuration, i32> = HashMap::new();
    let sol = find_max_pressure(
        &valves,
        start_id,
        time_left,
        open,
        accumulated_rate,
        &mut memo,
    );
    println!("{sol}");
}
