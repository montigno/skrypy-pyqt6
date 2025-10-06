class Scipy_statLoogiddtic:
    def __init__(self):
        from scipy.interpolate import interp1d
        import matplotlib.pyplot as plt
        import numpy as np
        x = np.linspace(0, 10, num=11, endpoint=True)
        y = np.cos(-x ** 2 / 9.0)
        f = interp1d(x, y)
        f2 = interp1d(x, y, kind='cubic')
        xnew = np.linspace(0, 10, num=41, endpoint=True)
        plt.ion()
        plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['data', 'linear', 'cubic'], loc='best')
        plt.show()

###############################################################################


class Fit_T1:
    def __init__(self, x=[0.0], y=[0.0], Mo=100.0, T1=1.0, C=1.0, n=20):
        import numpy as np
        import scipy.optimize as opt
        import matplotlib.pyplot as plt
        global np
        plt.ion()
        x = np.asarray(x)
        y = np.asarray(y)
        a, b, b = Mo, T1, C
        (a_, b_, c_), _ = opt.curve_fit(self._f, x, y)
        y_fit = self._f(x, a_, b_, c_)
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.plot(x, y, 'o')
        ax.plot(x, y_fit, '-')
        textstr = '\n'.join((
            r'MO*(1-2*C*exp(-x/T1))',
            r'MO=%.2f' % (a_,),
            r'T1=%.2f' % (b_,),
            r'C=%.2f' % (c_,)))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05,
                0.95,
                textstr,
                transform=ax.transAxes,
                fontsize=12,
                horizontalalignment='left',
                verticalalignment='top',
                bbox=props)
        ax.set_title('Fit_T1')
        plt.show()

    def _f(self, x, a, b, c):
        return a * (1 - 2 * c * np.exp(-x / b))

###############################################################################


class Fit_T2:
    def __init__(self, x=[0.0], y=[0.0], Mo=100.0, T2=1.0, C=1.0, n=20):
        import numpy as np
        import scipy.optimize as opt
        import matplotlib.pyplot as plt
        global np
        plt.ion()
        x = np.asarray(x)
        y = np.asarray(y)
        a, b, c = Mo, T2, C
        (a_, b_, c_), _ = opt.curve_fit(self._f, x, y)

        y_fit = self._f(x, a_, b_, c_)

        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.plot(x, y, 'o')
        ax.plot(x, y_fit, '-')
        textstr = '\n'.join((
            r'MO*exp(-x/T2)+C',
            r'MO=%.2f' % (a_,),
            r'T2=%.2f' % (b_,),
            r'C=%.2f' % (c_,)))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05,
                0.95,
                textstr,
                transform=ax.transAxes,
                fontsize=12,
                horizontalalignment='left',
                verticalalignment='top',
                bbox=props)
        ax.set_title('Fit_T2')
        plt.show()

    def _f(self, x, a, b, c):
        return a * (np.exp(-x / b)) + c
