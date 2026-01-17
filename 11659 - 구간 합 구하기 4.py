import sys
input = sys.stdin.readline

N, M=map(int,input().split())
num = list(map(int, input().split()))
total=[0]
sum=0
for i in num:
    sum+=i
    total.append(sum)

for i in range(M): 
    a, b=map(int,input().split())
    print(total[b]-total[a-1])