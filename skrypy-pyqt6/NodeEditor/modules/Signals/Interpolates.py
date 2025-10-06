class interpolate_cubic_spline():
    def __init__(self, x=[0.0], y=[0.0], n=50, **options):
        import numpy as np
        from scipy.interpolate import CubicSpline
        f = CubicSpline(x, y, **options)
        self.x_new = np.linspace(x[0], x[-1], n)
        self.cs = f(self.x_new)

    def spline_cubic(self: 'list_float'):
        return self.cs

    def x_new(self: 'list_float'):
        return self.x_new

##############################################################################


class interpolate_polynomial():
    def __init__(self, x=[0.0], y=[0.0], n=10, deg=1, **options):
        import numpy as np
        coeff = np.polyfit(x, y, deg)
        yn = np.poly1d(coeff)
        self.xn = np.linspace(x[0], x[-1], n)
        self.intpol = yn(self.xn)
        self.coeff = []
        for i in range(deg+1):
            self.coeff.append(yn[i])

    def polyn_interp(self: 'list_float'):
        return self.intpol

    def x_new(self: 'list_float'):
        return self.xn

    def coefficients(self: 'list_float'):
        return self.coeff

##############################################################################


class interpolate_interp1d():
    def __init__(self, x=[0.0], y=[0.0], **options):
        from scipy import interpolate
        self.ax = interpolate.interp1d(x, y, **options)

    def interp1d(self: 'list_float'):
        return self.ax
