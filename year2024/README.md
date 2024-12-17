# TODO

- Improve solution to day 12 by calculating the inner perimeter in a smarter way. Currently using outsideArea = (totalFieldArea - polygonArea) and identifying all areas not in polygonArea or totalFieldArea to find enclosed areas, then applying outer perimeter calculation on them.
- Improve solution to day 17 by relying on a more deterministic approach. Current approach relies on the following observations:
  - Initial register A value is of the same order of magnitude as the number constructed from reverting and joining the input program.
  - Similar initial register A values lead to similar outputs.
