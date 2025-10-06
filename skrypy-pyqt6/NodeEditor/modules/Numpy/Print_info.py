class Info_ndarray:
    def __init__(self, ndarray_in=[[0.0]]):
        import numpy as np
        print(np.asarray(ndarray_in).shape)

##############################################################################


class numpy_len:
    def __init__(self, ndarray_in=[[0.0]]):
        self.len_arr = len(ndarray_in)

    def len_ndarray(self: 'int'):
        return self.len_arr

##############################################################################


class numpy_shape:
    def __init__(self, ndarray_in=[[0.0]]):
        self.shape = ndarray_in.shape

    def shape(self: 'tuple'):
        return self.shape
