import sys

def solve():
    n = sys.stdin.readline().strip().split('-')
    
    result = 0
    
    first_part = n[0].split('+')
    for num in first_part:
        result += int(num)
        
    for part in n[1:]:
        rsum = sum(map(int, part.split('+')))
        result -= rsum
        
    print(result)

solve()