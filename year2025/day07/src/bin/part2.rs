use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

static START: char = 'S';
static MANIFOLD: char = '^';

fn main() {
    let lines: Vec<String> = stdin().lock().lines().map(|l| l.unwrap()).collect();

    let start_i = 0;
    let start_j = lines[start_i].find(START).unwrap();

    let mut beams = HashMap::from([(start_j, 1)]);

    for line in &lines[1..] {
        let line_chars: Vec<char> = line.chars().collect();

        let mut new_beams = HashMap::<usize, u64>::new();
        for (beam_j, beam_cnt) in &beams {
            if line_chars[*beam_j] == MANIFOLD {
                new_beams
                    .entry(beam_j - 1)
                    .and_modify(|e| *e += *beam_cnt)
                    .or_insert(*beam_cnt);

                new_beams
                    .entry(beam_j + 1)
                    .and_modify(|e| *e += *beam_cnt)
                    .or_insert(*beam_cnt);
            } else {
                new_beams
                    .entry(*beam_j)
                    .and_modify(|e| *e += *beam_cnt)
                    .or_insert(*beam_cnt);
            }
        }

        beams = new_beams
    }

    println!("{}", beams.values().sum::<u64>());
}
