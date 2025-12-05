use std::io::{stdin, BufRead};

static ROLL: char = '@';

fn count_neighbors(field: &Vec<Vec<u8>>, i: usize, j: usize) -> u32 {
    let mut counter = 0;

    let n_rows = field.len() as i32;
    let n_cols = field[0].len() as i32;

    for di in -1..=1 {
        for dj in -1..=1 {
            if di == 0 && dj == 0 {
                continue;
            }

            let ni = i as i32 + di;
            let nj = j as i32 + dj;
            if ni < 0 || ni >= n_rows || nj < 0 || nj >= n_cols {
                continue;
            }

            if field[ni as usize][nj as usize] as char == ROLL {
                counter += 1
            }
        }
    }

    counter
}

fn main() {
    let rows: Vec<Vec<u8>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap().bytes().collect())
        .collect();

    let mut sol = 0;
    for i in 0..rows.len() {
        for j in 0..rows[0].len() {
            if rows[i][j] == ROLL as u8 && count_neighbors(&rows, i, j) < 4 {
                sol += 1;
            }
        }
    }

    println!("{sol}");
}
