from utils import solve_quadratic

class Sphere():
    def __init__(self, position, radius, material):
        self.position = position
        self.material = material
        self.radius = radius
        self.diameter = radius*2

    
    def intersect(self, ray_direction, ray_origin):
        a = ray_direction.length**2

        to_sphere = ray_origin - self.position
        b = (ray_direction*to_sphere).product*2

        c = (to_sphere.length**2) - (self.radius**2)
        #print("ABC", a, b, c, ray_direction.values, to_sphere.values)
        t = solve_quadratic(a, b, c)
        
        #print(t)
        return t