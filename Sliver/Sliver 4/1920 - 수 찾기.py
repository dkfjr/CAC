import sys
input = sys.stdin.readline

x=int(input())
num=set(map(int,(input().split())))
'''set=탐색을 빠르게 하여 시간초과 해결 가능'''
y=int(input())
com=list(map(int,(input().split())))
for i in com:
    if i in num:
        print("1")
    else: print("0")