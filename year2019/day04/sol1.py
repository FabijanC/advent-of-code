mini, maxi = map(int, input().split("-"))

cnt = 0
for num in range(mini, maxi+1):
    last_digit = 10
    duplicate_found = False
    does_not_decrease = True
    copy = num
    while num > 0:
        curr_digit = num % 10
        if curr_digit == last_digit:
            duplicate_found = True
        if curr_digit > last_digit:
            does_not_decrease = False
        
        last_digit = curr_digit
        num //= 10
    
    if duplicate_found and does_not_decrease:
        print(copy)
        cnt += 1
print(cnt)