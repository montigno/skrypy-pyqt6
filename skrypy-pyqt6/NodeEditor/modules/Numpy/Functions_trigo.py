class numpy_trigonometry():
    def __init__(self, x=0.0,
                 op="enumerate(('sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan'))",
                 angle_type="enumerate(('degree','radian'))"):
        import numpy as np
        x = np.array(x)
        if op in ['sin', 'cos', 'tan']:
            if angle_type == 'degree':
                x = np.deg2rad(x)
                # x *= np.pi / 180.0
        self.reslt = getattr(np, op)(x)
        if op in ['arcsin', 'arccos', 'arctan']:
            if angle_type == 'degree':
                self.reslt = np.rad2deg(self.reslt)

    def res(self: 'float'):
        return self.reslt

##############################################################################


class numpy_sinc():
    def __init__(self, x=[0.0]):
        import numpy as np
        self.sc = np.sinc(x)

    def sinc(self: 'list_float'):
        return self.sc

##############################################################################
