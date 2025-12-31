use std::io::{stdin, BufRead};

type Point = (i64, i64);
type Edge = (Point, Point);

#[derive(PartialEq, Eq)]
enum Orientation {
    Horizontal,
    Vertical,
}

impl Orientation {
    fn of_edge(e: &Edge) -> Self {
        let (from, to) = e;
        if from.0 == to.0 {
            Self::Vertical
        } else if from.1 == to.1 {
            Self::Horizontal
        } else {
            panic!("Edge neither vertical nor horizontal: {e:?}")
        }
    }
}

fn intersect(e1: &Edge, e2: &Edge) -> Option<Point> {
    let orientation1 = Orientation::of_edge(e1);
    let orientation2 = Orientation::of_edge(e2);
    if orientation1 == orientation2 {
        // Checked: input contains no two edges with the same orientation that only share one point.
        // I.e. no edge extends another.
        return None;
    }

    let (horizontal, vertical) = if orientation1 == Orientation::Horizontal {
        (e1, e2)
    } else {
        (e2, e1)
    };

    let vx = vertical.0 .0;
    let mut hx = [horizontal.0 .0, horizontal.1 .0];
    hx.sort();

    let hy = horizontal.0 .1;
    let mut vy = [vertical.0 .1, vertical.1 .1];
    vy.sort();

    if hx[0] <= vx && vx <= hx[1] && vy[0] <= hy && hy <= vy[1] {
        Some((vx, hy))
    } else {
        None
    }
}

#[test]
fn test_intersect() {
    for (e1, e2) in [
        (((11, 7), (9, 7)), ((9, 7), (9, 5))),
        (((9, 7), (11, 7)), ((9, 5), (9, 7))),
    ] {
        assert_eq!(intersect(&e1, &e2), Some((9, 7)));
    }
}

#[derive(PartialEq, Eq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    fn new(from: &Point, to: &Point) -> Self {
        if from.0 < to.0 {
            Self::Left
        } else if from.0 > to.0 {
            Self::Right
        } else if from.1 < to.1 {
            Self::Down
        } else if from.1 > to.1 {
            Self::Up
        } else {
            panic!("Edge must not be a point: {from:?}")
        }
    }
}

/// Returns `true` iff `p` belongs to `e`.
fn belongs(p: &Point, e: &Edge) -> bool {
    let (from, to) = e;
    if from == p || to == p {
        return true;
    }

    if from.0 == p.0 {
        let mut ey = [from.1, to.1];
        ey.sort();
        return ey[0] <= p.1 && p.1 <= ey[1];
    }

    if from.1 == p.1 {
        let mut ex = [from.0, to.0];
        ex.sort();
        return ex[0] <= p.0 && p.0 <= ex[1];
    }

    false
}

#[test]
fn test_belongs() {
    for (p, e) in [
        ((1, 2), ((1, 2), (1, 3))),
        ((1, 3), ((1, 2), (1, 3))),
        ((1, 1), ((0, 1), (5, 1))),
        ((1, 1), ((1, 0), (1, 5))),
    ] {
        assert!(belongs(&p, &e), "p={p:?}, e={e:?}");
    }

    for (p, e) in [
        ((1, 0), ((1, 2), (1, 3))),
        ((1, 4), ((1, 2), (1, 3))),
        ((6, 1), ((0, 1), (5, 1))),
        ((1, 6), ((1, 0), (1, 5))),
        ((2, 0), ((1, 0), (1, 5))),
    ] {
        assert!(!belongs(&p, &e), "p={p:?}, e={e:?}");
    }
}

/// Calculates the edge from `start` to `end` and iterates through `polygon_edges` to check for
/// intersections. Disallow intersections not at any vertex. Those at vertex are allowed if turning
/// towards the `other` corner (the one diagonally from `start`).
fn reachable(start: &Point, end: &Point, other: &Point, polygon_edges: &Vec<Edge>) -> bool {
    assert_ne!(start, end);
    assert!(start.0 == end.0 || start.1 == end.1);

    let rectangle_edge: Edge = (*start, *end);
    let perpendicular_edge: Edge = (*end, *other);
    let final_perpendicular_direction = Direction::new(end, other);

    for polygon_edge in polygon_edges {
        let (ep1, ep2) = polygon_edge;

        let intersection = intersect(&rectangle_edge, polygon_edge);
        match intersection {
            None => continue,
            Some(ip /* intersection point */) => {
                if ep1 == start || ep2 == start {
                    // First edge ignored here and processed separately
                    continue;
                }

                if belongs(ep1, &perpendicular_edge) || belongs(ep2, &perpendicular_edge) {
                    // Polygon edge at the end of rectangle edge
                    continue;
                }

                if &ip != ep1 && &ip != ep2 {
                    // Intersection in the middle of the edge
                    return false;
                }

                if &ip == ep1 && Direction::new(&ip, ep2) == final_perpendicular_direction {
                    return false;
                }

                if &ip == ep2 && Direction::new(&ip, ep1) == final_perpendicular_direction {
                    return false;
                }
            }
        }
    }

    true
}

fn get_spanned_area(p1: &Point, p2: &Point) -> u64 {
    (p1.0.abs_diff(p2.0) + 1) * (p1.1.abs_diff(p2.1) + 1)
}

fn main() {
    let polygon_points: Vec<Point> = stdin()
        .lock()
        .lines()
        .map(|l| l.unwrap())
        .map(|l| {
            let pair: Vec<_> = l.split(',').map(|n| n.parse().unwrap()).collect();
            assert_eq!(pair.len(), 2);
            (pair[0], pair[1])
        })
        .collect();

    let n_pairs = polygon_points.len();

    let mut edges = vec![];
    for i in 0..n_pairs {
        let p1 = &polygon_points[i];
        let p2 = &polygon_points[(i + 1) % n_pairs];
        // Checked: no two consecutive edges have the same direction.
        edges.push((*p1, *p2));
    }

    let mut max_area = 0_u64;
    for i in 0..n_pairs {
        let p1 = &polygon_points[i];
        for j in (i + 1)..n_pairs {
            let p2 = &polygon_points[j];

            if p1.0 == p2.0 || p1.1 == p2.1 {
                // Skipping thin rectangles
                continue;
            }

            // Remaining (other) vertices
            let o1 = (p1.0, p2.1);
            let o2 = (p2.0, p1.1);

            // Now that we have two corner (red) tiles, from each of them try to reach the
            // remaining points, not the other corner tile
            let mut rectangle_valid = true;
            'reachability_loop: for (start, other) in [(p1, p2), (p2, p1)] {
                for end in [o1, o2] {
                    if !reachable(start, &end, other, &edges) {
                        rectangle_valid = false;
                        break 'reachability_loop;
                    }
                }
            }

            if rectangle_valid {
                let area = get_spanned_area(p1, p2);
                max_area = std::cmp::max(area, max_area);
            }
        }
    }

    println!("Max area: {max_area}");
}
