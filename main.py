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

m = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 2, Color(0.3, 0.3, 0.3))
m2 = Material(Color(0.1, 0.1, 0.6), Color(0.1, 0.1, 0.6), Color(0.3, 0.3, 0.3), 2,  Color(0.3, 0.3, 0.3))
m3 = Material(Color(0.1, 0.1,0.1), Color(0.1,0.1,0.1), Color(0.2, 0.2, 0.2), 2, Color(0.7, 0.7, 0.7))

objects = []
#objects = [Sphere(Vector3(4, 0, 8), 3, m3), Sphere(Vector3(-4, 0, 8), 1, m2)]
objects = [Triangle(Vector3(-7, 7, 10), Vector3(7, -7, 10), Vector3(-7, -7, 10), m3), Triangle(Vector3(-7, 7, 10), Vector3(7, 7, 10), Vector3(7, -7, 10), m3), Sphere(Vector3(-3, 0, 5), 1, m2)]

lights = [Light(Vector3(0, 0, 7), Color(.7, .7, .7), Color(.7, .7, .7))]
ambient_intensity = Color(0.6, 0.6, 0.6 )

image = np.zeros(shape=(resolution[1], resolution[0], 3))


def reflect(ray_direction, origin, depth, prev_hit=None):
    depth = depth - 1
    if depth != 0:
        
        ts = []
        for obj in objects:
            if (prev_hit != None and obj != prev_hit) or prev_hit is None: 
                for t in obj.intersect(ray_direction, origin):
                    if t > 0:
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
            p = origin + t* ray_direction

            if type(ts[i][1]) == Sphere:
                normal = (p - hit.position).normalized()
            elif type(ts[i][1]) == Triangle:
                tri = ts[i][1]
                normal = ((tri.V2 - tri.V1).cross((tri.V3-tri.V1))).normalized()
            
            




            ambient_component = ambient_intensity*hit.material.ambient_constant
            final = ambient_component
            for light in lights:
                shadow = False
                for obj in objects:
                    if obj != hit:
                        intersect = obj.intersect(light.position-p, p)
                        for inter in intersect:
                            if 0 < inter < 1:
                                shadow = True

                if not shadow:
                    light_vector = (light.position - p).normalized()
                    if (light_vector * normal).product < 0:

                        continue
                    else:
                        diffuse_component = (light_vector * normal).product*hit.material.diffuse_constant*light.diffuse_intensity
                        reflectance = 2*normal*(normal*light_vector).product - light_vector
                        view = (origin - p).normalized()
                        specular_component = hit.material.specular_constant*light.specular_intensity*(max(0, (view*reflectance).product))**hit.material.shininess
                        final = diffuse_component + specular_component + final
                elif prev_hit == None:
                    return final
            
           
            
            reflectance = ray_direction - 2*normal*(normal*ray_direction).product
            try:

                final = Color(full=[max(0, min(x, 1)) for x in final])
                
            except Exception as e:
                print("UNEPIC OK TRHIS IS BAD")
                raise e
            if p[2] > 100:
                print("WAT THE ACTUAL FRICK")
                print(str(p.values)+str(hit))
            if depth == 1 and prev_hit == objects[1]:
                
                
                print("TS: " + str(ts) + "\nRay Direction: " + str(ray_direction.values) +"\nOrigin: " +str(origin.values)+ "\nV :" + "\nNormal: " + str(normal.values)+"\nReflect: " + str(reflectance.values)+"\nHit: " +str(p.values)+ " " + str(depth) + " uh")
            return final + (reflect(reflectance, p, depth, prev_hit=hit)*hit.material.reflectivity_constant)

            



        else:
            return Color(0, 0, 0)
    else:
        return Color(0, 0, 0)




def single_ray(x, y, beta):
    if x == 0:
        print(y)
    alpha = x/resolution[0]

    t1 = ((1-alpha)*x1)
    t2 = (alpha*x2)
    t = t1+t2

    b = ((1-alpha)*x3)+(alpha*x4)

    origin = ((1-beta)*t) + (beta * b)
    direction = origin - c

    
        

    z = reflect(direction, origin, 3)
    z = [l*255 for l in z.values]
    z = [max(min(l, 255), 0) for l in z]

    return z


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