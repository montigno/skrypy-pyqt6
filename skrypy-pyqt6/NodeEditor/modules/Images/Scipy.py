class scipy_binary_opening:
    def __init__(self, image=[[0]], **options):
        from scipy import ndimage
        import numpy as np
        self.img_op = ndimage.binary_opening(np.array(image), **options)

    def image_opening(self: 'array_float'):
        return self.img_op

###############################################################################


class scipy_binary_closing:
    def __init__(self, image=[[0]], **options):
        from scipy import ndimage
        import numpy as np
        self.img_cl = ndimage.binary_closing(np.array(image), **options)

    def image_closing(self: 'array_float'):
        return self.img_cl

###############################################################################


class scipy_binary_propagation:
    def __init__(self, image=[[0]], **options):
        from scipy import ndimage
        import numpy as np
        self.img_pr = ndimage.binary_propagation(np.array(image), **options)

    def image_propagation(self: 'array_float'):
        return self.img_pr

###############################################################################


class scipy_binary_fill_holes:
    def __init__(self, image=[[0]], **options):
        from scipy import ndimage
        import numpy as np
        self.img_fh = ndimage.binary_fill_holes(np.array(image), **options)

    def image_holes_filled(self: 'array_float'):
        return self.img_fh

##############################################################################


class scipy_convolve2d():
    def __init__(self, image=[[0.0]], kern=[[0.0]], **options):
        from scipy import signal
        import numpy as np
        img = np.array(image)
        dim = len(image.shape)
        if dim == 3:
            tmp = signal.convolve2d(img[:, :, 0], kern, **options)
            self.img = np.zeros((tmp.shape[0], tmp.shape[1], image.shape[2]))
            for sl1 in range(image.shape[2]):
                self.img[:, :, sl1] = signal.convolve2d(img[:, :, sl1], kern, **options)
        if dim == 4:
            tmp = signal.convolve2d(img[:, :, 0, 0], kern, **options)
            self.img = np.zeros((tmp.shape[0], tmp.shape[1], image.shape[2], image.shape[3]))
            for sl1 in range(image.shape[2]):
                for sl2 in range(image.shape[3]):
                    self.img[:, :, sl1, sl2] = signal.convolve2d(img[:, :, sl1, sl2], kern, **options)
        if dim == 5:
            tmp = signal.convolve2d(img[:, :, 0, 0, 0], kern, **options)
            self.img = np.zeros((tmp.shape[0], tmp.shape[1], image.shape[2], image.shape[3], image.shape[4]))
            for sl1 in range(image.shape[2]):
                for sl2 in range(image.shape[3]):
                    for sl3 in range(image.shape[4]):
                        self.img[:, :, sl1, sl2, sl3] = signal.convolve2d(img[:, :, sl1, sl2, sl3], kern, **options)

    def Convol2d(self: 'array_float'):
        return self.img

##############################################################################


class scipy_convolve3d():
    def __init__(self, image=[[0.0]], kern=[[0.0]]):
        import numpy as np
        from scipy import ndimage
        img = np.array(image)
        k1 = np.array(kern).flatten()  # the kernel along the 1nd dimension
        k2 = k1  # the kernel along the 2nd dimension
        k3 = k1  # the kernel along the 3nd dimension

        # Convolve over all three axes in a for loop
        out = img.copy()
        for i, k in enumerate((k1, k2, k3)):
            out = ndimage.convolve1d(out, k, axis=i)

        self.img = out

    def Convol3d(self: 'array_float'):
        return self.img

##############################################################################


class scipy_fft():
    def __init__(self, x=[0.0]):
        from scipy import fft
        self.y = fft(x)

    def fft(self: 'list_float'):
        return self.y

##############################################################################


class scipy_filter_Sobel():
    def __init__(self, image=[[0.0]], **options):
        from scipy import ndimage
        self.ax = ndimage.sobel(image, **options)

    def Sobel(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_filter_Prewitt():
    def __init__(self, image=[[0.0]], **options):
        from scipy import ndimage
        self.ax = ndimage.prewitt(image, **options)

    def Prewitt(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_filter_Median():
    def __init__(self, image=[[0.0]], size=1, **options):
        from scipy import ndimage
        self.ax = ndimage.median_filter(image, size, **options)

    def Median(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_filter_Laplace():
    def __init__(self, image=[[0.0]], **options):
        from scipy import ndimage
        self.ax = ndimage.laplace(image, **options)

    def Laplace(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_filter_Gaussian():
    def __init__(self, image=[[0.0]], sigma=1, **options):
        from scipy import ndimage
        self.ax = ndimage.gaussian_filter(image, sigma=sigma, **options)

    def Gaussian(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_filter_Gaussian_laplace():
    def __init__(self, image=[[0.0]], sigma=1, **options):
        from scipy import ndimage
        self.ax = ndimage.gaussian_laplace(image, sigma=sigma, **options)

    def Gaussian(self: 'array_float'):
        return self.ax

##############################################################################


class scipy_rotate():
    def __init__(self, image=[[0.0]], angle=0):
        from scipy import ndimage
        self.rot_img = ndimage.rotate(image, angle)

    def rotate_img(self: 'array_float'):
        return self.rot_img
