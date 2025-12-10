use std::{
    collections::HashSet,
    io::{stdin, BufRead},
};

static START: char = 'S';
static MANIFOLD: char = '^';

fn main() {
    let lines: Vec<String> = stdin().lock().lines().map(|l| l.unwrap()).collect();

    let start_i = 0;
    let start_j = lines[start_i].find(START).unwrap();

    let mut beams = HashSet::from([start_j]);

    let mut n_splits = 0;

    for line in &lines[1..] {
        let line_chars: Vec<char> = line.chars().collect();

        let mut new_beams = HashSet::new();
        for beam_j in &beams {
            if line_chars[*beam_j] == MANIFOLD {
                new_beams.insert(beam_j - 1);
                new_beams.insert(beam_j + 1);
                n_splits += 1;
            } else {
                new_beams.insert(*beam_j);
            }
        }

        beams = new_beams
    }

    println!("{n_splits}");
}
