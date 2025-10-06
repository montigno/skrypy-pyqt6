class numpy_fft_1d():
    '''
    Compute the one-dimensional discrete Fourier Transform.
    This function computes the one-dimensional n-point discrete
    Fourier Transform (DFT) with the efficient
    Fast Fourier Transform (FFT) algorithm [CT].

    Args:
        data: array_like
              Input array, can be complex.

    Returns:
        fft_1d: complex ndarray
                The truncated or zero-padded input, transformed along
                the axis indicated by axis, or the last one if axis is
                not specified.

    Note:
        GUI: no
        dependencies: Numpy
        link_web:  https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
                    (click Ctrl + U)
    '''
    def __init__(self, data=[0.0], **options):
        import numpy as np
        self.out = np.fft.fft(data, **options)

    def fft_1d(self: 'list_float'):
        return self.out

###############################################################################


class numpy_ifft_1d():
    '''
    Compute the one-dimensional inverse discrete Fourier Transform.
    This function computes the inverse of the one-dimensional n-point discrete
    Fourier transform computed by fft. In other words, ifft(fft(a)) == a
    to within numerical accuracy.
    For a general description of the algorithm and definitions, see numpy.fft.
    The input should be ordered in the same way as is returned by fft, i.e.,
    a[0] should contain the zero frequency term,
    a[1:n//2] should contain the positive-frequency terms,
    a[n//2 + 1:] should contain the negative-frequency terms, in increasing order
    starting from the most negative frequency.

    For an even number of input points, A[n//2] represents the sum of the values
    at the positive and negative Nyquist frequencies, as the two are aliased together.
    See numpy.fft for details.

    Args:
        data: array_like
              Input array, can be complex.

    Returns:
        ifft_1d: complex ndarray
                 The truncated or zero-padded input, transformed along
                 the axis indicated by axis, or the last one if axis is
                 not specified.

    Note:
        GUI: no
        dependencies: Numpy
        link_web:  https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html
                    (click Ctrl + U)
    '''
    def __init__(self, data=[0.0], **options):
        import numpy as np
        self.out = np.fft.ifft(data, **options)

    def ifft_1d(self: 'list_float'):
        return self.out

###############################################################################


class numpy_fft_freq():
    def __init__(self, n=0, d=1.0):
        import numpy as np
        self.out = np.fft.fftfreq(n, d)

    def fft_freq(self: 'list_float'):
        return self.out

###############################################################################


class numpy_fft_shift():
    def __init__(self, array_like=[[0.0]]):
        import numpy as np
        self.out = np.fft.fftshift(array_like)

    def fft_shift(self: 'array_float'):
        return self.out
