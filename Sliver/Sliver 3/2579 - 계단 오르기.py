import sys
input = sys.stdin.readline

N=int(input())
dp=[0]*300
stair=[0]*300
for i in range(N):
    stair[i]=int(input())

dp[0]=stair[0]
dp[1]=stair[1]+stair[0]
dp[2]=max(stair[2]+stair[1],stair[2]+stair[0])
for i in range(3,N):
    dp[i]=max(dp[i-3]+stair[i]+stair[i-1],dp[i-2]+stair[i])
print(dp[N-1])