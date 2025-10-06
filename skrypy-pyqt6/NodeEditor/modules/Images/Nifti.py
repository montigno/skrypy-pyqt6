class nifti_display:
    def __init__(self, image='path', title=''):
        import os
        import sys
        import subprocess
        current_dir_path = os.path.abspath(os.path.join(__file__, "../../.."))
        source_disp = os.path.join(current_dir_path, r'api', r'dispNifti.py')
        p = subprocess.Popen([sys.executable, source_disp, image, title, 'no'],
                             shell=False,
                             stdin=None,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

##############################################################################


class nifti_get_header():

    def __init__(self, nii_image='path'):
        import nibabel as nib
        img = nib.load(nii_image)
        self.hdr = img.header

    def nii_hdr(self: 'str'):
        return self.hdr

    def nii_hdr_dict(self: 'dict'):
        return dict(self.hdr)

##############################################################################


class nifti_change_header():

    def __init__(self,
                 nifti_file='path',
                 structarr="enumerate(('sizeof_hdr',\
                                       'data_type',\
                                       'db_name',\
                                       'extents',\
                                       'session_error',\
                                       'regular',\
                                       'dim_info',\
                                       'dim',\
                                       'intent_p1',\
                                       'intent_p2',\
                                       'intent_p3',\
                                       'intent_code',\
                                       'datatype',\
                                       'bitpix',\
                                       'slice_start',\
                                       'pixdim',\
                                       'vox_offset',\
                                       'scl_slope',\
                                       'scl_inter',\
                                       'slice_end',\
                                       'slice_code',\
                                       'xyzt_units',\
                                       'cal_max',\
                                       'cal_min',\
                                       'slice_duration',\
                                       'toffset',\
                                       'glmax',\
                                       'glmin',\
                                       'descrip',\
                                       'aux_file',\
                                       'qform_code',\
                                       'sform_code',\
                                       'quatern_b',\
                                       'quatern_c',\
                                       'quatern_d',\
                                       'qoffset_x',\
                                       'qoffset_y',\
                                       'qoffset_z',\
                                       'srow_x',\
                                       'srow_y',\
                                       'srow_z',\
                                       'intent_name',\
                                       'magic'))",
                 new_value='',
                 outfile='path'):
        import nibabel as nib
        import os
        img = nib.load(nifti_file)
        hdr = img.header.copy()
        hdr[structarr] = new_value
        new_nifti = nib.Nifti1Image(img.get_fdata().copy(), None, header=hdr)
        nib.save(new_nifti, outfile)
        self.outf = outfile

    def outfile(self: 'path'):
        return self.outf

##############################################################################


class nifti_open_file:
    def __init__(self, nifti_file='path'):
        import os.path
        import nibabel as nib
        import numpy as np
        self.dim = 0
        self.img = [[0.0]]
        if (os.path.splitext(nifti_file)[1] == '.nii') or \
           ('.nii.gz' in nifti_file):
            img = nib.load(nifti_file)
            # self.img = img.get_fdata()
            self.img = np.asarray(img.dataobj)
            self.dim = len(img.shape)
            self.pxd = img.header._structarr['pixdim']
        else:
            print('no Nifti file')

    def image(self: 'array_float'):
        return self.img

    def dim(self: 'int'):
        return self.dim

    def pixdim(self: 'list_float'):
        return self.pxd

##############################################################################


class nifti_save_file:
    def __init__(self, image=[[0.0]], nifti_path='path', **options):
        import nibabel as nib
        import numpy as np
        import os

        fn, extn = os.path.splitext(nifti_path)
        if 'out_type' in options.keys():
            extn = options['out_type']
        else:
            if extn not in ['.nii', '.gz']:
                extn = '.nii'
        self.fileSaved = '{}{}'.format(fn, '.nii')
        image = np.array(image, dtype=float)
        if 'header' in options.keys():
            hdr = options['header']
            if not hdr:
                hdr = np.eye(4)
                img = nib.Nifti1Image(image, hdr)
            else:
                img = nib.Nifti1Image(image, None, hdr)
        else:
            hdr = np.eye(4)
            img = nib.Nifti1Image(image, hdr)
        if 'print_header' in options.keys():
            print(hdr)
        nib.save(img, self.fileSaved)

    def pathFile(self: 'path'):
        return self.fileSaved

##############################################################################


class nifti_get_slope_inter():
    def __init__(self, nifti_file='path'):
        import nibabel as nib
        import os
        img = nib.load(nifti_file)
        hdr = img.header.copy()
        self.slope_inter = hdr.get_slope_inter()

    def slope_inter(self: 'tuple'):
        return self.slope_inter

##############################################################################


class nifti_set_slope_inter():
    def __init__(self, nifti_file='path', slope=1.0, intercept=0.0, outfile='path'):
        import nibabel as nib
        import os
        img = nib.load(nifti_file)
        hdr = img.header.copy()
        data_img = img.get_fdata().copy()
        hdr.set_slope_inter(slope, intercept)
        new_nifti = nib.Nifti1Image(data_img, img.affine, header=hdr)
        nib.save(new_nifti, outfile)
        self.outf = outfile

    def outfile(self: 'path'):
        return self.outf

##############################################################################


class nifti_get_cal_max_min():
    def __init__(self, nifti_file='path'):
        import nibabel as nib
        import os
        img = nib.load(nifti_file)
        hdr = img.header.copy()
        self.cal_max_min = (hdr['cal_max'], hdr['cal_min'])

    def slope_inter(self: 'tuple'):
        return self.cal_max_min

##############################################################################


class nifti_set_cal_max_min():
    def __init__(self, nifti_file='path', cal_max=100.0, cal_min=0.0, outfile='path'):
        import nibabel as nib
        import os
        img = nib.load(nifti_file)
        hdr = img.header.copy()
        data_img = img.get_fdata().copy()
        hdr['cal_max'], hdr['cal_min'] = cal_max, cal_min
        new_nifti = nib.Nifti1Image(data_img, img.affine, header=hdr)
        nib.save(new_nifti, outfile)
        self.outf = outfile

    def outfile(self: 'path'):
        return self.outf

##############################################################################


class nifti_binarize_threshold():
    def __init__(self,
                 image='path',
                 threshold=1.0,
                 val_below=0.0,
                 val_equal_above=1.0,
                 output_file='path'):
        import nibabel
        import os
        self.outFile = output_file
        localizer_img = nibabel.load(image)
        localizer = localizer_img.get_fdata()
        localizer[localizer >= threshold] = val_equal_above
        localizer[localizer < threshold] = val_below
        locmask = nibabel.Nifti1Image(localizer, localizer_img.affine)
        nibabel.save(locmask, output_file)

    def outfile(self: 'path'):
        return self.outFile

##############################################################################


class nifti_four_to_three:
    def __init__(self, image_nii_4D='path', out_directory='path'):
        import nibabel as nib
        import os
        imgs = nib.four_to_three(nib.load(image_nii_4D))
        tmp = os.path.basename(image_nii_4D)
        froot = ('.').join(tmp.split('.')[:-1])
        self.listimg = []
        for i, img3d in enumerate(imgs):
            fname3d = '%s_%04d.nii' % (froot, i)
            nib.save(img3d, os.path.join(out_directory, fname3d))
            self.listimg.append(os.path.join(out_directory, fname3d))

    def list_3D_images(self: 'list_path'):
        return self.listimg

##############################################################################


class Nifti_rawInfo():

    def __init__(self,
                 nii_image='path',
                 structarr="enumerate(('sizeof_hdr', 'data_type', 'db_name', 'extents',\
                                       'session_error', 'regular', 'dim_info', 'dim',\
                                       'intent_p1', 'intent_p2', 'intent_p3', 'intent_code',\
                                       'datatype', 'bitpix', 'slice_start', 'pixdim',\
                                       'vox_offset', 'scl_slope', 'scl_inter', 'slice_end',\
                                       'slice_code', 'xyzt_units', 'cal_max', 'cal_min',\
                                       'slice_duration', 'toffset', 'glmax', 'glmin',\
                                       'descrip', 'aux_file', 'qform_code', 'sform_code',\
                                       'quatern_b', 'quatern_c', 'quatern_d',\
                                       'qoffset_x', 'qoffset_y', 'qoffset_z',\
                                       'srow_x', 'srow_y', 'srow_z',\
                                       'intent_name', 'magic'))"):
        import nibabel as nib
        img = nib.load(nii_image)
        hdr = img.header
        self.str = hdr.structarr[structarr].tolist()

    def out_structarr(self: 'list_str'):
        return self.str
