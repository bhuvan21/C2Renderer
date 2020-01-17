from math import sqrt

def solve_quadratic(a, b, c):
    if a != 0 and b != 0:
        d = (b**2)-(4*a*c)
        if d < 0:
            return []
        elif d == 0:
            return [((-b) + sqrt((b**2)-(4*a*c)))/(2*a)]
        else:
            return [((-b) + sqrt((b**2)-(4*a*c)))/(2*a), ((-b) - sqrt((b**2)-(4*a*c)))/(2*a)]
    elif a == 0 and b != 0:
        return [(-c)/b]
    else:
        return []
