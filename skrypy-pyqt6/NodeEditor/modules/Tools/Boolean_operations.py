class x_Greater_y:
    """
    Check if x > y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x > y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_Equal_y:
    """
    Check if x == y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x == y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_Less_y:
    """
    Check if x &lt; y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x < y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_Not_Equal_y:
    """
    Check if x != y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x != y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_GreaterOrEqual_y:
    """
    Check if x >= y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x >= y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_LessOrEqual_y:
    """
    Check if x &lt;&#61; y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0):
        self.res = x <= y

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_is_None:
    """
    Check if x == None

    Args:
        x: (float) a float number

    Returns::
      out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0):
        self.res = x is None

    def out(self: 'bool'):
        return self.res

###############################################################################


class x_Equal_y_dyn:
    """
    Check if x == y

    Args:
        x: (float) a float number
        y: (float) a float number

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, x=0.0, y=0.0, **dynamicsInputs):
        self.res = x == y
        for di in dynamicsInputs:
            self.res = self.res and y == dynamicsInputs[di]

    def out(self: 'bool'):
        return self.res

###############################################################################


class all_iterable:
    """
    Returns true if all of the items are True (or if the iterable is empty).

    Args:
        list_bool: (list of bool)

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, list_bool=[True]):
        self.res = all(list_bool)

    def out(self: 'bool'):
        return self.res

###############################################################################


class any_iterable:
    """
    Returns true if any of the items is True and returns False if empty or all are false.

    Args:
        list_bool: (list of bool)

    Returns:
        out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, list_bool=[True]):
        self.res = any(list_bool)

    def out(self: 'bool'):
        return self.res

###############################################################################


class AND_dyn:
    def __init__(self, bool_in=True, **dynamicsInputs):
        self.res = bool_in
        for di in dynamicsInputs:
            self.res = self.res and dynamicsInputs[di]

    def out(self: 'bool'):
        return self.res

###############################################################################


class OR_dyn:
    def __init__(self, bool_in=True, **dynamicsInputs):
        self.res = bool_in
        for di in dynamicsInputs:
            self.res = self.res or dynamicsInputs[di]

    def out(self: 'bool'):
        return self.res

###############################################################################


class NOT:
    def __init__(self, bool_in=True):
        self.res = not bool_in

    def out(self: 'bool'):
        return self.res

###############################################################################


class isinstance_var:
    """
    checks if the object (var) is an instance of type specifying by type_compare.

    Args:
        var: (any type) can take any type of variable (int, float, list of int, list of float, string, dict, tuple etc..)
        type_compare: (str) 'int', 'float', 'list', 'complex', 'str', 'dict', 'tuple' or 'set'

    Returns::
      out: (boolean) check condition (True or False)

    Note:
        GUI: no
    """
    def __init__(self, var='', type_compare="enumerate(('int', 'float', 'list', 'complex', 'str', 'dict', 'tuple', 'set'))"):
        known_types = {'int': int, 'float': float, 'list': list, 'complex': complex, 'str': str, 'dict': dict, 'tuple': tuple, 'set': set}
        if type_compare in known_types.keys():
            self.res = isinstance(var, known_types[type_compare])
        else:
            self.res = isinstance(var, type_compare)

    def out(self: 'bool'):
        return self.res

###############################################################################
