from Vector3 import Vector3
from structures import Color, Light, Material
from Sphere import Sphere
from Triangle import Triangle
import numpy as np
import tqdm
from PIL import Image
import math
from multiprocessing import Pool, Queue, Manager
from utils import add_STL
import time
from STL import STL

resolution = [1000, 500]
x2 = Vector3(1, resolution[1]/resolution[0], 0)
x1 = Vector3(-1, resolution[1]/resolution[0], 0)
x4 = Vector3(1, -resolution[1]/resolution[0], 0)
x3 = Vector3(-1, -resolution[1]/resolution[0], 0)
c = Vector3(0, 0, -1)

width = x2[0] - x1[0]
height = x2[1] - x3[1]

m = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 50)
m2 = Material(Color(0.1, 0.1, 0.6), Color(0.1, 0.1, 0.6), Color(0.3, 0.3, 0.3), 2)

objects = []
objects = add_STL(objects, STL(filename="20mm_cube.stl", camera=c, material=m2, scale_factor=(0.15, 0.15, 0.15), rotation=(15, 45, 0), translation=(-0.5, 3, 8)))

lights = [Light(Vector3(6, -1, 3), Color(.7, .7, .7), Color(.7, .7, .7))]
ambient_intensity = Color(0.3, 0.3, 0.3 )

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
    
    if ts != []:
        smallest = 999999
        i = 0
        for n, t in enumerate(ts):

            if t[0] < smallest:
                smallest = t[0]
                i = n
        
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
            light_vector = (light.position - p).normalized()
            if (light_vector * normal).product < 0:

                continue
            else:
                diffuse_component = (light_vector * normal).product*hit.material.diffuse_constant*light.diffuse_intensity
                reflectance = 2*normal*(normal*light_vector).product - light_vector
                view = (origin - p).normalized()
                specular_component = hit.material.specular_constant*light.specular_intensity*(max(0, (view*reflectance).product))**hit.material.shininess
                final = diffuse_component + specular_component + final
       
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