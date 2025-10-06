class numpy_abs():
    """
    Returns the absolute value of the array elements.

    Args:
        y: (array of float) array input

    Returns:
        abs: (array of float) absolute of y

    Note:
        GUI: no
    """
    def __init__(self, y=[0.0]):
        import numpy as np
        self.abs = np.absolute(y)

    def abs(self: 'list_float'):
        return self.abs

##############################################################################


class numpy_exponential():
    """
    Returns the exponential of the array elements.

    Args:
        y: (array of float) array input

    Returns:
        exp: (array of float) exponential of y

    Note:
        GUI: no
    """
    def __init__(self, y=[0.0]):
        import numpy as np
        self.exp = np.exp(y)

    def exp(self: 'list_float'):
        return self.exp

##############################################################################


class numpy_RMS():
    """
    Returns the Root Mean Square of the array elements.

    Args:
        y: (array of float) array input

    Returns:
        rms: (array of float) rms of y

    Note:
        GUI: no
    """
    def __init__(self, y=[0.0]):
        import numpy as np
        y = np.array(y)
        self.rms = np.sqrt(np.mean(y ** 2))

    def rms(self: 'float'):
        return self.rms

##############################################################################


class numpy_std():
    """
    Returns the standard deviation of the array elements.

    Args:
        y: (array of float) array input

    Returns:
        std: (array of float) standard deviation of y

    Note:
        GUI: no
    """
    def __init__(self, y=[0.0]):
        import numpy as np
        self.std = np.std(y)

    def rms(self: 'float'):
        return self.std

##############################################################################


class numpy_mean_array():
    def __init__(self, y=[[0.0]]):
        import numpy as np
        self.mean = np.mean(y)

    def rms(self: 'float'):
        return self.mean
