'''STL Class. Contains triangle culling algorithm, as well as STL intersection test (simply many triangle intersection tests)'''
from Vector3 import Vector3
import math
from utils import rotate_vertexes, translate_vertexes, scale_vertexes, is_clockwise
from Triangle import Triangle

# this class takes a filename (of an obj) or a list of vertices as well as an optional, scale factor, rotation and translation
# all three are applied to the STL
# a material, camera location and culling flag are also taken in
# if culling is true, simple triangle culling will take place
class OBJ():
    def __init__(self, filename="", vertexes=[], scale_factor=Vector3(1, 1, 1), rotation=Vector3(0, 0, 0), translation=(0, 0, 0), material=None, camera=None, culling=True):
        self.filename = filename
        self.vertices = []
        self.material = material
        
        # read in obj file and parse it for raw vertex and face data
        with open(filename, "r") as f:
            lines = f.readlines()
        
        string_vertexes = [x for x in lines if x[:2] == "v "]
        string_normals = [x for x in lines if x[:2] == "vn"]
        string_faces = [x for x in lines if x[:2] == "f "]

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

        vertex_normals = []
        for n in string_normals:
            parts = n.split(" ")
            while len(parts) >= 5:
                parts.pop(0)
            vertex_normals.append(Vector3(float(parts[1]), float(parts[2]), float(parts[3])))

        vertex_normals = rotate_vertexes(vertex_normals, rotation)

        triangles = []
        for f in string_faces:
            face = []
            norms = []
            parts = f.split(" ")
            if len(parts) >= 5:
                print("bruh you ain't a triangle")
            else:
                
                if "//" in parts[1]:
                    for part in parts[1:]:
                        vert_i = int(part.split("//")[0])
                        norm_i = int(part.split("//")[1])
                        face.append(points[vert_i])
                        norms.append(vertex_normals[norm_i])
                elif parts[1].count("/") == 2:
                    for part in parts[1:]:
                        vert_i = int(part.split("/")[0])
                        norm_i = int(part.split("/")[2])
                        face.append(points[vert_i])
                        norms.append(vertex_normals[norm_i])
                        
            face_normal = (norms[0] + norms[1] + norms[2]) * (1/3)
            triangles.append(Triangle(face[0], face[1], face[2], normal=face_normal, material=material))
        
        # simple back face triangle culling
        # gets rid of all triangles which will not be seen by the camera, so that intersection tests for them do not need to occur
        if culling:
            # cull the triangles facing backwards
            newtri_normals = []
            newtris = []
            badtris = 0
            for i, tri in enumerate(triangles):
                view = (tri.V1+tri.V2+tri.V3)*(1/3) - camera
                n = (tri.V2 - tri.V1).cross((tri.V3-tri.V1))
                try:
                    # if the angle between the normal of the triangle and the view vector is less than 90, the triangle is seen
                    if not 180-math.acos((view*n).product/view.length/n.length)*180/math.pi > 90:
                        newtris.append(tri)
                        newtri_normals.append(tri_normals[i])
                except ZeroDivisionError:
                    # sometimes STLs have bad triangles, these are ignored
                    badtris+=1
            print("{} bad triangles".format(badtris))
            print("culled from {} to {}".format(len(tris), len(newtris)))
            self.tris = newtris
            self.normals = newtri_normals
        else:
            self.tris = triangles
            self.normals = tri_normals
        self.vertices = points
        
    # conducts triangle intersection tests for every sub triangle
    def intersect(self, ray_direction, ray_origin):
        ts = []
        for t in self.tris:
            ts += t.intersect(ray_direction, ray_origin)
        return ts
