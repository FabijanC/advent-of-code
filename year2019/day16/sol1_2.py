import sys
import time
t1 = time.time()

with open(sys.argv[1]) as f:
    signal = list(map(int, list(f.read().strip())))

'''
    12345678
    (1+5) - (3+7) = -4 -> 4
    (2+3) - (6+7) = -8 -> 8
'''
SIGNAL_LEN = len(signal)
for step in range(100):
    prefix_sum = [0]
    for i in range(SIGNAL_LEN):
        prefix_sum.append(prefix_sum[i] + signal[i])
    new_signal = []
    for i in range(SIGNAL_LEN):
        sign = 1
        new_signal_val = 0
        for j in range(i, SIGNAL_LEN, 2*(i+1)):
            tmp = (prefix_sum[min(j+i+1, SIGNAL_LEN)] - prefix_sum[j])
            new_signal_val += sign*tmp
            sign *= -1
        new_signal.append(abs(new_signal_val) % 10)
    signal = new_signal
print("".join(map(str,signal[:8])))
print(time.time() - t1)
