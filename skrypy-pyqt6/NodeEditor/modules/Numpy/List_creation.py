class numpy_arange():
    """
    Return evenly spaced values within a given interval.
    arange can be called with a varying number of positional arguments:
        arange(stop): Values are generated within the half-open interval
        [0, stop) (in other words, the interval including start but excluding
        stop).
        arange(start, stop): Values are generated within the half-open interval
        [start, stop).
        arange(start, stop, step) Values are generated within the half-open
        interval [start, stop), with spacing between values given by step.
    For integer arguments the function is roughly equivalent to the Python
    built-in range, but returns an ndarray rather than a range instance.
    When using a non-integer step, such as 0.1, it is often better to use
    numpy.linspace.

    Args:
        start: integer or real, optional.
               Start of interval. The interval includes this value.
               The default start value is 0.
        stop: integer or real.
              End of interval. The interval does not include this value,
              except in some cases where step is not an integer and floating
              point round-off affects the length of out.
        step: integer or real, optional.
              Spacing between values. For any output out, this is the distance
              between two adjacent values, out[i+1] - out[i].
              The default step size is 1.
              If step is specified as a position argument,start must also be given.

    Returns:
        arange: ndarray.
                    Array of evenly spaced values.
                    For floating point arguments, the length of the result is
                    ceil((stop - start)/step). Because of floating point overflow,
                    this rule may result in the last element of out being greater
                    than stop.

    Note:
        dependencies: numpy
        GUI: 'no'
    """
    def __init__(self, start=0.0, stop=5.0, step=1.0, **options):
        import numpy as np
        self.arange = np.arange(start, stop, step, **options)

    def arange(self: 'list_float'):
        return self.arange

##############################################################################
