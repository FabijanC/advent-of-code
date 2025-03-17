import sys
import time
t1 = time.time()

with open(sys.argv[1]) as f:
    signal = list(map(int, list(f.read().strip())))

SIGNAL_LEN = len(signal)
for step in range(100):
    new_signal = []
    for i in range(SIGNAL_LEN):
        new_signal_val = 0
        j = i
        sign = 1
        while j < SIGNAL_LEN:
            lim = j + i + 1
            while j < lim and j < SIGNAL_LEN:
                new_signal_val += sign*signal[j]
                j += 1
            j += i+1
            sign *= -1
            # j += i+1
        # for j in range(i, SIGNAL_LEN, i+1):
        #     new_signal_val += signal[j] * pattern[((j+1) // (i+1)) % 4]
        new_signal.append(abs(new_signal_val) % 10)
    
    signal = new_signal
print("".join(map(str,signal[:8])))
print(time.time() - t1)
