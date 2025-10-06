class numpy_hyperbolic():
    def __init__(self, x=[0.0], op="enumerate(('sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh'))"):
        import numpy as np
        x = np.array(x)
        self.res = getattr(np, op)(x)

    def res(self: 'list_float'):
        return self.res

##############################################################################
