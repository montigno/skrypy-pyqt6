class int_list_add_element_dyn:
    def __init__(self, list_int_in=[0], int_in=0, **dynamicsInputs):
        self.outList = list_int_in
        self.outList.append(int_in)
        for di in dynamicsInputs:
            self.outList.append(dynamicsInputs[di])

    def out_list(self: 'list_int'):
        return self.outList

###############################################################################


class int_list_extend_dyn():
    def __init__(self, list_int_in=[0], **dynamicsInputs):
        self.listConcat = [list_int_in.copy()]
        for di in dynamicsInputs:
            self.listConcat.append(dynamicsInputs[di].copy())

    def list_concat(self: 'list_int'):
        return self.listConcat

#####################################################################


class int_list_getElement:
    def __init__(self, list_int_in=[0], index=0):
        self.outVal = list_int_in[index]

    def out_list_indexed(self: 'int'):
        return self.outVal

###############################################################################


class int_list_length():
    def __init__(self, list_int_in=[0]):
        self.len = len(list_int_in)

    def length(self: 'int'):
        return self.len

###############################################################################


class int_list_operations_dyn():
    def __init__(self, operation="enumerate(('add', 'sub', 'mul', 'div'))",
                 list_float_in=[0], **dynamicsInputs):
        self.result = list_float_in.copy()
        self.remain = [0 for i in self.result]
        if operation == 'add':
            for di, vi in dynamicsInputs.items():
                self.result = [x+y for x, y in zip(self.result, vi)]
        elif operation == 'sub':
            for di, vi in dynamicsInputs.items():
                self.result = [x-y for x, y in zip(self.result, vi)]
        elif operation == 'mul':
            for di, vi in dynamicsInputs.items():
                self.result = [x*y for x, y in zip(self.result, vi)]
        elif operation == 'div':
            for di, vi in dynamicsInputs.items():
                self.remain = [x%y for x, y in zip(self.result, vi)]
                self.result = [x//y for x, y in zip(self.result, vi)]

    def out_result(self: 'list_int'):
        return self.result

    def out_remainder(self: 'list_int'):
        return self.remain

##############################################################################


class int_list_reverse():
    def __init__(self, list_int_in=[0]):
        self.rev = list(reversed(list_int_in))

    def list_reversed(self: 'list_int'):
        return self.rev

##############################################################################


class int_list_to_float_list():
    """
    Allows the conversion of an integer list to a float list.
        Example [0 , 1 , 2] --> [0.0 , 1.0 , 2.0]"

    Args:
        list_int_in: (list of integer) list of integer values

    Returns:
        outListFloat: (list of float) list of floating values

    Note:
        GUI: no
    """
    def __init__(self, list_int_in=[0]):
        self.outlistfloat = [float(i) for i in list_int_in]

    def outListFloat(self: 'list_float'):
        return self.outlistfloat
