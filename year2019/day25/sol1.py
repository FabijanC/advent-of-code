import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
from intcode import Intcode

computer = Intcode(sys.argv[1])

while True:
    output = computer.run()
    if output is None:
        break
    else:
        print(chr(output), end="")

while True:
    command = input() + "\n"
    computer.put(map(ord,command))
    while True:
        output = computer.run()
        if output is None:
            break
        else:
            print(chr(output), end="")
