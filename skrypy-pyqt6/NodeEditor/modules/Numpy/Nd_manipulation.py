class numpy_append_dyn():
    def __init__(self, a1=[0.0], **dynamicsInputs):
        import numpy as np
        self.res = a1
        for di in dynamicsInputs:
            self.res = np.append(self.res, dynamicsInputs[di])

    def res(self: 'list_float'):
        return self.res

##############################################################################


class numpy_arange():
    def __init__(self, x=(1, 8)):
        import numpy as np
        self.res = np.arange(x[0], x[1])

    def res(self: 'list_int'):
        return self.res

##############################################################################


class numpy_interp():
    def __init__(self, x=0.0, xp=[0.0], yp=[0.0], **options):
        import numpy as np
        self.value = np.interp(x, xp, yp)

    def value_out(self: 'float'):
        return self.value

##############################################################################


class numpy_transpose():
    def __init__(self, a=[[0.0]]):
        import numpy as np
        self.p = np.transpose(a)

    def np_transpose(self: 'array_float'):
        return self.p

##############################################################################


class numpy_unique():
    """
    Find the unique elements of an array.
    Returns the sorted unique elements of an array. There are three optional
    outputs in addition to the unique elements:
    the indices of the input array that give the unique values
    the indices of the unique array that reconstruct the input array
    the number of times each unique value comes up in the input array

    Args:
        ar: array_like.
            Input array. Unless axis is specified, this will be flattened if it
            is not already 1-D.

    Returns:
        unique: ndarray. The sorted unique values.
        unique_indices: ndarray, optional.
                        The indices of the first occurrences of the unique values
                        in the original array.
                        Only provided if return_index is True.
        unique_inverse: ndarray, optional.
                        The indices to reconstruct the original array from the unique
                        array.
                        Only provided if return_inverse is True.
        unique_counts: ndarray, optional.
                       The number of times each of the unique values comes up in the
                       original array.
                       Only provided if return_counts is True.

    Notes:
        link_web: https://numpy.org/doc/stable/reference/generated/numpy.unique.html
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, ar=[[0.0]], **options):
        import numpy as np
        self.indices, self.inverse, self.counts = None, None, None
        self.unique = np.unique(ar, **options)
        if 'return_index' in options.keys():
            self.indices = True if options['return_index'] else None
        if 'return_inverse' in options.keys():
            self.inverse = True if options['return_inverse'] else None
        if 'return_counts' in options.keys():
            self.counts = True if options['return_counts'] else None

        if type(self.unique).__name__ == 'tuple':
            if (self.indices and self.inverse and self.counts):
                self.unique, self.indices, self.inverse, self.counts = self.unique
            elif (self.indices and self.inverse):
                self.unique, self.indices, self.inverse = self.unique
            elif (self.indices and self.counts):
                self.unique, self.indices, self.counts = self.unique
            elif (self.indices):
                self.unique, self.indices = self.unique
            elif (self.inverse and self.counts):
                self.unique, self.inverse, self.counts = self.unique
            elif (self.inverse):
                self.unique, self.inverse = self.unique
            elif (self.counts):
                self.unique, self.counts = self.unique

    def np_unique(self: 'array_float'):
        return self.unique

    def np_indices(self: 'array_float'):
        return self.indices

    def np_inverse(self: 'array_float'):
        return self.inverse

    def np_counts(self: 'array_float'):
        return self.counts
