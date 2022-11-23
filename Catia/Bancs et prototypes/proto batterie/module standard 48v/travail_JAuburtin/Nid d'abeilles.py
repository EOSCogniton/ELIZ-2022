import math

c = 11

L = []

for n in range(83,92):
    n0 = (2*n+1-c)/(2*c)
    if n0 == math.floor(n0):
        L.append(n0)

print(L)