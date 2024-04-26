import numpy as np

class Control:
    def __init__(self, ax, ay):
        self.u = np.array([ax, ay])

    def __str__(self):
        return f"(ax: {self.u[0]}, ay: {self.u[1]})"

    def __eq__(self, s):
        return self.u == s.u

    def __add__(self, s):
        return self.u + s.u

    def __sub__(self, s):
        return self.u - s.u

    def __mul__(self, k):
        return self.u * k

    def __truediv__(self, k):
        return self.u / k

    def ax(self):
        return self.u[0]
    def ay(self):
        return self.u[1]

    def magnitude(self):
        return np.linalg.norm(self.u)

