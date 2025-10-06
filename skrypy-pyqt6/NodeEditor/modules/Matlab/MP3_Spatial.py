class MP3_Brain_Mask_PCNN3D():
    def __init__(self,
                 mat_eng='',
                 file_in='path',
                 file_out='path',
                 **options):
        import matlab.engine
        files_in, files_out = {}, {}
        options['flag_test'] = 0
        files_in['In1'] = [file_in]
        files_out['In1'] = [file_out]
        mat_eng.Module_Brain_Mask_PCNN3D(files_in, files_out, options)
        self.mat_eng = mat_eng
        self.map = file_out

    def mat_eng(self: 'str'):
        return self.mat_eng

    def file_out(self: 'path'):
        return self.map

##############################################################################


class MP3_Arithmetic():
    def __init__(self,
                 mat_eng='',
                 img1='path',
                 img2='path',
                 file_out='path',
                 **options):
        import matlab.engine
        files_in, files_out = {}, {}
        options['flag_test'] = 0
        options['Table_in'] = {'Type': 'ROI'}
        files_in['In1'] = [img1]
        files_in['In2'] = [img2]
        files_out['In1'] = [file_out]
        mat_eng.Module_Arithmetic(files_in, files_out, options)
        self.mat_eng = mat_eng
        self.map = file_out

    def mat_eng(self: 'str'):
        return self.mat_eng

    def file_out(self: 'path'):
        return self.map

##############################################################################


class MP3_Reshape():
    def __init__(self,
                 mat_eng='',
                 img='path',
                 file_out='path',
                 **options):
        import matlab.engine
        files_in, files_out = {}, {}
        options['flag_test'] = 0
        # options['Table_in'] = {'Type': 'ROI'}
        files_in['In1'] = [img]
        files_out['In1'] = [file_out]
        mat_eng.Module_Reshape(files_in, files_out, options)
        self.mat_eng = mat_eng
        self.map = file_out

    def mat_eng(self: 'str'):
        return self.mat_eng

    def file_out(self: 'path'):
        return self.map

##############################################################################


class MP3_MICO_BIAS_Estimation():
    def __init__(self,
                 mat_eng='',
                 img='path',
                 file_out='path',
                 folder_out='path',
                 **options):
        import matlab.engine
        from NodeEditor.modules.Tools.Path import path_add_suffixprefix
        files_in, files_out = {}, {}
        options['flag_test'] = 0
        options['folder_out'] = folder_out
        files_in['In1'] = [img]
        files_out['In1'] = [path_add_suffixprefix(file_out, '_BiasField', 'suffix').newPath()]
        files_out['In2'] = [path_add_suffixprefix(file_out, '_bc', 'suffix').newPath()]
        files_out['In3'] = [path_add_suffixprefix(file_out, '_Seg', 'suffix').newPath()]
        mat_eng.Module_MICO_BIAS_Estimation(files_in, files_out, options)
        self.mat_eng = mat_eng
        self.map = files_out['In2'][0]

    def mat_eng(self: 'str'):
        return self.mat_eng

    def file_out(self: 'path'):
        return self.map
