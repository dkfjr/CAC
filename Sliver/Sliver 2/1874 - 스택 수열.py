import sys
input = sys.stdin.readline

N = int(input())
stack=[]
answer=[]
num=1
output=True
for i in range(N):
    n=int(input())
    while(num<=n):
        stack.append(num)
        answer.append("+")
        num+=1
    if(stack[-1]==n):
        stack.pop()
        answer.append("-")
    else:
        output=False
if output:
    for char in answer:
        print(char)
else:
    print("NO")