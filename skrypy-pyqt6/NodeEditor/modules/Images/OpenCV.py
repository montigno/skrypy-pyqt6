class openCV_fastNlMeansDenoising():
    def __init__(self, src=[[0.0]], dst='path', h=3, templateWindowSize=7, searchWindowSize=21):
        import cv2 as cv
        import os

        if dst == 'path':
            dst = None
        self.dst = cv.fastNlMeansDenoising(src, dst, h, templateWindowSize, searchWindowSize)

    def out_NLM(self: 'array_float'):
        return self.dst

##############################################################################


class openCV_imread():
    """
    Loads an image from a file.
    The function imread loads an image from the specified file and returns it.
    If the image cannot be read (because of missing file, improper permissions,
    unsupported or invalid format), the function returns an empty matrix
    ( Mat::data==NULL ).
    Currently, the following file formats are supported:
        Windows bitmaps - *.bmp, *.dib (always supported)
        JPEG files - *.jpeg, *.jpg, *.jpe (see the Note section)
        JPEG 2000 files - *.jp2 (see the Note section)
        Portable Network Graphics - *.png (see the Note section)
        WebP - *.webp (see the Note section)
        Portable image format - *.pbm, *.pgm, *.ppm *.pxm, *.pnm (always supported)
        Sun rasters - *.sr, *.ras (always supported)
        TIFF files - *.tiff, *.tif (see the Note section)
        OpenEXR Image files - *.exr (see the Note section)
        Radiance HDR - *.hdr, *.pic (always supported)
        Raster and Vector geospatial data supported by GDAL (see the Note section)

    Args:
        filename: Name of file to be loaded.

    Return:
        img_read: Image from the specified filename

    Note:
        dependencies: OpenCV
        GUI: no
        link_web: https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56
                                (click Ctrl + U)
    """
    def __init__(self, filename='path', **options):
        import cv2

        flags = 0  # grayscale by default
        if options:
            flags = getattr(cv2, options['flags'])
        self.out_img = cv2.imread(filename, flags)

    def img_read(self: 'array_float'):
        return self.out_img
