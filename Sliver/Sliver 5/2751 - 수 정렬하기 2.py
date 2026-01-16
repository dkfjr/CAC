import sys
input = sys.stdin.readline

x=int(input())
num=[]
for i in range(x):
    num.append(int(input()))
num.sort()
for j in num:
    print(j)