import sys
from collections import deque
input = sys.stdin.readline

def DFS(v):
    dfs[v]=True
    print(v,end=' ')
    for i in graph[v]:
        if not dfs[i]:
            DFS(i)
def BFS(v):
    q=deque([v])
    bfs[v]=True
    while q:
        v=q.popleft()
        print(v,end=' ')
        for i in graph[v]:
            if not bfs[i]:
                q.append(i)
                bfs[i]=True
N, M, V=map(int,input().split())
dfs=[False]*(N+1)
bfs=[False]*(N+1)
graph=[[]*M]

for i in range(M):
    a, b= map(int,input().split())
    graph[a].append(b)
    graph[b].append(a)
for j in range(1, N+1):
    graph[j].sort()
DFS(V)
print()
BFS(V)