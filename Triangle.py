
class Triangle():
    def __init__(self, V1, V2, V3, material):
        self.V1 = V1
        self.V2 = V2
        self.V3 = V3
        self.vertices = [V1, V2, V3]
        self.material = material
    
    def intersect(self, ray_direction, ray_origin):
        plane_normal = ((self.V2 - self.V1).cross((self.V3-self.V1))).normalized()
        d = (plane_normal*self.V1).product

        t = (d-(plane_normal*ray_origin).product)/(plane_normal*ray_direction).product
        Q = ray_origin + (t*ray_direction)


        if (((self.V2-self.V1).cross(Q-self.V1))*plane_normal).product >= 0:
            print(d, t, (plane_normal*((self.V2 - self.V1).cross(Q-self.V1))).product, Q.values)
            return [t]
        return []
