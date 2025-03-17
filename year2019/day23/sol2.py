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

def all_empty(lists):
    for L in lists:
        if L:
            return False
    return True

nat0 = None
nat = deque()

while True:
    idle_cnt = 0
    for i in range(N_COMP):
        computer = computers[i]
        assert computer.state != Intcode.HALTED
        if not buffers[i]:
            computer.put([-1])
            idle_cnt += 1
        else:
            computer.put([buffers[i].popleft(), buffers[i].popleft()])
        
        receiver = computer.run()
        if receiver is None:
            continue
        x, y = computer.run(), computer.run()
        if receiver == 255:
            nat = [x,y]
        else:
            buffer = buffers[receiver]
            buffer.append(x)
            buffer.append(y)
    
    # print(" ".join(map(lambda b: str(len(b)), buffers)))
    if all_empty(buffers) and idle_cnt == N_COMP:
        x, y = nat
        buffers[0].append(x)
        buffers[0].append(y)
        if nat0 == y:
            print(y)
            exit()
        nat0 = y