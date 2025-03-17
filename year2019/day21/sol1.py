import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
from intcode import Intcode
import copy

computer = Intcode(sys.argv[1])

while True:
    output = computer.run()
    if output is None:
        break
    else:
        print(chr(output), end="")

def simulate(commands):
    computer = copy.deepcopy(simulate.stored)
    commands_ascii = map(ord, "\n".join(commands) + "\n")
    computer.put(commands_ascii)
    while True:
        output = computer.run()
        if output is None:
            break
        else:
            try:
                print(chr(output), end="")
            except ValueError:
                print(output)
    
simulate.stored = computer

'''
    part1 solution:
        - if not a or not c and d
        - ["NOT A T", "NOT C J", "OR T J", "AND D J", "WALK"]
    part2 solution:
        - if not a or (not b or not c) and d
        - ["NOT C J", "NOT B T", "OR T J", "AND D J", "AND B T", "OR H T", "OR E T", "AND T J", "NOT A T", "OR T J", "RUN"]
        - AND B T -> in order to put 0 to reg T (previous value in T was ~T)
'''

# command = ""
# while command != "WALK":
#     command = input()
#     command_list.append(command)
# command_list_ascii = map(ord, "\n".join(command_list) + "\n")
# computer.put(command_list_ascii)