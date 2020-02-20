'''Triangle Class. Contains triangle definition as well as triangle intersection test'''
from utils import is_clockwise

# the triangle class is instantiated with 3 vectors (one for each vertex), a material, and an optional normal vector
class Triangle():
    def __init__(self, V1, V2, V3, material, normal=None):
        points = [V1, V2, V3]

        # order the vertices in a clockwise order
        # this is important for the intersection tests
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

        # use the given normal if it exists, if not, calculate a possible normal
        if normal is not None:
            self.normal = normal
        else:
            self.normal = ((self.V2 - self.V1).cross((self.V3-self.V1))).normalized()
    
    # this intersection test returns an array of t values, when given a ray
    # ray_direction is a vector representing the direction of the ray, starting from the point ray_origin (another vector)
    # t values are solution to equations representing the intersection of the ray and the triangle
    # (t*ray_direction) + ray_origin = a point on the trirangle
    def intersect(self, ray_direction, ray_origin):
        # first see where the ray intersection with the plane of the triangle
        plane_normal = self.normal
        d = (plane_normal*self.V1).product
        
        if (plane_normal*ray_direction).product == 0:
            # the angle between the plane normal and the ray is 90, so there is no intersection
            return []
        
        # calculate the t value
        t = (d-(plane_normal*ray_origin).product)/(plane_normal*ray_direction).product
        # calculate the point of intersection
        Q = ray_origin + (t*ray_direction)
        # check if the point of intersection is with the triangle
        edge1_test = (((self.V2-self.V1).cross(Q-self.V1))*plane_normal).product >= 0
        edge2_test = (((self.V3-self.V2).cross(Q-self.V2))*plane_normal).product >= 0
        edge3_test = (((self.V1-self.V3).cross(Q-self.V3))*plane_normal).product >= 0

        if edge1_test and edge2_test and edge3_test:
            return [t]
        return []
