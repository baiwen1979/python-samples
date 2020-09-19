# test.py
def factorial_r(n):
    if n < 2:
        return 1
    return n * factorial_r(n - 1)

print('10! = ', factorial_r(10))
