import itertools

A = [5, 4]
B = [7, 8, 9]
C = [5, 7, 8, 9, 10]
full = [A, B, C]
A, B, C = list(set(A)), list(set(B)), list(set(C))
result = itertools.product(*full)

print((list(result)))
