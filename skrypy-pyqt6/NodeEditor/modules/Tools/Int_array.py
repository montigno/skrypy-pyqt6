class int_array_to_float_array():
    """
    Allows the conversion of an integer array to a floating array.
        Example [[0] , [1] , [2]] --> [[0.0] , [1.0] , [2.0]]

    Args:
        array_int_in: (array of integer) array of integer values

    Returns:
        outArrayFloat: (array of float) array of floating values

    Note:
        GUI: no
    """
    def __init__(self, array_int_in=[[0]]):
        import numpy as np
        self.outarrayfloat = np.array(array_int_in)
        self.outarrayfloat = self.outarrayfloat.astype(float)

    def outArrayFloat(self: 'array_float'):
        return self.outarrayfloat.tolist()


###############################################################################
