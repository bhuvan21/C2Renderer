'''assorted functions for various uses'''
import math
from Vector3 import Vector3
from math import sqrt

# solves quadratic equations of the form 0 = ax^2 + bx + c
def solve_quadratic(a, b, c):
    if a != 0 and b != 0:
        # calculate the discriminant
        d = (b**2)-(4*a*c)
        
        if d < 0:
            # no real solutions
            return []
        elif d == 0:
            # one real solution
            return [((-b) + sqrt((b**2)-(4*a*c)))/(2*a)]
        else:
            # two real solutions
            return [((-b) + sqrt((b**2)-(4*a*c)))/(2*a), ((-b) - sqrt((b**2)-(4*a*c)))/(2*a)]
    elif a == 0 and b != 0:
        # this is a linear equation ( 0x^2 + bx + c = 0)
        return [(-c)/b]
    else:
        # this is just an statement (c = 0)
        return []

# helper function to rotate vertices by use of rotation matrices
def rotate_vertexes(vertexes, angles):
    angles = Vector3(angles[0]*2*math.pi/360, angles[1]*2*math.pi/360, angles[2]*2*math.pi/360)
    new_vertexes = []
    for v in vertexes:
        xtheta = angles[0]
        newv = Vector3(v[0], (v[1]*math.cos(xtheta) - v[2]*math.sin(xtheta)),((v[1]*math.sin(xtheta))+(v[2]*math.cos(xtheta))))
        

        ytheta = angles[1]
        newv = Vector3((newv[0]*math.cos(ytheta) + newv[2]*math.sin(ytheta)), newv[1],((-newv[0]*math.sin(ytheta))+(newv[2]*math.cos(ytheta))))

        ztheta = angles[2]
        newv = Vector3((newv[0]*math.cos(ztheta) - newv[1]*math.sin(ztheta)), ((newv[0]*math.sin(ztheta))+(newv[1]*math.cos(ztheta))), newv[2])
        new_vertexes.append(newv)
    
    return new_vertexes

# simple, but useful (rotates an STL)
def rotate(obj, angles):
    vertexes = obj.vertexes
    return rotate_vertexes(vertexes, angles)

# scales vertices about 0, 0, 0
def scale_vertexes(vertexes, scale_factor):
    print(vertexes[0])
    new_vertexes = []
    for v in vertexes:
        new_vertexes.append(Vector3(v[0]*scale_factor[0], v[1]*scale_factor[1], v[2]*scale_factor[2]))
    return new_vertexes

# simple, but useful (scales an STL)
def scale(obj, scale_factor):
    vertexes = obj.vertexes
    return scale_vertexes(vertexes, scale_factor)

# translates vertices
def translate_vertexes(vertexes, translation):
    new_vertexes = []
    for v in vertexes:
        new_vertexes.append(Vector3(v[0]+translation[0], v[1]+translation[1], v[2]+translation[2]))
    return new_vertexes

# simple, but useful (translates an STL)
def translate(obj, translation):
    vertexes = obj.vertexes
    return translate_vertexes(vertexes, translation)

# returns whether vector a is clockwise FROM vector b, when given their average (c) and a normal (n)
def is_clockwise(a, b, c, n):
    x = (n*((a-c).cross(b-c))).product
    if x > 0:
        return False
    else:
        return True

# small but useful
def add_STL(objects, stl):
    objects += stl.tris
    return objects