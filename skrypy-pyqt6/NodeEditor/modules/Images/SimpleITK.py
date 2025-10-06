class simpleITK_readImage:
    def __init__(self, inputImageFileName='path', **options):
        import SimpleITK as sitk
        self.image = sitk.ReadImage(inputImageFileName, **options)

    def read_image(self: 'array_float'):
        return self.image

##############################################################################


class simpleITK_writeImage:
    def __init__(self, image=[[0.0]], outputImageFileName='path'):
        import SimpleITK as sitk
        self.image = sitk.WriteImage(image, outputImageFileName)
        self.out_image_path = outputImageFileName

    def out_image_path(self: 'path'):
        return self.out_image_path

##############################################################################


class SimpleITK_ReadTransform:
    def __init__(self, file_in='path'):
        import SimpleITK as sitk
        self.read_transform = sitk.ReadTransform(file_in)

    def read_transform(self: 'array_float'):
        return self.read_transform

##############################################################################


class SimpleITK_WriteTransform:
    def __init__(self, basic_transform=[[0.0]], file_out_path='path'):
        import SimpleITK as sitk
        sitk.WriteTransform(basic_transform, file_out_path)
        self.out_file = file_out_path

    def file_transform(self: 'path'):
        return self.out_file
