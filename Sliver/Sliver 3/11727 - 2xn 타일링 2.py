import sys
input = sys.stdin.readline

N = int(input())
tile=[0]*(N+1)
tile[0]=1
tile[1]=3
for i in range(2, N+1):
    tile[i]=(tile[i-1]+tile[i-2]*2)%10007
print(tile[N-1])