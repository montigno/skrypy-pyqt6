class float_list_add_element_dyn():
    def __init__(self, list_float_in=[0.0], float_in=0.0, **dynamicsInputs):
        self.out = list_float_in.copy()
        self.out.append(float_in)
        for di in dynamicsInputs:
            self.out.append(dynamicsInputs[di])

    def list_float(self: 'list_float'):
        return self.out

#############################################################################


class float_list_extend_dyn():
    def __init__(self, list_float_in=[0.0], **dynamicsInputs):
        self.listConcat = [list_float_in.copy()]
        for di in dynamicsInputs:
            self.listConcat.append(dynamicsInputs[di].copy())

    def list_concat(self: 'list_float'):
        return self.listConcat

###############################################################################


class float_list_getElement():
    def __init__(self, list_float_in=[0.0], index=0):
        self.outVal = list_float_in[index]

    def out_list_indexed(self: 'float'):
        return self.outVal

###############################################################################


class float_list_get_sublist:
    def __init__(self, list_float_in=[0.0], index_start=0, index_end=1):
        if index_end < 0:
            index_end = len(list_float_in) + index_end + 1
        self.sublist = list_float_in[index_start:index_end]

    def index_element(self: 'list_float'):
        return self.sublist

###############################################################################


class float_list_length():
    def __init__(self, list_float_in=[0.0]):
        self.len = len(list_float_in)

    def length(self: 'int'):
        return self.len

###############################################################################


class float_list_mean:

    def __init__(self, list_float_in=[0.0]):
        import numpy as np
        self.result = np.mean(list_float_in)

    def mean(self: 'float'):
        return self.result

##############################################################################


class float_list_operations_dyn():
    def __init__(self, operation="enumerate(('add', 'sub', 'mul', 'div'))",
                 list_float_in=[0.0], **dynamicsInputs):
        self.result = list_float_in.copy()
        if operation == 'add':
            for di, vi in dynamicsInputs.items():
                if isinstance(vi, list) or type(vi).__name__ == 'ndarray':
                    self.result = [x+y for x, y in zip(self.result, vi)]
                else:
                    self.result = [x+vi for x in self.result]
        elif operation == 'sub':
            for di, vi in dynamicsInputs.items():
                if isinstance(vi, list) or type(vi).__name__ == 'ndarray':
                    self.result = [x-y for x, y in zip(self.result, vi)]
                else:
                    self.result = [x-vi for x in self.result]
        elif operation == 'mul':
            for di, vi in dynamicsInputs.items():
                if isinstance(vi, list) or type(vi).__name__ == 'ndarray':
                    self.result = [x*y for x, y in zip(self.result, vi)]
                else:
                    self.result = [x*vi for x in self.result]
        elif operation == 'div':
            for di, vi in dynamicsInputs.items():
                if isinstance(vi, list) or type(vi).__name__ == 'ndarray':
                    self.result = [x/y for x, y in zip(self.result, vi)]
                else:
                    self.result = [x/vi for x in self.result]

    def out_result(self: 'list_float'):
        return self.result

##############################################################################


class float_list_reverse():
    def __init__(self, list_float_in=[0.0]):
        self.rev = list(reversed(list_float_in))

    def list_reversed(self: 'list_float'):
        return self.rev

##############################################################################


class float_list_to_array_dyn():
    def __init__(self, list_float_in=[0.0], **dynamicsInputs):
        self.out = [list_float_in.copy()]
        for di in dynamicsInputs:
            self.out.append(dynamicsInputs[di])

    def array(self: 'array_float'):
        return self.out

##############################################################################


class float_list_to_int_list():
    """
    Allows the conversion of a float list to an integer list.
        Example  [0.1 , 1.1 , 2.2 ] --> [0 , 1 , 2]

    Args:
        listFloat : (list of float) list of floating values

    Returns:
        outListInt: (list of integer) list of integer values

    Note:
        GUI: no
    """
    def __init__(self, list_float_in=[0.0]):
        self.outlistint = [int(i) for i in list_float_in]

    def outListInt(self: 'list_int'):
        return self.outlistint

##############################################################################


class float_list_to_negative:

    def __init__(self, list_float_in=[0.0]):
        import numpy as np
        self.result = np.negative(list_float_in)

    def listDiv(self: 'list_float'):
        return self.result.tolist()

##############################################################################


class float_list_to_string_list():
    def __init__(self, list_float_in=[0.0]):
        self.outStr = [str(x) for x in list_float_in]

    def outString(self: 'list_str'):
        return self.outStr

##############################################################################


class float_list_to_tuple():
    def __init__(self, list_float_in=[0.0]):
        self.outTuple = tuple(list_float_in)

    def outTuple(self: 'tuple'):
        return self.outTuple
