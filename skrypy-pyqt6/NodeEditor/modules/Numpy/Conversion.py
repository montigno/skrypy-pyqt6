class numpy_array_str():
    """
    Convert ndarray to string

    Args:
        arr: (ndarray)

    Returns:
        out_array_str: (string)

    Note:
        GUI: no
    """
    def __init__(self, arr=[[0.0]], **options):
        import numpy as np
        self.out = np.array_str(arr, **options)

    def out_array_str(self: 'str'):
        return self.out

##############################################################################


class numpy_array_bool_to_array_int():
    """
    Convert array of boolean to ndarray of int

    Args:
        array_float: (array of float)

    Returns:
        out_ndarray: (string)

    Note:
        GUI: no
    """
    def __init__(self, array_bool=[[True]]):
        import numpy as np
        self.output = array_bool.astype(int)

    def out_ndarray(self: 'array_int'):
        return self.output

##############################################################################


class numpy_array_float_to_ndarray():
    """
    Convert array of float to ndarray

    Args:
        array_float: (array of float)

    Returns:
        out_ndarray: (string)

    Note:
        GUI: no
    """
    def __init__(self, array_float=[[0.0]]):
        import numpy as np
        self.output = np.array(array_float)

    def out_ndarray(self: 'array_float'):
        return self.output

##############################################################################


class numpy_ndarray_to_float_list():
    def __init__(self, ndarray_list=[0.0]):
        self.out = list(ndarray_list)

    def outList(self: 'list_float'):
        return self.out

##############################################################################


class numpy_ndarray_to_float_array():
    def __init__(self, array_in=[[0.0]]):
        self.out_array = array_in.tolist()

    def out_array(self: 'array_float'):
        return self.out_array

##############################################################################


class numpy_str_list_to_float_Array():
    def __init__(self, list_str=['']):
        import numpy as np
        x = np.array(list_str)
        self.output = x.astype(np.float)

    def outArray(self: 'array_float'):
        return self.output

##############################################################################


class numpy_float_list_to_ndarray():
    def __init__(self, list_float=[0.0]):
        import numpy as np
        self.output = np.array(list_float)

    def outArray(self: 'list_float'):
        return self.output

##############################################################################


class numpy_float_list_to_array():
    def __init__(self, list_float=[0.0], x=0, y=0):
        import numpy as np
        self.output = np.reshape(list_float, (x, y))

    def outArray(self: 'array_float'):
        return self.output

##############################################################################


class numpy_flatten():
    """
    Returns contiguous flattened array.

    Args:
        array_in: (array of float) Input array
        order: (string)
            [C-contiguous, F-contiguous, A-contiguous; optional]
             C-contiguous order in memory(last index varies the fastest)
             C order means that operating row-rise on the array will be slightly quicker
             FORTRAN-contiguous order in memory (first index varies the fastest).
             F order means that column-wise operations will be faster.
             ‘A’ means to read / write the elements in Fortran-like index order if,
             array is Fortran contiguous in memory, C-like order otherwise

    Returns:
        outAarray: (list of float) Flattened array having same type as the Input array and and order as per choice

    Note:
        GUI: no
    """
    def __init__(self,
                 array_in=[[0.0]],
                 order="enumerate(('C', 'F', 'A', 'K'))"):
        import numpy as np
        a = np.array(array_in)
        self.output = a.flatten(order)

    def outArray(self: 'list_float'):
        return self.output

##############################################################################


class numpy_ravel():
    def __init__(self,
                 array_in=[[0.0]],
                 order="enumerate(('C','F', 'A', 'K'))"):
        import numpy as np
        a = np.array(array_in)
        self.output = a.ravel(order)

    def outArray(self: 'list_float'):
        return self.output

##############################################################################


class numpy_new_axis():
    def __init__(self, image_nd_array=[[0.0]]):
        import numpy as np
        self.new_img = image_nd_array[:, :, np.newaxis]

    def newAxis(self: 'array_float'):
        return self.new_img

##############################################################################


class numpy_reshape():
    def __init__(self, a=[[0.0]], newshape=(3,)):
        self.reshaped_arr = a.reshape(newshape)

    def reshaped(self: 'array_float'):
        return self.reshaped_arr
