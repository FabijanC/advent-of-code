use std::io::{stdin, BufRead};

fn main() {
    let lines: Vec<String> = stdin().lock().lines().map(|l| l.unwrap()).collect();
    let mut index: i32 = 50;
    let size = 100;
    let mut password = 0;

    for line in lines {
        let mut clicks: i32 = line[1..].parse().unwrap();
        password += clicks / size; // full circles
        clicks %= size;

        match &line[..1] {
            "L" => {
                index -= clicks;
                if index <= 0 && -index != clicks {
                    // The case when before subtraction index was not already 0
                    password += 1;
                }
            }
            "R" => {
                index += clicks;
                if index >= size {
                    password += 1;
                }
            }
            _ => panic!("Invalid command: {line}"),
        }

        index = (index + size) % size;
    }

    println!("{password}");
}
