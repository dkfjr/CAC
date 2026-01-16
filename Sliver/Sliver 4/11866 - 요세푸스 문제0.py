import sys
input = sys.stdin.readline

num, jum=map(int, input().split())
remove=[]
res=[]
index=0

for i in range(num):
    res.append(i+1)
for j in range(num):
    index=(index+(jum-1)) % len(res)
    remove.append(res.pop(index))
result="<"+", ".join(map(str,remove))+">"
print(result)