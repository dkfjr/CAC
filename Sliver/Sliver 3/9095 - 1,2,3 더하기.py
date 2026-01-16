import sys
input = sys.stdin.readline

N=int(input())
for i in range(N):
    a=int(input())
    dp=[0]*(a+1)
    for i in range(1,a+1):
        if(i==1):
            dp[i]=1
        elif(i==2):
            dp[i]=2
        elif(i==3):
            dp[i]=4
        else:
            dp[i]=dp[i-3]+dp[i-2]+dp[i-1]
    print(dp[a])