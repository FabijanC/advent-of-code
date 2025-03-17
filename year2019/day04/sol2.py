mini, maxi = map(int, input().split("-"))

cnt = 0
for num in range(mini, maxi+1):
    last_digit = 10
    duplicate_found = False
    does_not_decrease = True
    seq_len = 0
    copy = num
    while num > 0:
        curr_digit = num % 10
        if curr_digit == last_digit:
            seq_len += 1
        elif curr_digit > last_digit:
            if seq_len == 2:
                duplicate_found = True
            seq_len = 1
            does_not_decrease = False
        else:
            if seq_len == 2:
                duplicate_found = True
            seq_len = 1
        
        last_digit = curr_digit
        num //= 10
    
    if seq_len == 2:
        duplicate_found = True
    
    if duplicate_found and does_not_decrease:
        print(copy)
        cnt += 1
print(cnt)