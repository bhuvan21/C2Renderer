
from Vector3 import Vector3
from structures import Color, Light, Material
from Sphere import Sphere
import numpy as np
import tqdm
from PIL import Image

resolution = [1000, 500]


m = Material(Color(0.5, 0.1, 0.1), Color(0.5, 0.1, 0.1), Color(0.5, 0.1, 0.1), 0.2)

objects = [Sphere(Vector3(0, 0, 5), 1, m)]
lights = [Light(Vector3(-2, 2, 3), Color(.8, .8, .8), Color(.8, .8, .8))]
ambient_intensity = Color(0.2, 0.2, 0.2)

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
                normal = (p - hit.position).normalized()
                
                ambient_component = ambient_intensity*hit.material.ambient_constant
                final = ambient_component
                for light in lights:
                    light_vector = (light.position - p).normalized()
                    if (light_vector * normal).product < 0:

                        continue
                    else:
                        diffuse_component = (light_vector * normal).product*hit.material.diffuse_constant*light.diffuse_intensity
                        reflectance = (2.0*normal*light_vector*normal)-light_vector
                        
                        view = (p - origin).normalized()
                        specular_component = light.specular_intensity*hit.material.specular_constant*((reflectance*view)**hit.material.shininess)
                        final = diffuse_component + final
                print(reflectance.values, view.values, specular_component.values, diffuse_component.values, final.values)
                image[-1].append((final*255.0).values)

            else:
                image[-1].append((0, 0, 0))
        
        
        #print(alpha, beta,direction.values, origin.values)
    
    Image.fromarray(np.uint8(np.array(image))).save('epic.png')
            
render()
