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

    def ADC(self) -> None:
        return self.res.outputs.ADC

    def B0(self) -> None:
        return self.res.outputs.B0

    def FA(self) -> None:
        return self.res.outputs.FA

    def FA_color(self) -> None:
        return self.res.outputs.FA_color

    def L1(self) -> None:
        return self.res.outputs.L1

    def L2(self) -> None:
        return self.res.outputs.L2

    def L3(self) -> None:
        return self.res.outputs.L3

    def V1(self) -> None:
        return self.res.outputs.V1

    def V2(self) -> None:
        return self.res.outputs.V2

    def V3(self) -> None:
        return self.res.outputs.V3

    def exp(self) -> None:
        return self.res.outputs.exp

    def tensor(self) -> None:
        return self.res.outputs.tensor
