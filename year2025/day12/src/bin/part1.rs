use std::{
    collections::HashSet,
    io::{stdin, BufRead},
};

const DIM: usize = 3;

#[derive(PartialEq, Eq, Hash, Clone, Debug)]
struct Shape([[bool; DIM]; DIM]);

#[derive(Debug)]
#[allow(dead_code)]
struct ShapeParseError(String);

impl Shape {
    fn parse<S>(raw: &[S]) -> Result<Self, ShapeParseError>
    where
        S: AsRef<str>,
    {
        if raw.len() != DIM {
            return Err(ShapeParseError("Invalid dim".into()));
        }

        let mut shape = Self::empty();

        for (i, raw_line) in raw.iter().enumerate() {
            let raw_line = raw_line.as_ref();
            if raw_line.len() != DIM {
                return Err(ShapeParseError("Invalid line dim".into()));
            }

            for (j, c) in raw_line.char_indices() {
                shape.0[i][j] = match c {
                    '#' => true,
                    '.' => false,
                    other => return Err(ShapeParseError(format!("Invalid char: {other}"))),
                }
            }
        }

        Ok(shape)
    }

    fn variants(&self) -> HashSet<Self> {
        let mut legal_variants = HashSet::new();

        let mut rotation = self.clone();
        for _ in 0..4 {
            rotation = rotation.rotate_cw();
            legal_variants.insert(rotation.clone());
        }

        rotation = self.flip_vertical_axis();
        for _ in 0..4 {
            rotation = rotation.rotate_cw();
            legal_variants.insert(rotation.clone());
        }

        legal_variants
    }

    fn empty() -> Self {
        Self([[false; DIM]; DIM])
    }

    fn rotate_cw(&self) -> Self {
        let mut rotated = Self::empty();
        for i in 0..DIM {
            for j in 0..DIM {
                rotated.0[j][DIM - i - 1] = self.0[i][j];
            }
        }

        rotated
    }

    fn flip_vertical_axis(&self) -> Self {
        let mut flipped = Self::empty();
        for i in 0..DIM {
            for j in 0..DIM {
                flipped.0[i][j] = self.0[i][DIM - j - 1];
            }
        }

        flipped
    }

    fn area(&self) -> usize {
        let mut n = 0;
        for i in 0..DIM {
            for j in 0..DIM {
                if self.0[i][j] {
                    n += 1;
                }
            }
        }

        n
    }
}

#[cfg(test)]
mod test_shape {
    use std::collections::HashSet;

    use crate::Shape;

    #[test]
    fn test_empty_creation() {
        assert_eq!(
            Shape::empty(),
            Shape([
                [false, false, false],
                [false, false, false],
                [false, false, false],
            ])
        );
    }

    #[test]
    fn test_parsing() {
        assert_eq!(
            Shape::parse(&["#..", "..#", "#.#"]).unwrap(),
            Shape([
                [true, false, false],
                [false, false, true],
                [true, false, true],
            ])
        );
    }

    #[test]
    fn test_flipping_along_vertical_axis_of_asymmetrical_shape() {
        assert_eq!(
            Shape::parse(&["#..", ".#.", "..#"])
                .unwrap()
                .flip_vertical_axis(),
            Shape::parse(&["..#", ".#.", "#.."]).unwrap(),
        );
    }

    #[test]
    fn test_flipping_along_vertical_axis_of_symmetrical_shape() {
        let shape = Shape::parse(&["#.#", ".#.", ".#."]).unwrap();
        assert_eq!(shape.flip_vertical_axis(), shape);
    }

    #[test]
    fn test_cw_rotation() {
        assert_eq!(
            Shape::parse(&["#.#", "...", "..."]).unwrap().rotate_cw(),
            Shape::parse(&["..#", "...", "..#"]).unwrap(),
        );
    }

    #[test]
    fn test_triple_rotation() {
        assert_eq!(
            Shape::parse(&["#.#", "...", "..."])
                .unwrap()
                .rotate_cw()
                .rotate_cw()
                .rotate_cw(),
            Shape::parse(&["#..", "...", "#.."]).unwrap(),
        );
    }

    #[test]
    fn test_quadruple_rotation() {
        let shape = Shape::parse(&["#.#", "...", "..."]).unwrap();
        assert_eq!(shape.rotate_cw().rotate_cw().rotate_cw().rotate_cw(), shape,);
    }

    #[test]
    fn test_variants() {
        let original_raw = ["##.", "...", "..."];
        let shape = Shape::parse(&original_raw).unwrap();
        let expected_variants = [
            original_raw,
            ["..#", "..#", "..."],
            ["...", "...", ".##"],
            ["...", "#..", "#.."],
            ["...", "...", "##."], // flipped
            ["#..", "#..", "..."],
            [".##", "...", "..."],
            ["...", "..#", "..#"],
        ]
        .into_iter()
        .map(|raw| Shape::parse(&raw).unwrap());

        let generated_variants = shape.variants();
        assert_eq!(generated_variants.len(), expected_variants.len()); // Make sure no duplicates in expected
        assert_eq!(generated_variants, HashSet::from_iter(expected_variants));
    }

    #[test]
    fn test_empty_area() {
        let shape = Shape::empty();
        assert_eq!(shape.area(), 0);
    }

    #[test]
    fn test_area() {
        let shape = Shape::parse(&["##.", "...", "#.#"]).unwrap();
        assert_eq!(shape.area(), 4);
    }
}

type ShapeVariantMap = Vec<Vec<Shape>>;

#[derive(PartialEq, Eq, Hash, Clone, Debug)]
struct Board(Vec<Vec<bool>>);

impl Board {
    fn empty(width: usize, length: usize) -> Self {
        Self(vec![vec![false; width]; length])
    }

    /// If `shape` fits into `self` starting at (board_i, board_j), returns `Some`: a new `Board`
    /// with the new locations set. Otherwise returns `None`.
    fn try_fit(&self, shape: &Shape, board_i: usize, board_j: usize) -> Option<Self> {
        let length = self.0.len();
        let width = self.0[0].len();

        let mut successful_fit = self.clone();

        for shape_i in 0..DIM {
            for shape_j in 0..DIM {
                if !shape.0[shape_i][shape_j] {
                    continue;
                }

                let candidate_i = board_i + shape_i;
                let candidate_j = board_j + shape_j;

                if candidate_i >= length || candidate_j >= width {
                    return None;
                }

                if self.0[candidate_i][candidate_j] {
                    return None;
                }

                successful_fit.0[candidate_i][candidate_j] = true;
            }
        }

        Some(successful_fit)
    }

    /// Produces a Vec of legal fittings of the provided `shape` into `self`.
    fn get_legal_fittings(&self, shape_variants: &[Shape]) -> Vec<Self> {
        let mut legal_fittings = vec![];
        for i in 0..self.0.len() {
            for j in 0..self.0[0].len() {
                for shape_variant in shape_variants {
                    if let Some(fit) = self.try_fit(shape_variant, i, j) {
                        legal_fittings.push(fit);
                    }
                }
            }
        }

        legal_fittings
    }

    fn free_area(&self) -> usize {
        let mut n = 0;
        for i in 0..self.0.len() {
            for j in 0..self.0[0].len() {
                if !self.0[i][j] {
                    n += 1
                }
            }
        }

        n
    }
}

#[cfg(test)]
mod test_board {
    use crate::{Board, Shape};

    #[test]
    fn test_initialization() {
        assert_eq!(
            Board::empty(3, 2),
            Board(vec![vec![false, false, false], vec![false, false, false]])
        );
    }

    #[test]
    fn test_try_fit_successful_on_empty_board() {
        let width = 5;
        let length = 6;
        let board = Board::empty(width, length);
        let shape = Shape::parse(&["#..", "...", "..."]).unwrap();
        for i in 0..length {
            for j in 0..width {
                let fit = board.try_fit(&shape, i, j);
                let mut expected = Board::empty(width, length);
                expected.0[i][j] = true;
                assert_eq!(fit, Some(expected));
            }
        }
    }

    #[test]
    fn test_try_fit_successful_on_almost_full_board() {
        let width = 5;
        let length = 6;
        let mut board = Board::empty(width, length);

        // All fields set except (0, 0)
        for i in 0..length {
            for j in 0..width {
                board.0[i][j] = true;
            }
        }
        let full_board = board.clone();
        board.0[0][0] = false;

        let shape = Shape::parse(&["#..", "...", "..."]).unwrap();
        for i in 0..length {
            for j in 0..width {
                let fit = board.try_fit(&shape, i, j);
                if i == 0 && j == 0 {
                    assert_eq!(fit, Some(full_board.clone()));
                } else {
                    assert_eq!(fit, None);
                }
            }
        }
    }

    #[test]
    fn test_try_fit_unsuccessful_due_to_shape_falling_out() {
        let width = 5;
        let length = 6;
        let board = Board::empty(width, length);
        let shape = Shape::parse(&["##.", "...", "..."]).unwrap();
        for i in 0..length {
            for j in 0..width {
                let fit = board.try_fit(&shape, i, j);
                if j == width - 1 {
                    assert_eq!(fit, None);
                } else {
                    let mut expected = Board::empty(width, length);
                    expected.0[i][j] = true;
                    expected.0[i][j + 1] = true;
                    assert_eq!(fit, Some(expected));
                }
            }
        }
    }

    #[test]
    fn test_try_fit_unsuccessful_due_to_overlap() {
        let width = 5;
        let length = 6;
        let mut board = Board::empty(width, length);
        board.0[0][0] = true;

        let shape = Shape::parse(&["#..", "...", "..."]).unwrap();
        for i in 0..length {
            for j in 0..width {
                let fit = board.try_fit(&shape, i, j);
                if i == 0 && j == 0 {
                    assert_eq!(fit, None);
                } else {
                    let mut expected = Board::empty(width, length);
                    expected.0[0][0] = true;
                    expected.0[i][j] = true;
                    assert_eq!(fit, Some(expected));
                }
            }
        }
    }

    #[test]
    fn test_calculating_free_area() {
        let width = 5;
        let length = 6;
        let mut board = Board::empty(width, length);

        assert_eq!(board.free_area(), width * length);

        board.0[1][1] = true;
        assert_eq!(board.free_area(), width * length - 1);
    }

    #[test]
    fn test_free_area_after_fitting_shape() {
        let width = 5;
        let length = 6;
        let mut board = Board::empty(width, length);
        board.0[0][0] = true;

        let shape = Shape::parse(&["#..", ".#.", ".#."]).unwrap();
        assert_eq!(shape.area(), 3);

        assert_eq!(board.free_area(), width * length - 1);

        let fit = board.try_fit(&shape, 0, 1).unwrap();
        assert_eq!(fit.free_area(), width * length - 1 - shape.area());
    }
}

#[derive(Debug)]
#[allow(dead_code)]
struct RequirementsParseError(String);

fn parse_requirements<S>(line: &S) -> Result<(usize, usize, Vec<usize>), RequirementsParseError>
where
    S: AsRef<str>,
{
    let line = line.as_ref();
    let parts: Vec<&str> = line.split(": ").collect();
    if parts.len() != 2 {
        return Err(RequirementsParseError(format!("Invalid line: {line}")));
    }

    let dims_raw: Vec<&str> = parts[0].split('x').collect();
    if dims_raw.len() != 2 {
        return Err(RequirementsParseError(format!(
            "Invalid board dimensions: {dims_raw:?}"
        )));
    }

    let width = dims_raw[0]
        .parse()
        .or_else(|e| Err(RequirementsParseError(format!("{e}"))))?;
    let length = dims_raw[1]
        .parse()
        .or_else(|e| Err(RequirementsParseError(format!("{e}"))))?;

    let mut shape_counter = vec![];
    for raw_shape_count in parts[1].split_whitespace() {
        let shape_count: usize = raw_shape_count
            .parse()
            .or_else(|e| Err(RequirementsParseError(format!("{e}"))))?;

        shape_counter.push(shape_count);
    }

    Ok((width, length, shape_counter))
}

fn generate_variant_map(shapes: &[Shape]) -> ShapeVariantMap {
    let mut all_variants_map = vec![];

    for shape in shapes {
        let variants = shape.variants().into_iter().collect();
        all_variants_map.push(variants);
    }

    all_variants_map
}

fn all_fits(
    board: Board,
    remaining_free_area: usize,
    requirements: Vec<usize>,
    remaining_required_area: usize,
    shape_variants_map: &ShapeVariantMap,
    shape_areas: &Vec<usize>,
    history: &mut HashSet<(Board, Vec<usize>)>,
) -> bool {
    if remaining_required_area == 0 {
        return true;
    }

    let historic_config = (board.clone(), requirements.clone());
    if history.contains(&historic_config) {
        return false;
    }
    history.insert(historic_config);

    for i in 0..requirements.len() {
        if requirements[i] == 0 {
            continue;
        }

        let mut next_requirements = requirements.clone();
        next_requirements[i] -= 1;

        if remaining_free_area < shape_areas[i] {
            continue;
        }
        let next_remaining_free_area = remaining_free_area - shape_areas[i];

        if remaining_required_area < shape_areas[i] {
            continue;
        }
        let next_remaining_required_area = remaining_required_area - shape_areas[i];

        if next_remaining_free_area < next_remaining_required_area {
            continue;
        }

        let shape_variants = &shape_variants_map[i];
        for next_board in board.get_legal_fittings(shape_variants) {
            if all_fits(
                next_board,
                next_remaining_free_area,
                next_requirements.clone(),
                next_remaining_required_area,
                shape_variants_map,
                shape_areas,
                history,
            ) {
                return true;
            }
        }
    }

    return false;
}

fn main() {
    let lines: Vec<String> = stdin().lock().lines().map(|l| l.unwrap()).collect();

    let mut shapes = vec![];
    let mut shape_areas = vec![];

    let mut line_i = 0;
    loop {
        // Every shape group begins with <ID> followed by colon
        if !lines[line_i].ends_with(':') {
            break;
        }

        line_i += 1; // Assume shapes numbered sequentially, skip shape ID parsing

        let shape_lines = &lines[line_i..line_i + DIM];
        let shape = Shape::parse(&shape_lines).unwrap();
        line_i += DIM + 1; // +1 because skipping empty line

        shape_areas.push(shape.area());
        shapes.push(shape);
    }

    let shape_variant_map = generate_variant_map(&shapes);
    let mut fittable_boards = 0;

    for line in &lines[line_i..] {
        let (width, length, requirements) = parse_requirements(line).unwrap();

        let mut required_free_area = 0;
        for (shape_index, shape_count) in requirements.iter().enumerate() {
            required_free_area += shape_areas[shape_index] * shape_count;
        }

        let board = Board::empty(width, length);
        let free_area = board.free_area();
        let mut history = Default::default(); // History can only be reused for equivalent boards - negligible
        if all_fits(
            board,
            free_area,
            requirements,
            required_free_area,
            &shape_variant_map,
            &shape_areas,
            &mut history,
        ) {
            println!("yes ok");
            fittable_boards += 1;
        } else {
            println!("not ok");
        }
    }

    println!("{fittable_boards}");
}
