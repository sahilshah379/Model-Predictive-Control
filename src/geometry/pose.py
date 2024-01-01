from geometry.vector import Vector

class Pose:
    def __init__(self, x, y, vx=0, vy=0):
        self.pos = Vector(x, y)
        self.vel = Vector(vx, vy)

    def __str__(self):
        return f"pos: {self.pos}, vel: {self.vel}"

    def __add__(self, p):
        return Pose(self.pos + p.pos, self.vel + p.vel)

    def __sub__(self, p):
        return Pose(self.pos - p.pos, self.vel - p.vel)

    def __mul__(self, k):
        return Pose(self.pos * k, self.vel * k)

    def __truediv__(self, k):
        return Pose(self.pos / k, self.vel / k)

    def positionMagnitude(self):
        return self.pos.magnitude()

    def velocityMagnitude(self):
        return self.vel.magnitude()

    def position(self):
        return self.pos.vectorize()
    
    def velocity(self):
        return self.vel.vectorize()

