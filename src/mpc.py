import numpy as np
import cvxpy as cp

from lib.state import State
from lib.control import Control

D_MAX = 100  # 100 x 100 meters
V_MAX = 10  # 10 m/s
A_MAX = 2.5  # 2.5 m/s^2

Q = np.diag([1.0, 0.5, 1.0, 0.5])
R = np.diag([0.01, 0.01])

EPSILON = 0.1


class ModelPredictiveControl:
    def __init__(self, n, m, T, dt=0.025):
        self.n = n  # number of states
        self.m = m  # number of inputs
        self.T = T  # horizon

        self.t = 0
        self.dt = dt

    def iterate(self, z0, target):
        state = z0
        while all(magnitude > EPSILON for magnitude in state.magnitude()):
            control = self.solve(state, target)
            state = State(
                0.5*control.ax()*(self.dt**2) + state.vx()*self.dt + state.x(),
                0.5*control.ay()*(self.dt**2) + state.vy()*self.dt + state.y(),
                control.ax()*self.dt + state.vx(),
                control.ay()*self.dt + state.vy()
            )
            self.t += self.dt
            print(f"state: {state}")
            print(f"control: {control}")
            print()
            break

    def solve(self, state, target):
        z = cp.Variable((self.m, self.T+1))  # state
        z0 = np.copy(state.z)
        u = cp.Variable((self.n, self.T))  # inputs

        objective = 0.0
        constraints = []
        A, B, C, D = self.state_space()

        for t in range(self.T):
            constraints += [z[:,t+1] == A@z[:,t] + B@u[:,t]]
            objective += cp.quad_form(target.z - z[:,t], Q)
            # objective += cp.quad_form(u[:,t], R)


        constraints += [z[:,0] == z0]
        constraints += [z[0,:] >= 0, z[0,:] <= D_MAX]
        constraints += [z[2,:] >= 0, z[2,:] >= D_MAX]
        constraints += [cp.power(z[1,:],2) + cp.power(z[3,:],2) <= V_MAX**2]
        constraints += [cp.power(u[0,:],2)+cp.power(u[1,:],2) <= A_MAX**2]

        problem = cp.Problem(cp.Minimize(objective), constraints)
        problem.solve(solver=cp.ECOS, verbose=False)

        if (problem.status == cp.OPTIMAL or problem.status == cp.OPTIMAL_INACCURATE):
            solution = Control(u.value[0,0], u.value[1,0])
        else:
            print("Error: Cannot solve mpc")
            solution = Control(0, 0)

        return solution

    def state_space(self):
        A = np.array([[0, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 0, 0]])
        B = np.array([[0, 0],
                      [1, 0],
                      [0, 0],
                      [0, 1]])
        C = np.array([[1, 0, 0, 0],
                      [0, 0, 1, 0]])
        D = np.array([[0, 0],
                      [0, 0]])
        return A, B, C, D


if __name__ == "__main__":
    z0 = State(x=1, y=1, dx=0, dy=0)
    target = State(x=10, y=10, dx=20, dy=20)
    mpc = ModelPredictiveControl(
        m=4,  # 4 states: x, y, vx, vy
        n=2,  # 2 inputs: ax, ay
        T=5  # horizon = 5
    )
    mpc.iterate(z0, target)

