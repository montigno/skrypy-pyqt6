class open_tif_file:
    def __init__(self, file_tiff='path'):
        from PIL import Image
        import numpy as np
        img = Image.open(file_tiff)
        nb = img.n_frames
        self.imarray = []
        for i in range(nb):
            img.seek(i)
            self.imarray.append(np.array(img))
        self.imarray = np.array(self.imarray)
        self.imarray = self.imarray.transpose(2, 1, 0)

    def out_tiff(self) -> list[list[float]]:
        return self.imarray

###############################################################################


class tif_to_nii:
    def __init__(self, Tif_file='path', output_nii='path', pixdim=[0.025, 0.025, 0.05]):
        import numpy as np
        import tifffile as tiff
        import nibabel as nib

        data = tiff.imread(Tif_file)

        assert data.ndim == 3, "TIFF must be 3D"

        data = np.transpose(data, (2, 1, 0))

        # --- Affine NIfTI ---
        affine = np.array([
            [pixdim[0], 0, 0, 0],
            [0, pixdim[1], 0, 0],
            [0, 0, pixdim[2], 0],
            [0, 0, 0, 1]
        ])

        nii = nib.Nifti1Image(data, affine)

        nii.set_qform(affine, code=1)
        nii.set_sform(affine, code=1)

        nib.save(nii, output_nii)
        self.out_nii = output_nii

    def output_nii(self) -> None:
        return self.out_nii

###############################################################################


class tif_to_nii_4d:
    def __init__(self, Tif_file='path', output_nii='path', pixdim=[0.025, 0.025, 0.05, 1.0]):
        import numpy as np
        import tifffile as tiff
        import nibabel as nib

        data = tiff.imread(Tif_file)
        assert data.ndim == 4, "TIFF must be 4D"

        # example : (T, Z, Y, X) -> (X, Y, Z, T)
        data = np.transpose(data, (3, 2, 1, 0))

        # --- Affine NIfTI (spatial only) ---
        affine = np.array([[pixdim[0], 0, 0, 0],
                           [0, pixdim[1], 0, 0],
                           [0, 0, pixdim[2], 0],
                           [0, 0, 0, 1]
                           ])
        nii = nib.Nifti1Image(data, affine)

        # définir pixdim
        nii.header.set_zooms(tuple(pixdim))
        # qform / sform
        nii.set_qform(affine, code=1)
        nii.set_sform(affine, code=1)

        nib.save(nii, output_nii)
        self.out_nii = output_nii

    def output_nii(self) -> None:
        return self.out_nii
