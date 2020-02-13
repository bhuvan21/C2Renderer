
from Vector3 import Vector3
from structures import Color, Light, Material
from Sphere import Sphere
from Triangle import Triangle
import numpy as np
import tqdm
from PIL import Image
import math
from multiprocessing import Pool, Queue, Manager

import time
resolution = [1000, 500]


m = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 50)
m2 = Material(Color(0.1, 0.1, 0.6), Color(0.1, 0.1, 0.6), Color(0.3, 0.3, 0.3), 2)
c = Vector3(0, 0, -1)

with open("20mm_cube.stl", "r") as f:
    lines = f.readlines()
vs = [x for x in lines if "vertex" in x]
theta = 2*math.pi/8
points = []
for v in vs:
    parts = v.split(" ")
    while len(parts) >= 5:
        parts.pop(0)

    newv = Vector3((float(parts[1])/5)-2, (float(parts[2])/5)+2, (float(parts[3])/5)+5)
    newnewv = Vector3((newv[0]*math.cos(theta) + newv[2]*math.sin(theta)), newv[1],((-newv[0]*math.sin(theta))+(newv[2]*math.cos(theta))))
    newnewnewv = Vector3(newnewv[0]-5, newnewv[1], newnewv[2]+4)
    points.append(newnewnewv)

tris = []

'''
You have the center C and the normal n. To determine whether point B is clockwise or counterclockwise from point A, 
calculate dot(n, cross(A-C, B-C)). If the result is positive, B is counterclockwise from A; if it's negative, B is clockwise from A.
'''

def is_clockwise(a, b, c, n):
    x = (n*((a-c).cross(b-c))).product
    if x > 0:
        return False
    else:
        return True


for p in range(0, len(points), 3):
    average = (points[p]+points[p+1]+points[p+2])*(1/3)
    
    ps = [points[p], points[p+1], points[p+2]]
    n = (ps[1] - ps[0]).cross((ps[2] - ps[0]))
    newps = []
    if is_clockwise(ps[0], ps[1], average, n):
        newps += [ps[1], ps[0]]
    else:
        newps += [ps[0], ps[1]]

    if is_clockwise(ps[1], ps[2], average, n):
        newps.append(ps[2])
    elif is_clockwise(ps[2], ps[0], average, n):
        newps.insert(1, ps[2])
    else:
        newps = [ps[2]]+ newps
    tris.append(Triangle(newps[0], newps[1], newps[2], m2))

newtris = []
for i, tri in enumerate(tris):
    view = (tri.V1+tri.V2+tri.V3)*(1/3) - c
    n = (tri.V2 - tri.V1).cross((tri.V3-tri.V1))

    if not 180-math.acos((view*n).product/view.length/n.length)*180/math.pi > 90:
        newtris.append(tri)

print("culled from {} to {}".format(len(tris), len(newtris)))

#objects = [Sphere(Vector3(4, 0, 8), 1, m), Sphere(Vector3(-4, 0, 8), 1, m2)]
objects = newtris

lights = [Light(Vector3(3, 0, 3), Color(.7, .7, .7), Color(.7, .7, .7))]
ambient_intensity = Color(0.3, 0.3, 0.3 )

x2 = Vector3(1, resolution[1]/resolution[0], 0)
x1 = Vector3(-1, resolution[1]/resolution[0], 0)
x4 = Vector3(1, -resolution[1]/resolution[0], 0)
x3 = Vector3(-1, -resolution[1]/resolution[0], 0)



width = x2[0] - x1[0]
height = x2[1] - x3[1]

image = np.zeros(shape=(resolution[1], resolution[0], 3))


def single_ray(x, y, beta):

    


    alpha = x/resolution[0]

    t1 = ((1-alpha)*x1)
    t2 = (alpha*x2)
    t = t1+t2

    b = ((1-alpha)*x3)+(alpha*x4)

    origin = ((1-beta)*t) + (beta * b)
    direction = origin - c

    ts = []
    for obj in objects:
        for t in obj.intersect(direction, origin):
            ts.append([t, obj])
    #print(ts)
    
    if ts != []:
        smallest = 999999
        i = 0
        for n, t in enumerate(ts):

            if t[0] < smallest:
                smallest = t[0]
                i = n
        
        #print(ts[i])
        t = smallest
        hit = ts[i][1]
        p = origin + t*direction
        if type(ts[i][1]) == Sphere:
            normal = (p - hit.position).normalized()
        elif type(ts[i][1]) == Triangle:
            tri = ts[i][1]
            normal = ((tri.V2 - tri.V1).cross((tri.V3-tri.V1))).normalized()
        

        ambient_component = ambient_intensity*hit.material.ambient_constant
        final = ambient_component
        for light in lights:
            l2 = (light.position - p)
            light_vector = (light.position - p).normalized()
            if (light_vector * normal).product < 0:

                continue
            else:
                diffuse_component = (light_vector * normal).product*hit.material.diffuse_constant*light.diffuse_intensity
                intensity = (normal*light_vector).product
                reflectance = 2*normal*(normal*light_vector).product - light_vector
                
                view = (origin - p).normalized()
                #if (view*reflectance).product > 1:
                    #print(view.values, reflectance.values, (view*reflectance).product)
                specular_component = hit.material.specular_constant*light.specular_intensity*(max(0, (view*reflectance).product))**hit.material.shininess
                
                final = diffuse_component + specular_component + final
        #print(reflectance.values, view.values, specular_component.values, diffuse_component.values, final.values)
        final = (final*255.0).values
        
        final = [max(0, min(x, 255)) for x in final]
        
        return final

    else:
        
        return [0, 0, 0]

def render():
    p = Pool(12)
        
    arglist = []

    for y in tqdm.tqdm(range(0, resolution[1])):

        beta = y/resolution[1]
        for x in range(0, resolution[0]):
            arglist.append([x, y, beta])

    results = []
    for a in arglist:
        results.append(p.apply_async(single_ray, args=a,))

    p.close()
    p.join()
    results = [r.get() for r in results]
    image = []
    i = 0
    for y in range(0, resolution[1]):
        image.append([])
        for x in range(0, resolution[0]):
            image[y].append(results[i])
            i += 1
    Image.fromarray(np.uint8(np.array(image))).save('test.png')

        
        

if __name__ == '__main__': 
    t= time.time()
    render()
    print(time.time()-t)
