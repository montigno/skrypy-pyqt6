class fsl_ApplyMask():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', mask_file='path', **options):
        from nipype.interfaces.fsl import ApplyMask
        mf = ApplyMask()
        mf.inputs.in_file = in_file
        mf.inputs.mask_file = mask_file
        for ef in options:
            setattr(mf.inputs, ef, options[ef])
        self.res = mf.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_BinaryMaths():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', operand_file='path', operand_value=0.0,
                 operation="enumerate(('add','sub','mul','div',\
                                       'rem','max','min'))",
                 **options):
        from nipype.interfaces.fsl import BinaryMaths
        import os
        mf = BinaryMaths()
        mf.inputs.in_file = in_file
        if os.path.exists(operand_file):
            mf.inputs.operand_file = operand_file
        else:
            mf.inputs.operand_value = operand_value
        mf.inputs.operation = operation
        for ef in options:
            setattr(mf.inputs, ef, options[ef])
        self.res = mf.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_EddyCorrect():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', ref_num=0, **options):
        from nipype.interfaces.fsl import EddyCorrect
        eddyc = EddyCorrect()
        eddyc.inputs.in_file = in_file
        eddyc.inputs.ref_num = ref_num
        for ef in options:
            setattr(eddyc.inputs, ef, options[ef])
        eddyc.cmdline
        self.res = eddyc.run()

    def eddy_corrected(self: 'path'):
        return self.res.outputs.eddy_corrected

##############################################################################


class fsl_Threshold():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', thresh=0.0, **options):
        from nipype.interfaces.fsl import Threshold
        mf = Threshold()
        mf.inputs.in_file = in_file
        mf.inputs.thresh = thresh
        for ef in options:
            setattr(mf.inputs, ef, options[ef])
        self.res = mf.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_UnaryMaths():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path',
                 operation="enumerate(('exp','log',\
                                       'sin','cos','tan',\
                                       'asin','acos','atan',\
                                       'sqr','sqrt','recip','abs',\
                                       'bin','binv','fillh','fillh26',\
                                       'index','edge','nan','nanm',\
                                       'rand','randn','range'))", **options):
        from nipype.interfaces.fsl import UnaryMaths
        mf = UnaryMaths()
        mf.inputs.in_file = in_file
        mf.inputs.operation = operation
        for ef in options:
            setattr(mf.inputs, ef, options[ef])
        self.res = mf.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_ApplyWarp:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', ref_file='path', **options):
        from nipype.interfaces import fsl
        aw = fsl.ApplyWarp()
        aw.inputs.in_file = in_file
        aw.inputs.ref_file = ref_file
        for ef in options:
            setattr(aw.inputs, ef, options[ef])
        self.res = aw.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_ApplyXFM:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', reference='path', **options):
        from nipype.interfaces import fsl
        applyxfm = fsl.ApplyXFM()
        applyxfm.inputs.in_file = in_file
        applyxfm.inputs.reference = reference
        for ef in options:
            setattr(applyxfm.inputs, ef, options[ef])
        self.res = applyxfm.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

    def out_log(self: 'path'):
        return self.res.outputs.out_log

    def out_matrix_file(self: 'path'):
        return self.res.outputs.out_matrix_file

##############################################################################


class fsl_BET:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces import fsl
        btr = fsl.BET()
        btr.inputs.in_file = in_file
        for ef in options:
            setattr(btr.inputs, ef, options[ef])
        self.res = btr.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

    def mask_file(self: 'path'):
        return self.res.outputs.mask_file

    def outline_file(self: 'path'):
        return self.res.outputs.outline_file

    def meshfile(self: 'path'):
        return self.res.outputs.meshfile

    def inskull_mask_file(self: 'path'):
        return self.res.outputs.inskull_mask_file

    def inskull_mesh_file(self: 'path'):
        return self.res.outputs.inskull_mesh_file

    def outskull_mask_file(self: 'path'):
        return self.res.outputs.outskull_mask_file

    def outskull_mesh_file(self: 'path'):
        return self.res.outputs.outskull_mesh_file

    def outskin_mask_file(self: 'path'):
        return self.res.outputs.outskin_mask_file

    def outskin_mesh_file(self: 'path'):
        return self.res.outputs.outskin_mesh_file

    def skull_mask_file(self: 'path'):
        return self.res.outputs.skull_mask_file

##############################################################################


class fsl_FAST:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_files=['path'], **options):
        from nipype.interfaces import fsl
        fastr = fsl.FAST()
        fastr.inputs.in_files = in_files
        for ef in options:
            setattr(fastr.inputs, ef, options[ef])
        self.res = fastr.run()

    def tissue_class_map(self: 'path'):
        return self.res.outputs.tissue_class_map

    def tissue_class_files(self: 'list_path'):
        return self.res.outputs.tissue_class_files

    def restored_image(self: 'list_path'):
        return self.res.outputs.restored_image

    def mixeltype(self: 'path'):
        return self.res.outputs.mixeltype

    def partial_volume_map(self: 'path'):
        return self.res.outputs.partial_volume_map

    def partial_volume_files(self: 'list_path'):
        return self.res.outputs.partial_volume_files

    def bias_field(self: 'list_path'):
        return self.res.outputs.bias_field

    def probability_maps(self: 'list_path'):
        return self.res.outputs.probability_maps

##############################################################################


class fsl_FLIRT:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.fsl.preprocess.html#flirt
    """
    def __init__(self, in_file='path', reference='path', **options):
        from nipype.interfaces import fsl
        flt = fsl.FLIRT()
        flt.inputs.in_file = in_file
        flt.inputs.reference = reference
        for ef in options:
            setattr(flt.inputs, ef, options[ef])
        self.res = flt.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

    def out_log(self: 'path'):
        return self.res.outputs.out_log

    def out_matrix_file(self: 'path'):
        return self.res.outputs.out_matrix_file

##############################################################################


class fsl_FNIRT:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', ref_file='path', **options):
        from nipype.interfaces import fsl
        fnt = fsl.FNIRT()
        fnt.inputs.in_file = in_file
        fnt.inputs.ref_file = ref_file
        for ef in options:
            setattr(fnt.inputs, ef, options[ef])
        self.res = fnt.run()

    def field_file(self: 'path'):
        return self.res.outputs.field_file

    def fieldcoeff_file(self: 'path'):
        return self.res.outputs.fieldcoeff_file

    def jacobian_file(self: 'path'):
        return self.res.outputs.jacobian_file

    def log_file(self: 'path'):
        return self.res.outputs.log_file

    def modulatedref_file(self: 'path'):
        return self.res.outputs.modulatedref_file

    def out_intensitymap_file(self: 'path'):
        return self.res.outputs.out_intensitymap_file

    def warped_file(self: 'path'):
        return self.res.outputs.warped_file

##############################################################################


class fsl_MCFLIRT:
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces import fsl
        mcflt = fsl.MCFLIRT()
        mcflt.inputs.in_file = in_file
        for ef in options:
            setattr(mcflt.inputs, ef, options[ef])
        self.res = mcflt.run()

    def mat_file(self: 'list_path'):
        return self.res.outputs.mat_file

    def mean_img(self: 'path'):
        return self.res.outputs.mean_img

    def out_file(self: 'path'):
        return self.res.outputs.out_file

    def par_file(self: 'path'):
        return self.res.outputs.par_file

    def rms_files(self: 'list_path'):
        return self.res.outputs.rms_files

    def std_img(self: 'path'):
        return self.res.outputs.std_img

    def variance_img(self: 'path'):
        return self.res.outputs.variance_img

##############################################################################


class fsl_MeanImage():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.fsl import MeanImage
        fu = MeanImage()
        fu.inputs.in_file = in_file
        for ef in options:
            setattr(fu.inputs, ef, options[ef])
        self.res = fu.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_Merge():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_files=['path'],
                 dimension="enumerate(('t','x','y','z','a'))", **options):
        from nipype.interfaces.fsl import Merge
        fu = Merge()
        fu.inputs.in_files = in_files
        fu.inputs.dimension = dimension
        for ef in options:
            setattr(fu.inputs, ef, options[ef])
        self.res = fu.run()

    def merged_file(self: 'path'):
        return self.res.outputs.merged_file

##############################################################################


class fsl_Overlay():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, auto_thresh_bg=False, background_image='path', bg_thresh=(0.0, 10),
                 full_bg_range=False, stat_image='path', stat_thresh=(0.0, 10.0), **options):
        from nipype.interfaces.fsl import Overlay
        comb = Overlay()
        comb.inputs.background_image = background_image
        if auto_thresh_bg:
            comb.inputs.auto_thresh_bg = auto_thresh_bg
        elif full_bg_range:
            comb.inputs.full_bg_range = full_bg_range
        else:
            comb.inputs.bg_thresh = bg_thresh
        comb.inputs.stat_thresh = stat_thresh
        comb.inputs.stat_image = stat_image
        for ef in options:
            setattr(comb.inputs, ef, options[ef])
        self.res = comb.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_SpatialFilter():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path',
                 operation="enumerate(('mean','median','meanu'))", **options):
        from nipype.interfaces.fsl import SpatialFilter
        fu = SpatialFilter()
        fu.inputs.in_file = in_file
        fu.inputs.operation = operation
        for ef in options:
            setattr(fu.inputs, ef, options[ef])
        self.res = fu.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file
##############################################################################


class fsl_Split():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path',
                 dimension="enumerate(('t','x','y','z'))", **options):
        from nipype.interfaces.fsl import Split
        fu = Split()
        fu.inputs.in_file = in_file
        fu.inputs.dimension = dimension
        for ef in options:
            setattr(fu.inputs, ef, options[ef])
        self.res = fu.run()

    def out_files(self: 'list_path'):
        return self.res.outputs.out_files

##############################################################################


class fsl_SwapDimensions():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', new_dims=('x', 'y', 'z'), **options):
        from nipype.interfaces.fsl import SwapDimensions
        fu = SwapDimensions()
        fu.inputs.in_file = in_file
        fu.inputs.new_dims = new_dims
        for ef in options:
            setattr(fu.inputs, ef, options[ef])
        self.res = fu.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_ExtractROI():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.fsl import ExtractROI
        fslroi = ExtractROI()
        fslroi.inputs.in_file = in_file
        for ef in options:
            setattr(fslroi.inputs, ef, options[ef])
        self.res = fslroi.run()

    def roi_file(self: 'path'):
        return self.res.outputs.roi_file

##############################################################################


class fsl_ImageMaths():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.fsl import ImageMaths
        fslmaths = ImageMaths()
        fslmaths.inputs.in_file = in_file
        for ef in options:
            setattr(fslmaths.inputs, ef, options[ef])
        self.res = fslmaths.run()

    def out_file(self: 'path'):
        return self.res.outputs.out_file

##############################################################################


class fsl_Smooth():
    """
    Note:
        dependencies: Nipype, fsl
        GUI: no
        link_web: (click Ctrl + U)
    """
    def __init__(self, in_file='path', **options):
        from nipype.interfaces.fsl import Smooth
        sm = Smooth()
        sm.inputs.in_file = in_file
        for ef in options:
            setattr(sm.inputs, ef, options[ef])
        self.res = sm.run()

    def smoothed_file(self: 'path'):
        return self.res.outputs.smoothed_file

##############################################################################
