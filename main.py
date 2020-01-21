
from Vector3 import Vector3
from structures import Color, Light, Material
from Sphere import Sphere
import numpy as np
import tqdm
from PIL import Image

resolution = [1000, 500]


m = Material(Color(0.5, 0.5, 0.5), Color(0.5, 0.5, 0.5), Color(0.5, 0.5, 0.5), 0.5)

objects = [Sphere(Vector3(0, 0, 5), 1, m)]
lights = [Light(Vector3(0, 8, 0), Color(1, 0, 0), Color(0, 1, 0))]
ambient_intensity = Color(0, 0, 1)

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

                image[-1].append(255)
            else:
                image[-1].append(0)
        #print(alpha, beta,direction.values, origin.values)
    
    Image.fromarray(np.uint8(np.array(image))).save('epic.png')
            
render()
