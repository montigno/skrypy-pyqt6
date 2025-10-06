class image_Reorient():
    """
    Note:
        dependencies: Nipype
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.image import Reorient
        import os
        import shutil
        reorient = Reorient()
        reorient.inputs.in_file = in_file
        for ef in options:
            setattr(reorient.inputs, ef, options[ef])
        self.res = reorient.run()
        old_path_file = self.res.outputs.out_file
        name_file = os.path.basename(old_path_file)
        cur_dir = os.path.dirname(in_file)
        new_path_file = os.path.join(cur_dir, name_file)
        shutil.move(old_path_file, new_path_file)
        self.outfile = new_path_file

    def out_file(self: 'path'):
        return self.outfile

    def transform(self: 'path'):
        return self.res.outputs.transform

##############################################################################


class image_Rescale():
    """
    Note:
        dependencies: Nipype
        GUI: 'no'
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', ref_file='path', **options):
        from nipype.interfaces.image import Rescale
        invert_t1w = Rescale(invert=True)
        invert_t1w.inputs.in_file = in_file
        invert_t1w.inputs.ref_file = ref_file
        for ef in options:
            setattr(invert_t1w.inputs, ef, options[ef])
        self.res = invert_t1w.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file
