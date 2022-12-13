import sys
from typing import List


def compare(left: List, right: List):
    for left_el, right_el in zip(left, right):
        left_el_is_int = isinstance(left_el, int)
        right_el_is_int = isinstance(right_el, int)
        if left_el_is_int and right_el_is_int:
            if left_el < right_el:
                return True
            if left_el > right_el:
                return False
        elif not left_el_is_int and not right_el_is_int:
            list_comparison = compare(left_el, right_el)
            if list_comparison is not None:
                return list_comparison
        else:
            list_comparison = (
                compare([left_el], right_el)
                if left_el_is_int
                else compare(left_el, [right_el])
            )
            if list_comparison is not None:
                return list_comparison
    
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False

    # lists are equal
    return None


def main():
    lines = [line.strip() for line in sys.stdin]

    sol = 0
    for line_i in range(0, len(lines), 3):
        left = eval(lines[line_i])
        right = eval(lines[line_i + 1])
        
        if compare(left, right) == True:
            i = line_i // 3 + 1
            sol += i

    print(sol)

if __name__ == "__main__":
    main()
