import sys
input = sys.stdin.readline

x=int(input())
word=[]
for i in range(x):
    word.append(input().strip())
s_word=list(set(word))
s_word.sort(key=lambda x: (len(x), x))    
for j in s_word:
    print(j)