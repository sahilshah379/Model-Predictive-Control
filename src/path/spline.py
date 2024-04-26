import numpy as np

class QuinticSpline:
    def __init__(self, p0, p1):
        self.start = p0
        self.end = p1

        scale = 1.2*(p1-p0).positionMagnitude()
        x0 = p0.x
        x1 = p1.x
        dx0 = p0.vx/p0.velocityMagnitude()*scale
        dx1 = p1.vx/p1.velocityMagnitude()*scale
        ddx0 = 0
        ddx1 = 0
        y0 = p0.y
        y1 = p1.y
        dy0 = p0.vy/p0.velocityMagnitude()*scale
        dy1 = p1.vy/p1.velocityMagnitude()*scale
        ddy0 = 0
        ddy1 = 0

        self.compute_coefficients(x0,x1,dx0,dx1,ddx0,ddx1,y0,y1,dy0,dy1,ddy0,ddy1)
        self.parametrize(0,1)

    def compute_coefficients(self, x0, x1, dx0, dx1, ddx0, ddx1, y0, y1, dy0, dy1, ddy0, ddy1):
        self.a_x = -6*x0-3*dx0-0.5*ddx0+0.5*ddx1-3*dx1+6*x1
        self.b_x = 15*x0+8*dx0+1.5*ddx0-ddx1+7*dx1-15*x1
        self.c_x = -10*x0-6*dx0-1.5*ddx0+0.5*ddx1-4*dx1+10*x1

        self.d_x = 0.5*ddx0
        self.e_x = dx0
        self.f_x = x0

        self.a_y = -6*y0-3*dy0-0.5*ddy0+0.5*ddy1-3*dy1+6*y1
        self.b_y = 15*y0+8*dy0+1.5*ddy0-ddy1+7*dy1-15*y1
        self.c_y = -10*y0-6*dy0-1.5*ddy0+0.5*ddy1-4*dy1+10*y1

        self.d_y = 0.5*ddy0
        self.e_y = dy0
        self.f_y = y0

    def parametrize(self, t_low, t_high):
        p_low = self.get(t_low)
        p_high = self.get(t_high)

        t_mid = (t_low+t_high)/2
        p_mid = self.get(t_mid)

        delta_k = abs(self.curvature(t_low)-self.curvature(t_high))
        segment_length = self.approx_length(p_low, p_mid, p_high)

        if delta_k > max_delta_k or segment_length > max_segment_length:
            self.parametrize(t_low, t_mid)
            self.parametrize(t_mid, t_high)
        else:
            self.length += segment_length
            self.ssamples.append(self.length)
            self.tsamples.append(t_high)
            self.psamples.append(Pose(self.get(t_high).x,self.get(t_high).y))
            self.csamples.append(self.curvature(t_high))

    def get(self, t):
        x = round(self.a_x*t**5+self.b_x*t**4+self.c_x*t**3+self.d_x*t**2+self.e_x*t+self.f_x,5)
        y = round(self.a_y*t**5+self.b_y*t**4+self.c_y*t**3+self.d_y*t**2+self.e_y*t+self.f_y,5)
        return Pose(x,y)
