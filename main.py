# external library imports
# for timing how long the render took
import time
# for trig functions and square rooting
import math
# for final image writing
import numpy as np
from PIL import Image
# for parallel processing
from multiprocessing import Pool

# all my code imports
from STL import STL
from OBJ import OBJ
from utils import add_STL
from Sphere import Sphere
from Vector3 import Vector3
from Triangle import Triangle
from structures import Color, Light, Material

# this function takes in the light ray it should simulate and information about the scene
# it then returns the color which should be used for the pixel for which this light ray was sent out
# it then calls itself recursively to simulate light reflecting and refracting
def reflect(ray_direction, origin, objects, lights, ambient_intensity, depth, prev_hit=None):
    # ray_direction and origin are vectors which represent the light ray
    # objects, lights and ambient_intensity contain information about the scene
    # depth keeps track of the recursion depth so that we don't get stuck infinitely
    # prev_hit contains information about the last surface which was hit by the last ray in this stream
    depth = depth - 1
    if depth >= 0:
        
        ts = []
        # get all the points of intersection of the ray and objects in the scene
        for obj in objects:
            if (prev_hit != None and obj != prev_hit) or prev_hit is None: 
                
                for t in obj.intersect(ray_direction, origin):
                    # discard backwards ray solutions
                    
                    if t > 0:
                        ts.append([t, obj])
                
        if ts != []:
            # if there are intersections, choose the one closest to the ray's origin
            smallest = 999999
            i = 0
            for n, t in enumerate(ts):

                if t[0] < smallest:
                    smallest = t[0]
                    i = n
            
            t = smallest
            hit = ts[i][1]
            # calculate point of intersection
            p = origin + t* ray_direction

            # get normal for intersection based on type of object which was hit
            if type(ts[i][1]) == Sphere:
                normal = (p - hit.position).normalized()
            elif type(ts[i][1]) == Triangle:
                tri = ts[i][1]
                normal = tri.normal
            
            # if the hit object's material refracts, do refraction math
            if (hit.material.refracts):

                # cosi = cos(incidence)
                cosi = max(-1, min(1, (p.normalized()*normal.normalized()).product))
                #eta i = refractive index of incident ray's medium
                etai = 1
                #et t = refractive index of refracted ray's medium
                etat = hit.material.refractive_index


                if cosi < 0:
                    # ray is coming from outside the object, cos(incidence) should be positive
                    cosi = -cosi
                else:   
                    # ray is coming from inside object, reverse the normal and swap refraction indexes
                    etai, etat = etat, etai
                    normal = -1*normal

                eta = etai/etat
                k = 1 - eta * eta * (1 - cosi * cosi)
                if k < 0:
                    # total internal reflection
                    kr = 1
                    kt = 0
                else:
                    
                    sint = etai/etat * math.sqrt(max(0, 1-cosi*cosi))
                    cost = math.sqrt(max(0, 1-sint*sint))
                    # use fresenel's equations to calculate ration of refracted to reflected light
                    rs = ((etat*cosi)-(etai*cost)) / ((etat*cosi) + (etai *cost))
                    rp = ((etai*cosi)-(etat*cost)) / ((etai*cosi) + (etat *cost))
                    kr = (rs*rs+rp*rp)/2
                    kt = 1-kr
                reflectance = ray_direction - 2*normal*(normal*ray_direction).product

                # return the combination of the refracted and reflected light
                # by sending out reflected and refracted rays, adding their contribution to the final pixel color
                return (kt*reflect(eta * p.normalized() + (eta *cosi - math.sqrt(k)) * normal, hit.position, objects, lights, ambient_intensity, depth+0.5, prev_hit=hit)) + (kr*reflect(reflectance, p, objects, lights, ambient_intensity, depth+0.5, prev_hit=hit))
                                  
            else:
                # reflection math if the object does not refract light

                # first, calculate ambient component of light
                ambient_component = ambient_intensity*hit.material.ambient_constant
                final = ambient_component

                # send out another ray to check if the object is in shadow
                for light in lights:
                    shadow = False
                    for obj in objects:
                        if obj != hit:
                            intersect = obj.intersect(light.position-p, p)
                            for inter in intersect:
                                if 0 < inter < 1:
                                    shadow = True


                    if not shadow:
                        # calculate diffuse component of light
                        light_vector = (light.position - p).normalized()
                        diffuse_component = (light_vector * normal).product*hit.material.diffuse_constant*light.diffuse_intensity
                        # calculate specular component of light
                        reflectance = 2*normal*(normal*light_vector).product - light_vector
                        view = (origin - p).normalized()
                        specular_component = hit.material.specular_constant*light.specular_intensity*(max(0, (view*reflectance).product))**hit.material.shininess
                        final = diffuse_component + specular_component + final
                    elif prev_hit == None:
                        # if the object is in shadow, use only ambient component of light
                        return final
                
            
                # send out the reflected ray and add its color contribution on
                reflectance = ray_direction - 2*normal*(normal*ray_direction).product
                final = Color(full=[max(0, min(x, 1)) for x in final])
                
                return final + (reflect(reflectance, p, objects, lights, ambient_intensity, depth, prev_hit=hit)*hit.material.reflectivity_constant)

        else:
            return Color(0, 0, 0)
    else:
        # max recursion depth reached, return an empty color
        return Color(0, 0, 0)



# the function is called once for each pixel, with information about the scene and camera
# handles anti-aliasing and sending out original rays from the camera/image plane
def single_ray(x, y, x1, x2, x3, x4, c, resolution, objects, lights, ambient_intensity, anti_aliasing):
    if x == 0:
        print(str(int(y/resolution[1]*100))+"% " + "done")


    oldx = x
    oldy = y
    pixel = [0, 0, 0]

    if anti_aliasing:
        loop = 3
    else:
        loop = 1
    for i in range(loop):
        for j in range(loop):
            if anti_aliasing:
                x = oldx - 0.33333 +(i*0.33333)
                y = oldy- 0.33333 +(j*0.33333)
            
            # calculate original ray information
            beta = y/resolution[1]
            alpha = x/resolution[0]

            t1 = ((1-alpha)*x1)
            t2 = (alpha*x2)
            t = t1+t2

            b = ((1-alpha)*x3)+(alpha*x4)

            origin = ((1-beta)*t) + (beta * b)
            direction = origin - c

            # send out original ray
            z = reflect(direction, origin, objects, lights, ambient_intensity, 3)
            z = [l*255 for l in z.values]
            z = [max(min(l, 255), 0) for l in z]

            pixel = [p + z for p,z in zip(pixel, z)]
    if anti_aliasing:

        return [p/9 for p in pixel]
    else:
        return pixel

# highest level function, takes in information about the scene, saves an image with the render
# essentially just calls single_ray a lot
def render(c, resolution, objects, lights, ambient_intensity, anti_aliasing=False):
    # image plane coordinates
    x2 = Vector3(1, resolution[1]/resolution[0], 0)
    x1 = Vector3(-1, resolution[1]/resolution[0], 0)
    x4 = Vector3(1, -resolution[1]/resolution[0], 0)
    x3 = Vector3(-1, -resolution[1]/resolution[0], 0)
    
    # Pool is used for conducting multiple raycasts simultaneously
    # adjust the '12' according to how much processing power you are willing to devote to the render
    p = Pool(12)
    
    # generate list of commands to execute in parallel
    arglist = []
    for y in range(0, resolution[1]):
        for x in range(0, resolution[0]):
            arglist.append([x, y, x1, x2, x3, x4, c, resolution, objects, lights, ambient_intensity, anti_aliasing])

    results = []
    for a in arglist:
        results.append(p.apply_async(single_ray, args=a,))

    # actually execute commands
    p.close()
    p.join()
    results = [r.get() for r in results]
    #write resultant pixel data to image
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
    # camera location
    c = Vector3(0, 0, -1)
    # CHANGE THINGS AFTER THIS POINT
    # setup code which is used for renders
    # all of this is adjustable depending on what you want to render
    # blue and red test materials, with different shininesses
    m = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 2, Color(0.3, 0.3, 0.3))
    m2 = Material(Color(0.1, 0.1, 0.6), Color(0.1, 0.1, 0.6), Color(0.3, 0.3, 0.3), 2,  Color(0.3, 0.3, 0.3))
    
    # mirror material, high reflectivity, low diffuse constant
    m3 = Material(Color(0.1, 0.1,0.1), Color(0.1,0.1,0.1), Color(0.2, 0.2, 0.2), 2, Color(0.7, 0.7, 0.7))
    # glass material, refracts, index of refraction is 1.5
    m4 = Material(Color(0.6, 0.1, 0.1), Color(0.6, 0.1, 0.1), Color(0.3, 0.3, 0.3), 2, Color(0.3, 0.3, 0.3), True, 1.5)
    

    # objects in the scene
    #objects = [Sphere(Vector3(0, 0, 8), 3, m)]
    #objects = [] + STL(filename="dragons.stl", rotation=Vector3(270, 40+180, 0), translation=Vector3(3, -3, 15), scale_factor=Vector3(.1, .1, .1), material=m, camera=c, culling=True).tris
    
    objects = [OBJ(filename="cube.obj", translation=(0, 0, 0), material=m, camera=c, culling=False)]

    # lighting information for the scene
    lights = [Light(Vector3(5 , 4, 2), Color(.7, .7, .7), Color(.7, .7, .7))]
    ambient_intensity = Color(0.2, 0.2, 0.2 )

    # information about the resultant image
    resolution = [500, 500]
    anti_aliasing = False
    
    render(c, resolution, objects, lights, ambient_intensity, anti_aliasing=anti_aliasing)
    print(time.time()-t)