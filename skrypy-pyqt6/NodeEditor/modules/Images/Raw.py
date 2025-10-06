class raw_display:
    """
    visualize the raw image

    Args:
        image: (array of float)
        title: (string) title of the window

    Returns:

    Note:
        dependencies: Numpy, Nibabel
        GUI: yes
    """
    def __init__(self, image=[[0.0]], title=''):
        import os
        import sys
        import subprocess
        import nibabel as nib
        import numpy as np
        from datetime import datetime
        image = np.array(image)
        img = nib.Nifti1Image(image, np.eye(4))
        name_file = '/tmp/tmpNifti{}.nii'.format(datetime.now())
        n_header = img.header
        n_header['xyzt_units'] = 10
        nib.save(img, name_file)
        current_dir_path = os.path.abspath(os.path.join(__file__, "../../.."))
        source_disp = os.path.join(current_dir_path, 'api', 'dispNifti.py')
        p = subprocess.Popen([sys.executable, source_disp, name_file, title, 'yes'],
                             shell=False,
                             stdin=None,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

##############################################################################


class raw_open_image():
    def __init__(self,
                 raw_file='path',
                 imageSize=(128, 128, 9),
                 byteorder="enumerate(('little-endian', 'big-endian'))",
                 data_type="enumerate(('int8', 'int16', 'int32', 'uint8', 'uint16', 'uint32', 'float16', 'float32'))"):
        import numpy as np
        if 'little' in byteorder:
            typeImg = '<'
        else:
            typeImg = '>'
        if 'uint' in data_type:
            typeImg += 'u'
            typeImg += str(int(int(data_type[4:]) / 8))
        elif 'int' in data_type:
            typeImg += 'i'
            typeImg += str(int(int(data_type[3:]) / 8))
        else:
            typeImg += 'f'
            typeImg += str(int(int(data_type[5:]) / 8))

        self.npimg = np.fromfile(raw_file, dtype=typeImg)
        # self.npimg = self.npimg.reshape(tuple(reversed(imageSize)))
        self.npimg = self.npimg.reshape(imageSize, order='F')

    def raw_image(self: 'array_float'):
        return self.npimg
