import numpy as np

class State:
    def __init__(self, x, dx, y, dy):
        self.z = np.array([x, dx, y, dy])

    def __str__(self):
        return f"(x: {self.z[0]}, dx: {self.z[1]}, y: {self.z[2]}, dy: {self.z[3]})"

    def __eq__(self, s):
        return self.z == s.z

    def __add__(self, s):
        return self.z + s.z

    def __sub__(self, s):
        return self.z - s.z

    def __mul__(self, k):
        return self.z * k

    def __truediv__(self, k):
        return self.z / k

    def x(self):
        return self.z[0]
    def vx(self):
        return self.z[1]
    def y(self):
        return self.z[2]
    def vy(self):
        return self.z[3]

    def position(self):
        return np.array([self.z[0], self.z[1]])
    def velocity(self):
        return np.array([self.z[2], self.z[3]])
    def magnitude(self):
        return np.linalg.norm(self.position()), np.linalg.norm(self.velocity())

