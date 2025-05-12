def fib_recursive(n):
    if n == 1 or n == 2:
        return 1
    return fib_recursive(n-1) + fib_recursive(n-2)

def fib_non_recursive(n):
    if n == 1 or n == 2:
        return 1
    a, b = 1, 1
    for _ in range(n-2):
        a, b = b, a + b
    return b

m = int(input(""))
recursive_terms = [fib_recursive(i) for i in range(1, m+1)]
non_recursive_terms = [fib_non_recursive(i) for i in range(1, m+1)]

print(''.join(f"{num:5d}" for num in recursive_terms))
print(''.join(f"{num:5d}" for num in non_recursive_terms))