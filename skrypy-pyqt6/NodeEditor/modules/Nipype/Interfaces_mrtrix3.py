class mrtrix3_DWIDenoise():
    """
    Note:
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.mrtrix3 import DWIDenoise
        denoise = DWIDenoise()
        denoise.inputs.in_file = in_file
        for ef in options:
            setattr(denoise.inputs, ef, options[ef])
        self.res = denoise.run()

    def noise(self: 'path'):
        return self.res.outputs.noise

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class mrtrix3_Tractography():
    """
    Note:
        dependencies: Nipype, MRtrix3
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', out_file='path', **options):
        import nipype.interfaces.mrtrix3 as mrt
        tk = mrt.Tractography()
        tk.inputs.in_file = in_file
        tk.inputs.out_file = out_file
        for ef in options:
            setattr(tk.inputs, ef, options[ef])
        self.res = tk.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

    def out_seeds(self: 'path'):
        return self.res.outputs.out_seeds

##############################################################################


class mrtrix3_DWIExtract():
    """
    Note:
        dependencies: Nipype, MRtrix3
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', out_file='path', **options):
        from nipype.interfaces.mrtrix3 import DWIExtract
        dwiextract = DWIExtract()
        dwiextract.inputs.in_file = in_file
        dwiextract.inputs.out_file = out_file
        for ef in options:
            setattr(dwiextract.inputs, ef, options[ef])
        self.res = dwiextract.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class mrtrix3_MRConvert():
    """
    Note:
        dependencies: Nipype, MRtrix3
        GUI: 'no'
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', out_file='path', **options):
        from nipype.interfaces.mrtrix3 import MRConvert
        mrconvert = MRConvert()
        mrconvert.inputs.in_file = in_file
        mrconvert.inputs.out_file = out_file
        for ef in options:
            setattr(mrconvert.inputs, ef, options[ef])
        self.res = mrconvert.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file
