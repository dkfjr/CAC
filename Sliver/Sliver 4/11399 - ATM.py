import sys
input = sys.stdin.readline()

n = int(input())
p_times = list(map(int, input().split()))
p_times.sort()

total_wait = 0   
current_wait = 0 

for time in p_times:
    current_wait += time
    total_wait += current_wait
print(total_wait)