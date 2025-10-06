class fact:
    """
    return x factorial as integer

    Args:
        enter_int: (integer) an integer number

    Returns:
        factorial: (integer) factorial of enter_int

    Note:
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, enter_int=0):
        import os
        from numpy.ctypeslib import load_library
        path_so = os.path.dirname(os.path.realpath(__file__))
        path_so = os.path.join(path_so, 'sources')
        cal = load_library('lib_fact.so', path_so)
        self.out = cal.fact(enter_int)

    def factorial(self: 'int'):
        return self.out
