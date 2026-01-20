use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

fn count_paths_to(
    label: &str,
    parents: &HashMap<String, Vec<String>>,
    count_memo: &mut HashMap<String, u32>,
) -> u32 {
    if label == "you" {
        return 1;
    }

    if let Some(old_count) = count_memo.get(label) {
        return *old_count;
    }

    let mut parent_count = 0;

    if let Some(current_parents) = parents.get(label) {
        for parent in current_parents {
            parent_count += count_paths_to(parent, parents, count_memo);
        }
    }

    count_memo.insert(label.into(), parent_count);
    parent_count
}

fn main() {
    let lines = stdin().lock().lines().map(|l| l.unwrap());
    let mut parents = HashMap::<String, Vec<String>>::new();
    for l in lines {
        let parts: Vec<_> = l.split_whitespace().collect();
        let from = parts[0].strip_suffix(':').unwrap();
        parts[1..].iter().for_each(|target| {
            let current_target_parents = parents.entry(target.to_string()).or_default();
            current_target_parents.push(from.to_string());
        });
    }

    let mut count_memo = Default::default();
    println!("{}", count_paths_to(&"out", &parents, &mut count_memo));
}
