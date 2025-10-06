class dti_DTIRecon():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, DWI='path', bvals='path', bvecs='path', **options):
        from nipype.interfaces.diffusion_toolkit import DTIRecon
        mf = DTIRecon()
        mf.inputs.DWI = DWI
        mf.inputs.bvals = bvals
        mf.inputs.bvecs = bvecs
        for ef in options:
            setattr(mf.inputs, ef, options[ef])
        self.res = mf.run()

    def ADC(self: 'path'):
        return self.res.outputs.ADC

    def B0(self: 'path'):
        return self.res.outputs.B0

    def FA(self: 'path'):
        return self.res.outputs.FA

    def FA_color(self: 'path'):
        return self.res.outputs.FA_color

    def L1(self: 'path'):
        return self.res.outputs.L1

    def L2(self: 'path'):
        return self.res.outputs.L2

    def L3(self: 'path'):
        return self.res.outputs.L3

    def V1(self: 'path'):
        return self.res.outputs.V1

    def V2(self: 'path'):
        return self.res.outputs.V2

    def V3(self: 'path'):
        return self.res.outputs.V3

    def exp(self: 'path'):
        return self.res.outputs.exp

    def tensor(self: 'path'):
        return self.res.outputs.tensor
