from math import gcd


def lcm(*integers):
    a = integers[0]
    for b in integers[1:]:
        a = (a * b) // gcd(a, b)
    return a