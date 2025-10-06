class string_array_to_float_array():
    def __init__(self, array_string_in=[['']]):
        import numpy as np
        array_string_in = np.array(array_string_in)
        self.outarrayfloat = array_string_in.astype(float)

    def outArrayFloat(self: 'array_float'):
        return self.outarrayfloat.tolist()

###############################################################################


class string_array_concatenat_dyn:
    def __init__(self, array_string_in=[['']], array_0=[['']], **dynamicsInputs):
        self.stringArray = array_string_in.copy()
        self.stringArray.extend(array_0)
        for di in dynamicsInputs:
            self.stringArray.extend(dynamicsInputs[di])

    def out_array(self: 'array_str'):
        return self.stringArray

##############################################################################


class string_array_getElement():
    def __init__(self, array_string_in=[['']], row=0, column=0):
        self.out = array_string_in[row][column]

    def out_subarray(self: 'str'):
        return self.out

#############################################################################


class string_array_getSubarray():
    def __init__(self, array_string_in=[['']], row=(0, 1), column=(0, 1)):
        self.out = [i[column[0]:column[1]] for i in array_string_in[row[0]:row[1]]]

    def out_subarray(self: 'array_str'):
        return self.out

#############################################################################


class string_array_merge_dyn:
    def __init__(self, array_string_in=[['']], array_0=[['']], **dynamicsInputs):
        self.stringArray = []
        for i in range(len(array_string_in)):
            rowList = []
            rowList.extend(array_string_in[i])
            rowList.extend(array_0[i])
            for di in dynamicsInputs:
                rowList.extend(dynamicsInputs[di][i])
            self.stringArray.append(rowList)

    def out_array(self: 'array_str'):
        return self.stringArray

##############################################################################


class string_array_index:
    def __init__(self, array_string_in=[['']], index_start=0, index_end=1):
        if index_end == 0:
            self.res = array_string_in[index_start:]
        else:
            self.res = array_string_in[index_start:index_end]

    def out_subarray(self: 'array_str'):
        return self.res

###############################################################################


class string_array_getcolumn:
    def __init__(self, array_string_in=[['']], index_column=0):
        self.res = [row[index_column] for row in array_string_in]

    def out_column(self: 'list_str'):
        return self.res

###############################################################################


class string_array_remove_column:
    def __init__(self, array_string_in=[['']], index_column=0):
        import numpy as np
        self.out = np.delete(array_string_in, index_column, axis=1)

    def new_array(self: 'array_str'):
        return self.out

###############################################################################


class string_array_remove_row:
    def __init__(self, array_string_in=[['']], index_row=0):
        import numpy as np
        self.out = np.delete(array_string_in, index_row, axis=0)

    def new_array(self: 'array_str'):
        return self.out
