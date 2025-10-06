class dcmstack_CopyMeta:
    """
    Note:
        dependencies: Nipype, AFNI
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, src_file='path', dest_file='path', **options):
        from nipype.interfaces.dcmstack import CopyMeta
        copmeta = CopyMeta()
        copmeta.inputs.src_file = src_file
        copmeta.inputs.dest_file = dest_file
        for ef in options:
            setattr(copmeta.inputs, ef, options[ef])
        self.res = copmeta.run()

    def dest_file(self: 'path'):
        return self.res.outputs.dest_file

##############################################################################


class dcmstack_MergeNifti:
    def __init__(self, in_files=['path'], **options):
        from nipype.interfaces.dcmstack import MergeNifti
        mergeNif = MergeNifti()
        mergeNif.inputs.in_files = in_files
        for ef in options:
            setattr(mergeNif.inputs, ef, options[ef])
        self.res = mergeNif.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class dcmstack_SplitNifti():
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.dcmstack import SplitNifti
        split = SplitNifti()
        split.inputs.in_file = in_file
        for ef in options:
            setattr(split.inputs, ef, options[ef])
        self.res = split.run()

    def out_list(self: 'list_path'):
        return self.res.outputs.out_list
