
from Vector3 import Vector3
from structures import Color, Light, Material
from Sphere import Sphere
from Triangle import Triangle
import numpy as np
import tqdm
from PIL import Image
import math

resolution = [1000, 500]


m = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 50)
m2 = Material(Color(0.1, 0.1, 0.6), Color(0.1, 0.1, 0.6), Color(0.3, 0.3, 0.3), 50)

with open("20mm_cube.stl", "r") as f:
    lines = f.readlines()
vs = [x for x in lines if "vertex" in x]
theta = 2*math.pi/8
points = []
for v in vs:
    parts = v.split(" ")
    newv = Vector3((float(parts[1])/5)-2, (float(parts[2])/5)+2, (float(parts[3])/5)+5)
    newnewv = Vector3((newv[0]*math.cos(theta) + newv[2]*math.sin(theta)), newv[1],((-newv[0]*math.sin(theta))+(newv[2]*math.cos(theta))))
    newnewnewv = Vector3(newnewv[0]-5, newnewv[1], newnewv[2]+4)
    points.append(newnewnewv)
print(points[0].values)
tris = []
for p in range(0, len(points), 3):
    print(p)
    tris.append(Triangle(points[p], points[p+1], points[p+2], m2))




#objects = [Sphere(Vector3(4, 0, 8), 1, m), Sphere(Vector3(-4, 0, 8), 1, m2)]
objects = tris
lights = [Light(Vector3(0, -5, 0), Color(.7, .7, .7), Color(.7, .7, .7))]
ambient_intensity = Color(0.3, 0.3, 0.3 )

x2 = Vector3(1, resolution[1]/resolution[0], 0)
x1 = Vector3(-1, resolution[1]/resolution[0], 0)
x4 = Vector3(1, -resolution[1]/resolution[0], 0)
x3 = Vector3(-1, -resolution[1]/resolution[0], 0)

c = Vector3(0, 0, -1)

width = x2[0] - x1[0]
height = x2[1] - x3[1]



def render():
    image = []
    for y in tqdm.tqdm(range(0, resolution[1])):
        image.append([])
        beta = y/resolution[1]
        for x in range(0, resolution[0]):
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
                        if (view*reflectance).product > 1:
                            print(view.values, reflectance.values, (view*reflectance).product)
                        specular_component = hit.material.specular_constant*light.specular_intensity*(max(0, (view*reflectance).product))**hit.material.shininess
                        
                        final = diffuse_component + specular_component + final
                #print(reflectance.values, view.values, specular_component.values, diffuse_component.values, final.values)
                final = (final*255.0).values
                
                final = [max(0, min(x, 255)) for x in final]
                image[-1].append(final)

            else:
                image[-1].append((0, 0, 0))
        
        
        #print(alpha, beta,direction.values, origin.values)
    
    Image.fromarray(np.uint8(np.array(image))).save('epic.png')
            
render()
