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
    outputs = []
    while True:
        output = computer.run()
        if output is None:
            break
        else:
            try:
                outputs.append(chr(output))
            except ValueError:
                print(output)
                print(commands)
                exit()
    return "".join(outputs)
    
simulate.stored = computer

op_list = ["NOT", "OR", "AND"]
reg1_list = "ABCDTJ"
reg2_list = "TJ"
cnt = 0
def rek(commands):
    global cnt
    if len(commands) > 4:
        return
    
    cnt += 1
    if cnt % 10000 == 0:
        print(commands)
        print("DEBUG", cnt)
    
    executable_commands = commands + ["WALK"]
    output = simulate(executable_commands)
    
    for op in op_list:
        for reg1 in reg1_list:
            for reg2 in reg2_list:
                rek(commands + [f"{op} {reg1} {reg2}"])

rek([])
