import sys
input = sys.stdin.readline

N=int(input())
wave=[0]*101
for i in range(N):
    M=int(input())
    for j in range(M+1):
        if(j<3):
            wave[j]=1
        else:
            wave[j]=wave[j-3]+wave[j-2]
    print(wave[M-1])