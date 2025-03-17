import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
from intcode import Intcode
from collections import deque

N_COMP = 50

computers = []
buffers = []
receiver = []
sent = []
for i in range(N_COMP):
    computer = Intcode(sys.argv[1])
    computer.put([i])
    computer.run()
    computers.append(computer)
    buffers.append(deque())
    receiver.append(None)
    sent.append(0)

round = 1
while True:
    print("round", round)
    round += 1
    for i in range(N_COMP):
        computer = computers[i]
        assert computer.state != Intcode.HALTED
        if not buffers[i]:
            computer.put([-1])
        else:
            computer.put([buffers[i].popleft(),buffers[i].popleft()])
        
        receiver = computer.run()
        if receiver is None:
            continue
        x, y = computer.run(), computer.run()
        if receiver == 255:
            print(y)
            exit()
        buffer = buffers[receiver]
        buffer.append(x)
        buffer.append(y)