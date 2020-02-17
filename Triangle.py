'''Triangle Class. Contains triangle definition as well as triangle intersection test'''
from utils import is_clockwise

class Triangle():
    def __init__(self, V1, V2, V3, material, normal=None):
        points = [V1, V2, V3]

        average = (points[0]+points[1]+points[2])*(1/3)
        
        n = (points[1] - points[0]).cross((points[2] - points[0]))
        newps = []
        if is_clockwise(points[0], points[1], average, n):
            newps += [points[1], points[0]]
        else:
            newps += [points[0], points[1]]

        if is_clockwise(points[1], points[2], average, n):
            newps.append(points[2])
        elif is_clockwise(points[2], points[0], average, n):
            newps.insert(1, points[2])
        else:
            newps = [points[2]]+ newps

        self.vertices = newps
        self.V1 = newps[0]
        self.V2 = newps[1]
        self.V3 = newps[2]

        self.material = material
        if normal is not None:
            self.normal = normal
        else:
            self.normal = ((self.V2 - self.V1).cross((self.V3-self.V1))).normalized()
    
    def intersect(self, ray_direction, ray_origin):
        plane_normal = ((self.V2 - self.V1).cross((self.V3-self.V1))).normalized()
        d = (plane_normal*self.V1).product
        
        if (plane_normal*ray_direction).product == 0:
            return []
        t = (d-(plane_normal*ray_origin).product)/(plane_normal*ray_direction).product
        Q = ray_origin + (t*ray_direction)

        edge1_test = (((self.V2-self.V1).cross(Q-self.V1))*plane_normal).product >= 0
        edge2_test = (((self.V3-self.V2).cross(Q-self.V2))*plane_normal).product >= 0
        edge3_test = (((self.V1-self.V3).cross(Q-self.V3))*plane_normal).product >= 0

        if edge1_test and edge2_test and edge3_test:

            return [t]
        return []
