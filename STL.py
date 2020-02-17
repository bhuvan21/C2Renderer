'''STL Class. Contains triangle culling algorithm, as well as STL intersection test (simply many triangle intersection tests)'''
from Vector3 import Vector3
import math
from utils import rotate_vertexes, translate_vertexes, scale_vertexes, is_clockwise
from Triangle import Triangle

class STL():
    def __init__(self, filename="", vertexes=[], scale_factor=Vector3(1, 1, 1), rotation=Vector3(0, 0, 0), translation=(0, 0, 0), material=None, camera=None):
        self.filename = filename
        self.vertices = []
        self.material = material
        
        # read in stl file and parse it for raw vertex data
        with open(filename, "r") as f:
            lines = f.readlines()
        string_vertexes = [x for x in lines if "vertex" in x]
        points = []
        for v in string_vertexes:
            parts = v.split(" ")
            while len(parts) >= 5:
                parts.pop(0)

            newv = Vector3(float(parts[1]), float(parts[2]), float(parts[3]))

            points.append(newv)

        # apply given transformations to all vertices of the STL
        points = scale_vertexes(points, scale_factor)
        points = rotate_vertexes(points, rotation)
        points = translate_vertexes(points, translation)


        # simple back face triangle culling
        tris = []
        # organise all triangles into same circular point order
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
            tris.append(Triangle(newps[0], newps[1], newps[2], material))

        # cull the triangles facing backwards
        newtris = []
        badtris = 0
        for i, tri in enumerate(tris):
            view = (tri.V1+tri.V2+tri.V3)*(1/3) - camera
            n = (tri.V2 - tri.V1).cross((tri.V3-tri.V1))
            try:
                #print(tri.V1.values, tri.V2.values, tri.V3.values, view.values, n.values)
                if not 180-math.acos((view*n).product/view.length/n.length)*180/math.pi > 90:
                    newtris.append(tri)
            except ZeroDivisionError:
                badtris+=1
        print("{} bad triangles".format(badtris))
        print("culled from {} to {}".format(len(tris), len(newtris)))
        self.tris = newtris
        self.vertices = points
    
    # conducts triangle intersection tests for every sub triangle
    def intersect(self, ray_direction, ray_origin):
        ts = []
        for t in self.tris:
            ts += t.intersect(ray_direction, ray_origin)
        return ts
