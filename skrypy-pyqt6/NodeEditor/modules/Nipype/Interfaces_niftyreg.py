class niftyreg_RegResample():
    def __init__(self, flo_file='path', ref_file='path', **options):
        from nipype.interfaces import niftyreg
        node = niftyreg.RegResample()
        node.inputs.flo_file = flo_file
        node.inputs.ref_file = ref_file
        for ef in options:
            setattr(node.inputs, ef, options[ef])
        self.res = node.run()

    def out_file(self) -> None:
        return self.res.outputs.out_file
