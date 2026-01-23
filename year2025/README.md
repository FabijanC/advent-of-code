# TODO

- Day 12 took around 26 minutes to execute on my machine.
  - Searching could rely on A\* instead of DFS. This would present a speed-up only if the shapes do fit onto the board.
  - Could implement `Board` as sequence of 64-bit integers and use bitwise operations (`&` to check if area occupied, `|` to add shape).
