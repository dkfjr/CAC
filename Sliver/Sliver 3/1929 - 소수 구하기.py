import sys
input = sys.stdin.readline

N, M = map(int, input().split())
prime = [True] * (M + 1)
prime[0] = prime[1] = False

for i in range(2, int(M ** 0.5) + 1):
    if prime[i]:
        for j in range(i * i, M + 1, i):
            prime[j] = False

for i in range(N, M + 1):
    if prime[i]:
        print(i)