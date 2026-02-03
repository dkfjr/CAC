import sys

def solve():
    n = int(sys.stdin.readline())
    
    if int(n**0.5)**2 == n:
        print(1)
        return
    for i in range(1, int(n**0.5) + 1):
        if int((n - i**2)**0.5)**2 == (n - i**2):
            print(2)
            return
    for i in range(1, int(n**0.5) + 1):
        for j in range(1, int((n - i**2)**0.5) + 1):
            if int((n - i**2 - j**2)**0.5)**2 == (n - i**2 - j**2):
                print(3)
                return
    print(4)

solve()