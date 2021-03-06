'''Sphere class. Includes basic definition of a sphere, as well as sphere intersection test'''

from utils import solve_quadratic

# spheres are initialsed from a position, radius and material
# they are the simplest objects
class Sphere():
    def __init__(self, position, radius, material):
        self.position = position
        self.material = material
        self.radius = radius
        self.diameter = radius*2

    # constructs a quadratic equation to find the intersections of the given ray and the sphere
    # returns t values, when given ray_direction (a vector of the ray's direction) and ray_origin (a vector for the ray's origin)
    # (t*ray_direction) + ray_origin = point on sphere
    def intersect(self, ray_direction, ray_origin):
        '''Contruct and solve a quadratic equation to find the intersection of the given ray and this sphere'''
        a = ray_direction.length**2

        to_sphere = ray_origin - self.position
        b = (ray_direction*to_sphere).product*2

        c = (to_sphere.length**2) - (self.radius**2)

        ts = solve_quadratic(a, b, c)
        
        return ts