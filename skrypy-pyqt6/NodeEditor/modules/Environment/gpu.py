class gpu_available():
    def __init__(self):
        from numba import cuda
        if cuda.is_available():
            self.gpu_av = True
        else:
            self.gpu_av = False

    def gpu_available(self: 'bool'):
        return self.gpu_av
