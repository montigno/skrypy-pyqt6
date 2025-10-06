class gen_abscissa:
    """
    Generate an abscissa list from xmin to xmax in steps of delta_x.
    Example (xmin=0.0, xmax=10.0, delta_x=0.1) --> [0.0, 0.1, ...., 9.9, 10.0].

    Args:
        xmin : (float) minimum value
        xmax : (float) maximal value
        delta_x: (float) deviation of x

    Returns:
        outAbscissa: (list of float) list of abscissa of x

    Note:
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, xmin=0.0, xmax=10.0, delta_x=1.0):
        import numpy as np
        self.x = list(np.linspace(xmin,
                                  xmax,
                                  int(1 + (xmax - xmin) / delta_x)))

    def outAbscissa(self: 'list_float'):
        return self.x

##############################################################################


class gen_list_of_integer:
    """
    Create a list of integer number 0 to n-1.

    Args:
        n: (integer) an integer number

    Returns:
        serie_int: (list of integer) a list of integer number 0 to n-1

    Note:
      GUI: no
    """
    def __init__(self, n=10):
        self.serie = range(0, n)

    def serie_int(self: 'list_int'):
        return self.serie

##############################################################################


class gen_list_of_integer_2():
    """
    Create a list of integer number start to end-1.

    Args:
        start: (integer) an integer number
        end: (integer) an integer number

    Returns:
        serie_int: (list of integer)

    Note:
      GUI: no
    """
    def __init__(self, start=0, end=10):
        self.serie = range(start, end + 1)

    def serie_int(self: 'list_int'):
        return self.serie

##############################################################################


class gen_list_of_zero_float:
    def __init__(self, n=10):
        self.serie = [0.0 for x in range(0, n)]

    def serie_float(self: 'list_float'):
        return self.serie

##############################################################################


class gen_noise:
    def __init__(self, size=5, scale=1.0):
        import numpy as np
        self.noise = np.random.normal(size=size, scale=scale)

    def noisy_signal(self: 'list_float'):
        return self.noise

##############################################################################


class gen_random_float():
    def __init__(self):
        import numpy as np
        self.randout = np.random.rand(1, 1)[0][0]

    def rand_out(self: 'float'):
        return self.randout

##############################################################################


class gen_random_list_float():
    def __init__(self, n=10):
        import numpy as np
        self.randout = np.random.rand(1, n)[0].tolist()

    def rand_out(self: 'list_float'):
        return self.randout

##############################################################################


class gen_random_float_2D():
    '''
    Generate a random image 2D (row, column)

    Args:
        row: (integer) number of rows
        col: (integer) number of columns

    Returns:
        rand_out: (array of float) image 2D

    Note:
        dependencies: Numpy
        GUI: no
    '''
    def __init__(self, row=10, col=10):
        import numpy as np
        self.randout = np.random.rand(row, col).tolist()

    def rand_out(self: 'array_float'):
        return self.randout

##############################################################################


class gen_random_float_3D():
    """
    Generate a random image 3D (row, column and slice)

    Args:
        row: (integer) number of rows
        col: (integer) number of columns
        slice: (integer) number of slices

    Returns:
        rand_out: (array of float) image 3D

    Note:
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, row=10, col=10, slice=10):
        import numpy as np
        self.randout = np.random.rand(row, col, slice).tolist()

    def rand_out(self: 'array_float'):
        return self.randout

##############################################################################


class gen_random_float_4D():
    """
    Generate a random image 4D (row, column, slice and temporel)

    Args:
        row: (integer) number of rows
        col: (integer) number of columns
        slice: (integer) number of slices
        temporal: (integer) number of temporal stacks

    Returns:
        rand_out: (array of float) image 4D

    Note:
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, row=10, col=10, slice=10, temporal=10):
        import numpy as np
        self.randout = np.random.rand(row, col, slice, temporal).tolist()

    def rand_out(self: 'array_float'):
        return self.randout

##############################################################################


class gen_random_float_5D():
    """
    Generate a random image 5D (row, column, slice, temporal and canal)

    Args:
        row: (integer) number of rows
        col: (integer) number of columns
        slice: (integer) number of slices
        temporal: (integer) number of temporal stacks
        canal:  (integer) number of canals

    Returns:
        rand_out: (array of float) image 5D

    Note:
        dependencies: Numpy
        GUI: no
    """
    def __init__(self, row=10, col=10, slice=10, temporal=10, canal=10):
        import numpy as np
        self.randout = np.random.rand(row,
                                      col,
                                      slice,
                                      temporal,
                                      canal).tolist()

    def rand_out(self: 'array_float'):
        return self.randout

##############################################################################
