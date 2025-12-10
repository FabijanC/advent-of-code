use std::{
    collections::HashMap,
    io::{stdin, BufRead},
    str::FromStr,
    string::ParseError,
};

#[derive(Debug)]
struct Point {
    x: u64,
    y: u64,
    z: u64,
}

fn get_squared_distance_between(p1: &Point, p2: &Point) -> u64 {
    let dx = p1.x.abs_diff(p2.x);
    let dy = p1.y.abs_diff(p2.y);
    let dz = p1.z.abs_diff(p2.z);

    dx * dx + dy * dy + dz * dz
}

impl FromStr for Point {
    type Err = ParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let coordinates: Vec<u64> = s
            .split(',')
            .map(|raw_coordinate| raw_coordinate.parse().unwrap())
            .collect();

        assert_eq!(coordinates.len(), 3);

        Ok(Point {
            x: coordinates[0],
            y: coordinates[1],
            z: coordinates[2],
        })
    }
}

/// Union-find
fn get_root(mut i: usize, junction_membership: &HashMap<usize, usize>) -> usize {
    loop {
        let parent = *junction_membership.get(&i).unwrap();
        if parent == i {
            break;
        }

        i = parent;
    }

    i
}

fn main() {
    let points: Vec<Point> = stdin()
        .lock()
        .lines()
        .map(|l| Point::from_str(&l.unwrap()).unwrap())
        .collect();

    // Stores the distance and the pair of indices between which it was calculated.
    let mut distances: Vec<(u64, (usize, usize))> = vec![];

    for (i, pi) in points.iter().enumerate() {
        for (j, pj) in points.iter().enumerate().skip(i + 1) {
            let d = get_squared_distance_between(pi, pj);

            distances.push((d, (i, j)));
        }
    }

    // Floats in Rust do not implement Ord, only PartialOrd
    // distances.sort_by(|(d1, _), (d2, _)| d1.partial_cmp(d2).unwrap());
    distances.sort_by_key(|(d, _)| *d);

    // Each junction is identified by one (and only one) of its members
    let mut junction_membership: HashMap<usize, usize> = HashMap::new();
    for i in 0..points.len() {
        junction_membership.insert(i, i);
    }

    let mut sol = 0;
    for (_, (i, j)) in distances.into_iter() {
        let root_i = get_root(i, &junction_membership);
        let root_j = get_root(j, &junction_membership);
        if root_i != root_j {
            sol = points[i].x * points[j].x;
        }

        junction_membership.insert(root_i, root_j);
    }

    println!("{sol}");
}
