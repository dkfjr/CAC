import sys
input = sys.stdin.readline

x=int(input())

queue=[]

for i in range(x):
    y=input().strip().split()
    st=y[0]
    if(st=="push"):
        queue.append(y[1])
    if(st=="front"):
        if(len(queue)==0):
            print("-1")
        else:
            print(f"{queue[0]}")
    if(st=="back"):
        if(len(queue)==0):
            print("-1")
        else:
            print(f"{queue[-1]}")
    if(st=="size"):
        print(len(queue))
    if(st=="empty"):
        if(len(queue)==0):
            print("1")
        else:
            print("0")
    if(st=="pop"):
        if(len(queue)==0):
            print("-1")
        else:   
            print(f"{queue[0]}")
            queue.pop(0)
        