class float_array_add_column():
    def __init__(self, array_float_in=[[0.0]], new_column=[0.0], index=0):
        import numpy as np
        if index < 0:
            index = len(array_float_in[0]) + index + 1
        arr = np.array(array_float_in)
        col = np.array(new_column)
        self.out = np.insert(arr, index, col, axis=1)

    def new_array(self: 'array_float'):
        return self.out

##############################################################################


class float_array_add_row():
    def __init__(self, array_float_in=[[0.0]], new_row=[0.0], index=0):
        import numpy as np
        if index < 0:
            index = len(array_float_in) + index + 1
        arr = np.array(array_float_in)
        row = np.array(new_row)
        self.out = np.insert(arr, index, row, axis=0)

    def new_array(self: 'array_float'):
        return self.out

##############################################################################


class float_array_append_dyn():
    def __init__(self, array_float_in=[[0.0]], **dynamicsInputs):
        self.arr = []
        self.arr.append(array_float_in)
        for di, vi in dynamicsInputs.items():
            self.arr.append(vi)

    def outArray(self: 'array_float'):
        return self.arr

##############################################################################


class float_array_concatenate_dyn():
    def __init__(self, array_float_in=[[0.0]], **dynamicsInputs):
        import numpy as np
        self.arr = np.array(array_float_in)
        print(dynamicsInputs)
        for di, vi in dynamicsInputs.items():
            self.arr = np.concatenate((self.arr, vi), dtype=float)

    def outArray(self: 'array_float'):
        return self.arr

##############################################################################


class float_array_get_dimension():
    def __init__(self, array_float_in=[[0.0]]):
        try:
            self.dim = (len(array_float_in[0]), len(array_float_in[0][0]), len(array_float_in))
        except Exception as err:
            self.dim = (len(array_float_in[0]), len(array_float_in))

    def dim_array(self: 'tuple'):
        return self.dim

##############################################################################


class float_array_getElement():
    def __init__(self, array_float_in=[[0.0]], index1=0, index2=0):
        self.out = array_float_in[index1][index2]

    def outArray(self: 'float'):
        return self.out

##############################################################################


class float_array_getRow():
    def __init__(self, array_float_in=[[0.0]], row=0):
        self.outList = array_float_in[row]

    def outList(self: 'list_float'):
        return self.outList

##############################################################################


class float_array_getColumn():
    def __init__(self, array_float_in=[[0.0]], column=0):
        self.out = [row[column] for row in array_float_in]

    def outColumn(self: 'list_float'):
        return self.out

##############################################################################


class float_array_getSubarray():
    def __init__(self, array_float_in=[[0.0]], row=(0, 1), column=(0, 1)):
        self.out = [i[column[0]:column[1]] for i in array_float_in[row[0]:row[1]]]

    def out_subarray(self: 'array_float'):
        return self.out

##############################################################################


class float_array_mean:

    def __init__(self, array_float_in=[[0.0]]):
        import numpy as np
        self.result = np.mean(array_float_in)

    def mean(self: 'float'):
        return self.result

##############################################################################


class float_array_nlargest():
    """
    Check the n largest value in array input.

    Args:
        array_float_in: (array of float) array input
        n: (integer) number of desired largest values

    Returns:
        listMax: (list of float) list of n largest values of in_array

    Note:
        GUI: no
    """
    def __init__(self, array_float_in=[[0.0]], n=2):
        import numpy as np
        array_float_in = np.array(array_float_in)
        self.result_list = -np.sort(-array_float_in, axis=None)[0:n]

    def listMax(self: 'list_float'):
        return self.result_list.tolist()

##############################################################################


class float_array_nsmallest():
    """
    Check the n smallest value in array input.

    Args:
        array_float_in: (array of float) array input
        n: (integer) number of desired smallest values

    Returns:
        listMin: (list of float) list of n smallest values of in_array

    Note:
        GUI: no
    """
    def __init__(self, array_float_in=[[0.0]], n=2):
        import numpy as np
        self.result_list = np.sort(array_float_in, axis=None)[0:n]

    def listMin(self: 'list_float'):
        return self.result_list.tolist()

##############################################################################


class float_array_operations_dyn():
    def __init__(self, operation="enumerate(('add', 'sub', 'mul', 'div'))",
                 array_float_in=[[0.0]], **dynamicsInputs):
        import numpy as np
        self.result = np.array(array_float_in)
        if operation == 'add':
            for di, vi in dynamicsInputs.items():
                self.result = np.add(self.result, np.array(vi))
        elif operation == 'sub':
            for di, vi in dynamicsInputs.items():
                self.result = np.subtract(self.result, np.array(vi))
        elif operation == 'mul':
            for di, vi in dynamicsInputs.items():
                self.result = np.multiply(self.result, np.array(vi))
        elif operation == 'div':
            for di, vi in dynamicsInputs.items():
                self.result = np.divide(self.result, np.array(vi))
        self.result = self.result.tolist()

    def out_result(self: 'array_float'):
        return self.result

##############################################################################


class float_array_transpose():
    def __init__(self, array_float_in=[[0.0]]):
        self.out = list(map(list, zip(*array_float_in)))

    def transp_out(self: 'array_float'):
        return self.out

##############################################################################


class float_array_to_int_array():
    """
    Allows the conversion of a float array to an integer array.
        Example  [[0.1] , [1.1] , [2.2]] --> [[0] , [1] , [2]]

    Args:
        array_float_in : (array of float) array of floating values

    Returns:
        outArrayInt: (array of integer) array of integer values

    Note:
        GUI: no
    """
    def __init__(self, array_float_in=[[0.0]]):
        import numpy as np
        self.outarrayint = np.array(array_float_in)
        self.outarrayint = self.outarrayint.astype(int)

    def outArrayInt(self: 'array_int'):
        return self.outarrayint.tolist()

##############################################################################


class float_array_to_negative:

    def __init__(self, array_float_in=[[0.0]]):
        import numpy as np
        self.result = np.negative(array_float_in)

    def listDiv(self: 'array_float'):
        return self.result.tolist()

##############################################################################


class float_array_to_string_array():
    def __init__(self, array_float_in=[[0.0]]):
        self.outStr = []
        for y in array_float_in:
            self.outStr.append([str(x) for x in y])

    def outString(self: 'array_str'):
        return self.outStr

##############################################################################
