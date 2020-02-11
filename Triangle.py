
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
