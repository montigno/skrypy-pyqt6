class Bru2Nii:
    def __init__(self, input_dir='path', **options):
        from nipype.interfaces.bru2nii import Bru2
        converter = Bru2()
        converter.inputs.input_dir = input_dir
#         converter.cmdline
#         self.outfile = converter._list_outputs()
        for ef in options:
            setattr(converter.inputs, ef, options[ef])
        self.res = converter.run()

    def nii_file(self: 'path'):
        return self.res.outputs.nii_file

##############################################################################


class Dcm2nii:
    def __init__(self, source_names=['', '']):
        from nipype.interfaces.dcm2nii import Dcm2nii
        converter = Dcm2nii()
        converter.inputs.source_names = source_names
        converter.inputs.gzip_output = True
        converter.inputs.output_dir = '.'
        converter.cmdline
        converter.run()

    def dicom_file(self: 'path'):
        return self.outfile
