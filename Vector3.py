from math import sqrt


class Vector3():
    def __init__(self, a=0, b=0, c=0, full=[0, 0, 0]):

        if full == [0, 0, 0]:
            self.values = [a, b, c]
        else:
            self.values = full

        self.product = self.values[0]+self.values[1]+self.values[2]
        

        self.length = sqrt((self.values[0]**2) + (self.values[1]**2) + (self.values[2]**2))

    
    def normalized(self):
        scale_factor = 1.0/self.length
        return scale_factor*self
    
    def cross(self, other):
        cx = (self.values[1]*other.values[2]) - (self.values[2]*other.values[1])
        cy = (self.values[2]*other.values[0]) - (self.values[0]*other.values[2])
        cz = (self.values[0]*other.values[1]) - (self.values[1]*other.values[0])
        return Vector3(cx, cy, cz)

    def __add__(self, other):
        
        r = []
        for i in range(3):
            r.append(self.values[i]+other.values[i])
        return Vector3(full=r)
    
    def __sub__(self, other):
        r = []
        for i in range(3):
            r.append(self.values[i]-other.values[i])
        return Vector3(full=r)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return self.values

    def __mul__(self, other):
        if type(other) == Vector3:
            r = []
            for i in range(3):
                r.append(self.values[i]*other.values[i])
            return Vector3(full=r)
        else:
            return Vector3(full=[other*y for y in self.values])

    def __rmul__(self, other):
        if type(other) == Vector3:
            r = []
            for i in range(3):
                r.append(self.values[i]*other.values[i])
            return Vector3(full=r)
        else:

            return Vector3(full=[other*y for y in self.values])
    
    def __pow__(self, other):
        return Vector3(full=[other**y for y in self.values])
    
