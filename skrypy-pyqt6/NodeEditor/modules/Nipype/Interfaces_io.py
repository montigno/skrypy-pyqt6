class io_S3DataGrabber():
    """
    Note:
        dependencies: Nipype
        GUI: 'no'
        link_web: (click Ctrl + U)
    """
    def __init__(self,
                 infields='',
                 outfields='',
                 bucket='', sort_filelist=True, template='path', **options):
        from nipype.interfaces.io import S3DataGrabber
        s3grab = S3DataGrabber(infields, outfields)
        s3grab.inputs.bucket = bucket
        s3grab.inputs.sort_filelist = sort_filelist
        s3grab.inputs.template = template
        for ef in options:
            setattr(s3grab.inputs, ef, options[ef])
        self.res = s3grab.run()

    def outfiles(self: 'list_path'):
        return self.res.outputs.outfiles

##############################################################################


class io_DataSink():
    """
    Note:
        dependencies: Nipype
        GUI: 'no'
        link_web: (click Ctrl + U)
    """
    def __init__(self, infields='', outfields='', **options):
        from nipype.interfaces.io import DataSink
        ds = DataSink(infields)
        for ef in options:
            setattr(ds.inputs, ef, options[ef])
        self.res = ds.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file
