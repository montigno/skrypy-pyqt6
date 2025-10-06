class MP3_DCE_phenomeno():
    def __init__(self,
                 mat_eng='',
                 file_in='path',
                 file_out='path',
                 **options):
        import matlab.engine
        from NodeEditor.modules.Tools.Path import path_add_suffixprefix
        files_in, files_out = {}, {}
        options['flag_test'] = 0
        files_in['In1'] = [file_in]
        files_out['In1'] = [path_add_suffixprefix(file_out, options['output_filename_AUC'], 'suffix').newPath(),
                            path_add_suffixprefix(file_out, options['output_filename_Max'], 'suffix').newPath(),
                            path_add_suffixprefix(file_out, options['output_filename_pc_enhanc'], 'suffix').newPath(),
                            path_add_suffixprefix(file_out, options['output_filename_TTP'], 'suffix').newPath()]
        mat_eng.Module_DCE_phenomeno(files_in, files_out, options)
        self.mat_eng = mat_eng
        self.map = files_out

    def mat_eng(self: 'str'):
        return self.mat_eng

    def file_out(self: 'list_path'):
        return self.map
