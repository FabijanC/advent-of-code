use std::{
    collections::HashSet,
    io::{stdin, BufRead},
};

static ROLL: char = '@';
static EMPTY: char = '.';

static NEIGHBOR_LIMIT: u32 = 4;

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

fn remove(field: &mut Vec<Vec<u8>>, removables: &HashSet<(usize, usize)>) {
    for (removable_i, removable_j) in removables {
        field[*removable_i][*removable_j] = EMPTY as u8;
    }
}

fn collect_removable_neighbors(
    field: &Vec<Vec<u8>>,
    i: usize,
    j: usize,
) -> HashSet<(usize, usize)> {
    let n_rows = field.len() as i32;
    let n_cols = field[0].len() as i32;

    let mut removable_neighbors = HashSet::new();
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

            let n_neighbors = count_neighbors(field, ni as usize, nj as usize);
            if field[ni as usize][nj as usize] == ROLL as u8 && n_neighbors < NEIGHBOR_LIMIT {
                removable_neighbors.insert((ni as usize, nj as usize));
            }
        }
    }

    removable_neighbors
}

fn main() {
    let mut field: Vec<Vec<u8>> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap().bytes().collect())
        .collect();

    let mut removables = HashSet::new();
    for i in 0..field.len() {
        for j in 0..field[0].len() {
            if field[i][j] == ROLL as u8 && count_neighbors(&field, i, j) < NEIGHBOR_LIMIT {
                removables.insert((i, j));
            }
        }
    }

    let mut total_removable = 0;
    while !removables.is_empty() {
        remove(&mut field, &removables);
        total_removable += removables.len();

        let mut new_removables = HashSet::new();
        for (removable_i, removable_j) in removables.iter() {
            let removable_neighbors =
                collect_removable_neighbors(&field, *removable_i, *removable_j);
            new_removables.extend(removable_neighbors);
        }

        removables = new_removables;
    }

    println!("{total_removable}");
}
