import math
from Vector3 import Vector3
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

def rotate(obj, angles):
    vertexes = obj.vertexes
    return rotate_vertexes(vertexes, angles)

def scale_vertexes(vertexes, scale_factor):
    print(vertexes[0])
    new_vertexes = []
    for v in vertexes:
        new_vertexes.append(Vector3(v[0]*scale_factor[0], v[1]*scale_factor[1], v[2]*scale_factor[2]))
    return new_vertexes

def scale(obj, scale_factor):
    vertexes = obj.vertexes
    return scale_vertexes(vertexes, scale_factor)

def translate_vertexes(vertexes, translation):
    
    new_vertexes = []
    for v in vertexes:
        new_vertexes.append(Vector3(v[0]+translation[0], v[1]+translation[1], v[2]+translation[2]))
    return new_vertexes


def translate(obj, translation):
    vertexes = obj.vertexes
    return translate_vertexes(vertexes, translation)

def is_clockwise(a, b, c, n):
    x = (n*((a-c).cross(b-c))).product
    if x > 0:
        return False
    else:
        return True

def add_STL(objects, stl):
    objects += stl.tris
    return objects