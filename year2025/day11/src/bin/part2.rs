use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

fn count_paths(
    from: &str,
    to: String,
    avoid: &[&str],
    parents: &HashMap<String, Vec<String>>,
    count_memo: &mut HashMap<String, u64>,
) -> u64 {
    if let Some(old_count) = count_memo.get(&to) {
        return *old_count;
    }

    if to == from {
        return 1;
    }

    let mut count = 0;
    for parent in parents.get(&to).unwrap_or(&vec![]) {
        if avoid.contains(&parent.as_str()) {
            continue;
        }

        count += count_paths(from, parent.clone(), avoid, parents, count_memo);
    }

    count_memo.insert(to, count);
    count
}

fn main() {
    let lines = stdin().lock().lines().map(|l| l.unwrap());
    let mut parents = HashMap::<String, Vec<String>>::new();
    for l in lines {
        let parts: Vec<_> = l.split_whitespace().collect();
        let from = parts[0].strip_suffix(':').unwrap().to_string();
        parts[1..].iter().for_each(|target| {
            let current_target_parents = parents.entry(target.to_string()).or_default();
            assert!(!current_target_parents.contains(&from));
            current_target_parents.push(from.clone());
        });
    }

    let server_to_dac = count_paths(
        "svr",
        "dac".into(),
        &["fft"],
        &parents,
        &mut Default::default(),
    );

    let dac_to_out = count_paths(
        "dac",
        "out".into(),
        &["fft"],
        &parents,
        &mut Default::default(),
    );

    let server_to_fft = count_paths(
        "svr",
        "fft".into(),
        &["dac"],
        &parents,
        &mut Default::default(),
    );

    let fft_to_out = count_paths(
        "fft",
        "out".into(),
        &["dac"],
        &parents,
        &mut Default::default(),
    );

    let fft_to_dac = count_paths("fft", "dac".into(), &[], &parents, &mut Default::default());

    // Finds no paths, therefore calculating server_to_dac and fft_to_out is needless, but left
    // for the sake of completeness.
    let dac_to_fft = count_paths("dac", "fft".into(), &[], &parents, &mut Default::default());

    println!(
        "{} * {} * {} + {} * {} * {}",
        server_to_dac, dac_to_fft, fft_to_out, server_to_fft, fft_to_dac, dac_to_out
    );
    println!(
        "= {}",
        server_to_dac * dac_to_fft * fft_to_out + server_to_fft * fft_to_dac * dac_to_out
    );
}
