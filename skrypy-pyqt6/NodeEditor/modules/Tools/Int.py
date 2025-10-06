class int_operations_dyn():
    def __init__(self, operation="enumerate(('add', 'sub', 'mul', 'div'))",
                 list_float_in=0, **dynamicsInputs):
        self.result = list_float_in
        self.remain = 0
        if operation == 'add':
            for di, vi in dynamicsInputs.items():
                self.result = self.result + vi
        elif operation == 'sub':
            for di, vi in dynamicsInputs.items():
                self.result = self.result - vi
        elif operation == 'mul':
            for di, vi in dynamicsInputs.items():
                self.result = self.result * vi
        elif operation == 'div':
            for di, vi in dynamicsInputs.items():
                self.remain = self.result % vi
                self.result = self.result // vi

    def out_result(self: 'int'):
        return self.result

    def out_remainder(self: 'int'):
        return self.remain

#############################################################################


class int_to_list_dyn:
    def __init__(self, int_in=0, **dynamicsInputs):
        self.outList = [int_in]
        for di in dynamicsInputs:
            self.outList.append(dynamicsInputs[di])

    def out_list(self: 'list_int'):
        return self.outList

###############################################################################


class int_to_float():
    """
    Allows the conversion of an integer number to a float number.
        Example 2 --> 2.0

    Args:
        int_in: (integer) integer value

    Returns:
        outFloat: (float) floating value

    Note:
        GUI: no
    """
    def __init__(self, int_in=0):
        self.outfloat = float(int_in)

    def outFloat(self: 'float'):
        return self.outfloat

###############################################################################


class int_to_string():
    """
    Allows the conversion of a integer number to string.
        Example 1 --> '1'

    Args:
        int_in: (integer) integer number

    Returns:
        outString: (string) string of integer number

    Note:
        GUI: no
    """
    def __init__(self, int_in=0):
        self.outStr = str(int_in)

    def outString(self: 'str'):
        return self.outStr
