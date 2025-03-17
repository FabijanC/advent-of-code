from collections import deque

ADD = "01"
MUL = "02"
GET = "03"
PUT = "04"
JPT = "05"
JPF = "06"
LST = "07"
EQS = "08"
REL = "09"
HALT = "99"

class Intcode:
    HALTED = "HALTED"
    OK = "OK"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"

    def __init__(self, file_name):
        self.field = {}
        with open(file_name) as f:
            for i, val in enumerate(map(int, f.read().strip().split(","))):
                self.field[i] = val
        self.rel_base = 0
        self.i = 0
        self.input_stream = deque()
        self.state = Intcode.OK

    def read(self, i, mode):
        if mode == "0":
            return self.field.get(self.field.get(i, 0), 0)
        elif mode == "1":
            return self.field.get(i, 0)
        elif mode == "2":
            return self.field.get(self.rel_base + self.field[i], 0)

    def write(self, i, mode, val):
        if mode == "0":
            self.field[self.field[i]] = val
        elif mode == "1":
            print("ERROR")
            raise RuntimeError("Unknown write mode")
        elif mode == "2":
            self.field[self.rel_base + self.field[i]] = val

    def put(self, content):
        for c in content:
            self.input_stream.appendleft(c)

    def run(self):
        while True:
            curr = str(self.field[self.i])
            curr = "0"*(5 - len(curr)) + curr
            modes, command = curr[:3], curr[3:]
            
            if command == HALT:
                self.state = Intcode.HALTED
                return None
            elif command == ADD:
                val = self.read(self.i+1, modes[-1]) + self.read(self.i+2, modes[-2])
                self.write(self.i+3, modes[-3], val)
                self.i += 4
            elif command == MUL:
                val = self.read(self.i+1, modes[-1]) * self.read(self.i+2, modes[-2])
                self.write(self.i+3, modes[-3], val)
                self.i += 4
            elif command == GET:
                if not self.input_stream:
                    self.state = Intcode.WAITING_FOR_INPUT
                    return None
                self.state = Intcode.OK
                input_val = self.input_stream.pop()
                self.write(self.i+1, modes[-1], input_val)
                self.i += 2
            elif command == PUT:
                output = self.read(self.i+1, modes[-1])
                self.i += 2
                return output
            elif command == JPT:
                if self.read(self.i+1, modes[-1]):
                    self.i = self.read(self.i+2, modes[-2])
                else:
                    self.i += 3
            elif command == JPF:
                if not self.read(self.i+1, modes[-1]):
                    self.i = self.read(self.i+2, modes[-2])
                else:
                    self.i += 3
            elif command == LST:
                first = self.read(self.i+1, modes[-1])
                second = self.read(self.i+2, modes[-2])
                val = int(first < second)
                self.write(self.i+3, modes[-3], val)
                self.i += 4
            elif command == EQS:
                first = self.read(self.i+1, modes[-1])
                second = self.read(self.i+2, modes[-2])
                val = int(first == second)
                self.write(self.i+3, modes[-3], val)
                self.i += 4
            elif command == REL:
                delta = self.read(self.i+1, modes[-1])
                self.rel_base += delta
                self.i += 2
            else:
                raise RuntimeError("Unknown opcode, ", command)