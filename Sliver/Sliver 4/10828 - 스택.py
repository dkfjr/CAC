import sys
input = sys.stdin.readline

x=int(input())

stack=[]

for i in range(x):
    y=input().strip().split()
    st=y[0]
    if(st=="push"):
        stack.append(y[1])
    if(st=="top"):
        if(len(stack)==0):
            print("-1")
        else:
            print(f"{stack[-1]}")
    if(st=="size"):
        print(len(stack))
    if(st=="empty"):
        if(len(stack)==0):
            print("1")
        else:
            print("0")
    if(st=="pop"):
        if(len(stack)==0):
            print("-1")
        else:   
            print(f"{stack[-1]}")
            stack.pop()
        