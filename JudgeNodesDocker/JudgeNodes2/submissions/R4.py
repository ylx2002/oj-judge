a, b = input().split()
a = int(a)
b = int(b)
for i in range(1, 1000001):
    a=a+b*i
print(a)