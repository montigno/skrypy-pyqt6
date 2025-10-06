class mrtrix3_deGibbs3D:
    def __init__(self, inImg='path', outImg='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(inImg)
        list_options.append(outImg)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['deGibbs3D']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.deG3D = outImg

    def deGibbs3D(self: 'path'):
        return self.deG3D

###############################################################################


class mrtrix3_dwi2fod:
    def __init__(self,
                 algorithm="enumerate(('csd', \
                                       'msmt_csd'))",
                 dwi='path',
                 response='path',
                 odf='path',
                 **options):
        from subprocess import run
        list_options = []
        list_options.append(algorithm)
        list_options.append(dwi)
        list_options.append(response)
        list_options.append(odf)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['dwi2fod']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwi2f = odf

    def dwi2fod(self: 'path'):
        return self.dwi2f

###############################################################################


class mrtrix3_dwi2mask:
    def __init__(self, mif_image='path', dwi2mask_out='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(mif_image)
        list_options.append(dwi2mask_out)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['dwi2mask']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwi2m = dwi2mask_out

    def dwi2mask(self: 'path'):
        return self.dwi2m

###############################################################################


class mrtrix3_dwi2response:
    def __init__(self,
                 algorithm="enumerate(('dhollander', \
                                             'fa', \
                                             'manual', \
                                             'msmt_5tt', \
                                             'tax', \
                                             'tournier'))",
                 inputs=['path'],
                 outputs=['path'],
                 **options):
        from subprocess import run
        list_options = []
        list_options.append(algorithm)
        for ls in inputs:
            if ls == 'path' or ls == '':
                inputs = ''
            else:
                list_options.append(ls)
        for ls in outputs:
            if ls == 'path' or ls == '':
                outputs = ''
            else:
                list_options.append(ls)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['dwi2response']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwi2r = outputs

    def dwi2response(self: 'list_path'):
        return self.dwi2r

###############################################################################


class mrtrix3_dwi2tensor:
    def __init__(self, dwi2tensor_out='path', **options):
        from subprocess import run
        list_options = []
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                if type(options[op]).__name__ == 'list':
                    for tp in options[op]:
                        list_options.append(tp)
                else:
                    list_options.append(str(options[op]))
        command = ['dwi2tensor']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwi2t = dwi2tensor_out

    def dwi2tensor(self: 'path'):
        return self.dwi2t

###############################################################################


class mrtrix3_dwi2tensor2:
    def __init__(self, dwi_input='path', dwi2tensor_out='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(dwi_input)
        list_options.append(dwi2tensor_out)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                if type(options[op]).__name__ == 'list':
                    for tp in options[op]:
                        list_options.append(tp)
                else:
                    list_options.append(str(options[op]))
        command = ['dwi2tensor']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwi2t = dwi2tensor_out

    def dwi2tensor(self: 'path'):
        return self.dwi2t

###############################################################################


class mrtrix3_dwidenoise:
    def __init__(self, mif_image='path', dwi_out='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(mif_image)
        list_options.append(dwi_out)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['dwidenoise']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.dwiden = dwi_out

    def dwidenoise(self: 'path'):
        return self.dwiden

###############################################################################


class mrtrix3_lmax:
    def __init__(self, number_DWI_volumes=6):
        self.lmax = 2
        if number_DWI_volumes <= 14:
            self.lmax = 2
        elif number_DWI_volumes <= 27:
            self.lmax = 4
        elif number_DWI_volumes <= 44:
            self.lmax = 6
        elif number_DWI_volumes <= 65:
            self.lmax = 8
        elif number_DWI_volumes <= 90:
            self.lmax = 10
        elif number_DWI_volumes > 91:
            self.lmax = 12

    def lmax(self: 'int'):
        return sel.lmax

###############################################################################


class mrtrix3_mrcalc:
    def __init__(self, mif_images=['path'], mrcalc_out=['path'], **options):
        from subprocess import run
        list_options = []
        for ls in mif_images:
            list_options.append(ls)
        for ls in mrcalc_out:
            if ls == 'path' or ls == '':
                mrcalc_out = ''
            else:
                list_options.append(ls)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mrcalc']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.mrc = mrcalc_out

    def mrcalc(self: 'path'):
        return self.mrc

###############################################################################


class mrtrix3_mrconvert:
    def __init__(self, input='path', output='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(input)
        list_options.append(output)
        for op in options:
            list_options.append('-' + op)
            if op == 'coord':
                list_options.extend(options[op].split())
            elif op == 'fslgrad':
                list_options.extend(options[op])
            else:
                if options[op]:
                    list_options.append(str(options[op]))

        command = ["mrconvert"]
        command.extend(list_options)
        print('MrTrix3 command : ', command)
        result = run(command, shell=False, check=True)
        self.outfile = output

    def output_file(self: 'path'):
        return self.outfile

###############################################################################


class mrtrix3_mrdegibbs:
    def __init__(self, mif_image='path', mrdegibbs_out='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(mif_image)
        list_options.append(mrdegibbs_out)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mrdegibbs']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.mrdeg = mrdegibbs_out

    def mrdegibbs(self: 'path'):
        return self.mrdeg

###############################################################################


class mrtrix3_mrinfo:
    def __init__(self, mif_images=['path'], **options):
        from subprocess import Popen
        list_options = []
        list_options.extend(mif_images)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mrinfo']
        command.extend(list_options)
        proc = Popen(command)

###############################################################################


class mrtrix3_mrview:
    def __init__(self, list_images=['path'], **options):
        from subprocess import Popen
        list_options = []
        list_options.extend(list_images)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mrview']
        command.extend(list_options)
        proc = Popen(command)

###############################################################################


class mrtrix3_mtnormalise:
    def __init__(self, inputs=['path'], outputs=['path'], **options):
        from subprocess import run
        list_options = []
        for ls in inputs:
            if ls == 'path' or ls == '':
                inputs = ''
            else:
                list_options.append(ls)
        for ls in outputs:
            if ls == 'path' or ls == '':
                outputs = ''
            else:
                list_options.append(ls)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mtnormalise']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.mtn = outputs

    def mrcalc(self: 'list_path'):
        return self.mtn

###############################################################################


class mrtrix3_mrtransform:
    def __init__(self, input='path', output='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(input)
        list_options.append(output)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['mrtransform']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.mrtra = output

    def mrtransform(self: 'path'):
        return self.mrtra

###############################################################################


class mrtrix3_tckgen:
    def __init__(self, source='path', tracks='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(mif_image)
        for op in options:
            list_options.append(str(options[op]))
        command = ['tckgen']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.tracks = tracks

    def outfile_tracks(self: 'path'):
        return self.tracks

###############################################################################


class mrtrix3_tensor2metric:
    def __init__(self, mif_image='path', tensor2metric_out='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(mif_image)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['tensor2metric']
        command.extend(list_options)
        result = run(command, shell=False, check=True)
        self.tens = tensor2metric_out

    def tensor2metric(self: 'path'):
        return self.tens

###############################################################################


class mrtrix3_tensor2metric2:
    def __init__(self, tensor='path', **options):
        from subprocess import run
        list_options = []
        list_options.append(tensor)
        for op in options:
            if options[op]:
                list_options.append('-' + op)
                list_options.append(str(options[op]))
        command = ['tensor2metric']
        command.extend(list_options)
        result = run(command, shell=False, check=True)

###############################################################################
