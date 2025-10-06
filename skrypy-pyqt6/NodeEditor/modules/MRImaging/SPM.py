class spm_imcalc():
    def __init__(self, mat_eng='', Vi=['path'], Vo='path', f='', **options):
        import matlab.engine
        # list_opt_arg = ['dmtx', 'mask', 'interp', 'dtype']
        # list_opt_val = [0, 0, 0.0, 4]
        # for opk, opv in options.items():
        #     list_opt_val[list_opt_arg.index(opk)] = opv
        # opt_cell = mat_eng.cell(list_opt_val)
        self.Vo = mat_eng.spm_imcalc(Vi, Vo, f, options)
        self.mat_eng = mat_eng

    def mat_eng(self: 'str'):
        return self.mat_eng

    def Vo(self: 'dict'):
        return self.Vo

##################################################################


class spm_reslice():
    def __init__(self, mat_eng='', P=['path'], **options):
        import matlab.engine
        mat_eng.spm_reslice(P, options)
        self.mat_eng = mat_eng

    def mat_eng(self: 'str'):
        return self.mat_eng

##################################################################
