class skimage_active_contour():
    def __init__(self, image=[[0.0]], snake=[[0.0]], **options):
        from skimage.segmentation import active_contour
        self.a = active_contour(image, snake, **options)

    def act_contour(self: 'array_float'):
        return self.a

##############################################################################


class skimage_ball:
    def __init__(self, radius=1):
        from skimage.morphology import ball
        self.ball = ball(radius)

    def sk_ball(self: 'array_float'):
        return self.ball

##############################################################################


class skimage_Canny_Edge():
    def __init__(self, image=[[0.0]], **options):
        from skimage import feature
        import numpy as np
        self.img = np.array(image)
        dim = len(image.shape)
        if dim == 3:
            for sl1 in range(image.shape[2]):
                self.img[:, :, sl1] = feature.canny(self.img[:, :, sl1], **options)
        if dim == 4:
            for sl1 in range(image.shape[2]):
                for sl2 in range(image.shape[3]):
                    self.img[:, :, sl1, sl2] = feature.canny(self.img[:, :, sl1, sl2], **options)
        if dim == 5:
            for sl1 in range(image.shape[2]):
                for sl2 in range(image.shape[3]):
                    for sl3 in range(image.shape[4]):
                        self.img[:, :, sl1, sl2, sl3] = feature.canny(self.img[:, :, sl1, sl2, sl3], **options)

    def canny_edge(self: 'array_float'):
        return self.img

##############################################################################


class skimage_closing:
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import closing
        import numpy as np
        self.cl = closing(np.array(image), **options)

    def sk_closing(self: 'array_float'):
        return self.cl

##############################################################################


class skimage_convex_hull_image:
    """
    Return greyscale morphological dilation of an image.
    Morphological dilation sets a pixel at (i,j) to the
        maximum over all pixels in the neighborhood centered at (i,j).
    Dilation enlarges bright regions and shrinks dark regions.

    Args:
        image: (array) Binary input image. This array is cast to bool before processing..

    Returns:
        sk_convex: (M, N) array of bool
                    Binary image with pixels in convex hull set to True.

    Note:
        link_web: https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.convex_hull_image
        dependencies: skimage
        GUI: no
    """
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import convex_hull_image
        import numpy as np
        self.ch = convex_hull_image(image, **options)

    def sk_convex(self: 'array_bool'):
        return self.ch

##############################################################################


class skimage_remove_small_holes:
    def __init__(self, image=[[0.0]], **options):
        from skimage import morphology
        import numpy as np
        self.a = np.array(image, dtype=bool)
        for sl1 in range(self.a.shape[2]):
            self.a[:, :, sl1] = morphology.remove_small_holes(self.a[:, :, sl1], **options)

    def image_cln(self: 'array_int'):
        return self.a.astype(int)

##############################################################################


class skimage_remove_small_objects:
    def __init__(self, image=[[0.0]], **options):
        from skimage import morphology
        import numpy as np
        self.a = np.array(image, dtype=bool)
        for sl1 in range(self.a.shape[2]):
            self.a[:, :, sl1] = morphology.remove_small_objects(self.a[:, :, sl1], **options)

    def image_cln(self: 'array_int'):
        return self.a.astype(int)

##############################################################################


class skimage_erosion:
    """
    Return greyscale morphological erosion of an image.
    Morphological erosion sets a pixel at (i,j) to the
        minimum over all pixels in the neighborhood centered at (i,j).
    Erosion shrinks bright regions and enlarges dark regions.

    Args:
        image: (ndarray) Image array.

    Returns:
        sk_erosion: (array, same shape as image)
                    The result of the morphological erosion.

    Note:
        link_web: https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.erosion
        dependencies: skimage
        GUI: no
    """
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import erosion
        import numpy as np
        self.eroded = erosion(np.array(image), **options)

    def sk_erosion(self: 'array_float'):
        return self.eroded

##############################################################################


class skimage_dilation:
    """
    Return greyscale morphological dilation of an image.
    Morphological dilation sets a pixel at (i,j) to the
        maximum over all pixels in the neighborhood centered at (i,j).
    Dilation enlarges bright regions and shrinks dark regions.

    Args:
        image: (ndarray) Image array.

    Returns:
        sk_dilation: (uint8 array, same shape and type as image)
                        The result of the morphological dilation.

    Note:
        link_web: https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.dilation
        dependencies: skimage
        GUI: no
    """
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import dilation
        import numpy as np
        self.dilated = dilation(np.array(image), **options)

    def sk_dilation(self: 'array_float'):
        return self.dilated

##############################################################################


class skimage_white_tophat:
    """
    Return white top hat of an image.
    The white top hat of an image is defined as
        the image minus its morphological opening.
    This operation returns the bright spots of the image
        that are smaller than the structuring element.

    Args:
        image: (ndarray) Image array.

    Returns:
        sk_white_tophat: (array, same) shape and type as image.
                        The result of the morphological white top hat.

    Note:
        link_web: https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.white_tophat
        dependencies: skimage
        GUI: no
    """
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import white_tophat
        import numpy as np
        self.wt = white_tophat(np.array(image), **options)

    def sk_white_tophat(self: 'array_float'):
        return self.wt

##############################################################################


class skimage_black_tophat:
    """
    Return black top hat of an image.
    The black top hat of an image is defined as
        its morphological closing minus the original image.
    This operation returns the dark spots of the image
        that are smaller than the structuring element.
    Note that dark spots in the original image are bright spots after
        the black top hat.

    Args:
        image: (ndarray) Image array.

    Returns:
        sk_black_tophat: (array, same shape and type as image)
                            The result of the morphological black top hat.

    Note:
        link_web: https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.black_tophat
        dependencies: skimage
        GUI: no
    """
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import black_tophat
        import numpy as np
        self.bt = black_tophat(np.array(image), **options)

    def sk_black_tophat(self: 'array_float'):
        return self.bt

##############################################################################


class skimage_opening:
    def __init__(self, image=[[0.0]], **options):
        from skimage.morphology import opening
        import numpy as np
        self.op = opening(np.array(image), **options)

    def sk_opening(self: 'array_float'):
        return self.op

##############################################################################


class skimage_threshold_multiotsu:
    def __init__(self, image=[[0.0]], **options):
        from skimage.filters import threshold_multiotsu
        self.thresholds = threshold_multiotsu(image)

    def multi_otsu(self: 'list_float'):
        return self.thresholds

##############################################################################


class skimage_resize():
    def __init__(self, image=[[0.0]], output_shape=(128, 128, 64), **options):
        from skimage import transform
        self.a = transform.resize(image, output_shape, **options)

    def image_resize(self: 'array_float'):
        return self.a

##############################################################################


# class skimage_Canny_Edge():
#     def __init__(self, image=[[0.0]], **options):
#         from skimage import feature
#         self.a = feature.canny(image, **options)
#
#     def canny_edge(self: 'array_float'):
#         return self.a
